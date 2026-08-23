import asyncio
import time
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Label
from textual.worker import Worker, WorkerState

from autorecon.core.config import PRESETS, APP_NAME, APP_VERSION
from autorecon.core.validator import validate_target
from autorecon.ui.components import TargetInputArea, ProfileSelector, ActionArea, ConsoleOutput
from autorecon.reporting.html_reporter import generate_html_report
from autorecon.reporting.json_reporter import generate_json_report

from autorecon.modules.ping_module import PingModule
from autorecon.modules.whois_module import WhoisModule
from autorecon.modules.dns_module import DnsModule
from autorecon.modules.subdomain_module import SubdomainModule
from autorecon.modules.nmap_module import NmapModule
from autorecon.modules.nikto_module import NiktoModule

class AutoReconApp(App):
    CSS_PATH = "styles.tcss"
    TITLE = APP_NAME
    SUB_TITLE = f"v{APP_VERSION} - Educational Reconnaissance Framework"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("c", "clear_console", "Clear Console"),
    ]

    def __init__(self):
        super().__init__()
        self.selected_profile = list(PRESETS.keys())[0]
        self.is_scanning = False
        self.worker = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main-container"):
            with Vertical(id="sidebar"):
                yield TargetInputArea(classes="card")
                yield ProfileSelector(PRESETS)
                yield ActionArea(classes="card")
            with Vertical(id="main-content"):
                yield ConsoleOutput(classes="card")
        yield Footer()

    def on_mount(self) -> None:
        self.log_msg("[*] AutoRecon Studio Initialized")
        self.log_msg("[*] Select a profile and enter a target to begin.")

    def log_msg(self, msg: str) -> None:
        console = self.query_one("#console-output")
        console.write(msg)

    def on_profile_selector_profile_selected(self, message: ProfileSelector.ProfileSelected) -> None:
        self.selected_profile = message.profile_id
        profile_name = PRESETS[self.selected_profile]["name"]
        self.log_msg(f"[*] Selected Profile: {profile_name}")

    async def on_button_pressed(self, event) -> None:
        if event.button.id == "start-btn":
            if self.is_scanning:
                return
            await self.start_scan()
        elif event.button.id == "stop-btn":
            if self.is_scanning and self.worker:
                self.worker.cancel()
                self.log_msg("[!] Scan cancelled by user.")

    async def start_scan(self):
        target_input = self.query_one("#target-input").value
        status_label = self.query_one("#target-status")
        
        validation = validate_target(target_input)
        if not validation["valid"]:
            status_label.update(f"[red]{validation['error']}[/red]")
            return
            
        target = validation["target"]
        if validation["private"]:
            status_label.update(f"[yellow]Warning: Private IP Detected[/yellow]")
        else:
            status_label.update(f"[green]Valid Target: {validation['type']}[/green]")

        self.is_scanning = True
        self.query_one("#start-btn").disabled = True
        self.query_one("#stop-btn").disabled = False
        self.query_one("#console-output").clear()
        
        self.log_msg(f"[*] Starting scan against {target} using profile '{PRESETS[self.selected_profile]['name']}'")
        
        # Start worker
        self.worker = self.run_worker(self.run_modules(target, self.selected_profile), exclusive=True)

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.state in (WorkerState.SUCCESS, WorkerState.ERROR, WorkerState.CANCELLED):
            self.is_scanning = False
            self.query_one("#start-btn").disabled = False
            self.query_one("#stop-btn").disabled = True
            
            if event.state == WorkerState.SUCCESS:
                self.log_msg("\n[+] Scan execution completed.")
            elif event.state == WorkerState.ERROR:
                self.log_msg(f"\n[!] Scan failed with error: {event.worker.error}")

    async def run_modules(self, target: str, profile_id: str):
        profile = PRESETS[profile_id]
        modules_to_run = profile["modules"]
        
        results = {}
        start_time = time.time()
        
        for mod_key in modules_to_run:
            module = self.get_module_instance(mod_key, target)
            if not module:
                continue
                
            self.log_msg(f"\n{'='*40}")
            self.log_msg(f"[*] Starting Module: {module.name}")
            self.log_msg(f"{'='*40}")
            
            module_output = []
            try:
                async for line in module.execute():
                    self.log_msg(line)
                    module_output.append(line)
            except asyncio.CancelledError:
                self.log_msg("[!] Module execution cancelled.")
                raise
            except Exception as e:
                self.log_msg(f"[!] Module error: {e}")
                
            results[module.name] = "\n".join(module_output)
            
        duration = int(time.time() - start_time)
        self.log_msg("\n[*] Generating HTML Report...")
        try:
            report_path = generate_html_report(target, results, duration)
            generate_json_report(target, results, duration)
            self.log_msg(f"[+] HTML Report saved to: {report_path}")
        except Exception as e:
            self.log_msg(f"[-] Failed to generate report: {e}")
            
    def get_module_instance(self, mod_key: str, target: str):
        if mod_key == "ping":
            return PingModule(target)
        elif mod_key == "whois":
            return WhoisModule(target)
        elif mod_key == "dns":
            return DnsModule(target)
        elif mod_key == "subdomain":
            return SubdomainModule(target)
        elif mod_key == "nikto":
            return NiktoModule(target)
        elif mod_key.startswith("nmap_"):
            scan_type = mod_key.split("_")[1]
            return NmapModule(target, scan_type=scan_type)
        return None

    def action_clear_console(self) -> None:
        self.query_one("#console-output").clear()
