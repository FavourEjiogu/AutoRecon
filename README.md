# AutoRecon Studio

![AutoRecon Studio](https://img.shields.io/badge/Status-Active-success)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

AutoRecon Studio is an educational and research-grade reconnaissance suite designed for Kali Linux. It orchestrates passive OSINT and active network probing tools through a unified modern Textual terminal user interface (TUI) and generates standalone HTML reports.

## Features

- **Interactive TUI**: Mouse-clickable, keyboard-navigable Textual interface styled with a sleek, modern dark theme.
- **Passive OSINT**: WHOIS lookup, DNS record querying (`dig`), and Subdomain discovery (`subfinder` + public Certificate Transparency `crt.sh` fallback).
- **Active Probing**: ICMP latency testing (`ping`), Nmap port/service/OS scanning (`nmap`), and web vulnerability auditing (`nikto`).
- **Automated Dependency Management**: Checks for missing system binaries and prompts for automated `sudo apt` installation before launching.
- **Reporting**: Generates standalone single-file offline-friendly responsive HTML reports with metric summary cards and structured JSON telemetry.
- **Headless CLI Mode**: Includes a Command-Line Interface (`autorecon_cli.py`) for automated research scripts and batch runs.

## Prerequisites

- Kali Linux (or Debian-based system)
- Python 3.10+
- System tools (handled by the setup script or auto-installer): `ping`, `whois`, `dig`, `nmap`, `subfinder`, `nikto`

## Installation

```bash
# Clone the repository
git clone https://github.com/favourejiogu/AutoRecon.git
cd AutoRecon

# Run the setup script to create a virtual environment and install python dependencies
chmod +x setup.sh
./setup.sh
```

## Usage

### Interactive TUI (Recommended)
Launch the interactive terminal interface:
```bash
source .venv/bin/activate
python3 app.py
```
- Select a scan profile from the sidebar (e.g. Quick Passive, Full Surface Audit).
- Enter the target domain or IP.
- Click `Start Scan`.
- View live execution logs and find the generated HTML report in the `reports/` folder.

### Headless CLI Mode
For automated scripting and batch testing, use the CLI mode:
```bash
source .venv/bin/activate
python3 autorecon_cli.py -t scanme.nmap.org -p quick_passive
```

Available profiles: 
- `quick_passive`
- `host_verification`
- `full_surface_audit`
- `web_discovery`
- `deep_port_scan`
- `dns_only`

## Ethical Usage & Disclaimer

This tool is built strictly for **educational purposes** and **authorized auditing/research**. 
- Do not execute active scanning modules (e.g., Nmap, Nikto) against targets without explicit, written permission. 
- Passive modules (WHOIS, DNS, crt.sh) are generally considered safe open-source intelligence (OSINT), but usage must comply with your local laws and Terms of Service.
- The author is not responsible for any misuse or damage caused by this program.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
