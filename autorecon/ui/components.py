from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Input, Button, Label, ListItem, ListView, RichLog
from textual.message import Message

class TargetInputArea(Vertical):
    def compose(self) -> ComposeResult:
        yield Label("Target IP or Domain:", classes="card-title")
        yield Input(placeholder="e.g. scanme.nmap.org or 192.168.1.1", id="target-input")
        yield Label("", id="target-status")

class ProfileSelector(Vertical):
    class ProfileSelected(Message):
        def __init__(self, profile_id: str):
            self.profile_id = profile_id
            super().__init__()

    def __init__(self, profiles: dict):
        super().__init__()
        self.profiles = profiles

    def compose(self) -> ComposeResult:
        yield Label("Scan Profile", classes="card-title")
        with ListView(id="profile-list"):
            for pid, profile in self.profiles.items():
                yield ListItem(Label(f"[b]{profile['name']}[/b]\n[dim]{profile['description']}[/dim]"), id=f"prof_{pid}")

    def on_list_view_selected(self, event: ListView.Selected):
        item_id = event.item.id
        if item_id and item_id.startswith("prof_"):
            self.post_message(self.ProfileSelected(item_id[5:]))

class ActionArea(Horizontal):
    def compose(self) -> ComposeResult:
        yield Button("Start Scan", id="start-btn", variant="primary")
        yield Button("Stop", id="stop-btn", classes="stop-btn", disabled=True)

class ConsoleOutput(Vertical):
    def compose(self) -> ComposeResult:
        yield Label("Live Execution Console", classes="card-title")
        yield RichLog(id="console-output", markup=True, highlight=True, wrap=True)
