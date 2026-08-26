# AutoRecon Studio

AutoRecon Studio is an educational and research-purpose reconnaissance suite designed for Kali Linux. It orchestrates passive OSINT and active network probing tools through a unified modern Textual TUI and standalone HTML report generator.

## Prerequisites
- Kali Linux (or Debian-based system)
- Python 3.10+
- `ping`, `whois`, `dig`, `nmap`, `subfinder`, `nikto`

## Installation

```bash
# Clone the repository
git clone https://github.com/favourejiogu/AutoRecon.git
cd AutoRecon

# Ensure system tools are installed (run manually)
sudo apt-get install -y python3-venv python3-pip iputils-ping whois dnsutils nmap subfinder nikto

# Run the setup script to create a virtual environment
chmod +x setup.sh
./setup.sh
```

## Usage

### Interactive TUI (Recommended)
Launch the mouse-clickable, keyboard-navigable Textual interface:
```bash
source .venv/bin/activate
python3 app.py
```
- Select a scan profile from the sidebar.
- Enter the target domain or IP.
- Click `Start Scan`.
- Output is generated in the `reports/` folder.

### Headless CLI Mode
For automated scripting and batch testing, use the CLI mode:
```bash
source .venv/bin/activate
python3 autorecon_cli.py -t scanme.nmap.org -p quick_passive
```
Available profiles: `quick_passive`, `host_verification`, `full_surface_audit`, `web_discovery`, `deep_port_scan`, `dns_only`.

## Project Structure
- `app.py`: TUI entrypoint
- `autorecon_cli.py`: Headless CLI entrypoint
- `autorecon/core/`: Configuration, dependencies, and validation engines.
- `autorecon/modules/`: Concrete implementations for `ping`, `nmap`, `subfinder`, etc.
- `autorecon/reporting/`: Generators for JSON telemetry and responsive HTML reports.
- `autorecon/ui/`: Textual interface layouts and styles.

## Ethical Usage
This tool is built strictly for **educational purposes** and **authorized auditing**. Do not execute active scanning modules (e.g., Nmap, Nikto) against targets without explicit, written permission. Passive modules (WHOIS, DNS, crt.sh) are generally considered safe open-source intelligence (OSINT).
