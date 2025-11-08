# Cyber‑Toolkit – Defensive Security Tools

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Port Scanner (Python)](#port-scanner-python)
- [Log Monitor (Bash)](#log-monitor-bash)
- [Sub‑Domain Enumerator (Node.js)](#sub-domain-enumerator-nodejs)
- [License](#license)

---

## Overview
A small collection of open‑source scripts for:
* **Port scanning** – discover open services on a host or network.
* **Log monitoring** – watch log files live and alert on suspicious patterns.
* **Sub‑domain enumeration** – gather sub‑domains for a target domain using public sources.

All tools are written to be easy to understand, modify, and integrate into larger automation pipelines.

---

## Installation

### Prerequisites
| Tool | Required Runtime |
|------|-------------------|
| Port scanner | Python 3.8+ |
| Log monitor | Bash (Linux/macOS) + `mail` (or `sendmail`) for alerts |
| Sub‑domain enumerator | Node.js 14+ & npm |

### Step‑by‑step

```bash
# Clone the repo (or copy the files) into a folder
git clone https://github.com/yourusername/cyber-toolkit.git
cd cyber-toolkit

# Python dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Node.js dependencies (subdomain enumerator)
npm install
```

---

## Port Scanner (Python)

### Run
```bash
# Scan a single host (all ports 1‑1024)
python3 port_scanner.py -t 192.168.1.10 -p 1-1024

# Scan multiple hosts from a file, output CSV
python3 port_scanner.py -i hosts.txt -p 80,443,8080 -o results.csv
```

### Options
```
-t, --target      Single IP or hostname
-i, --input       File with one target per line
-p, --ports       Port list (e.g., 22,80,443) or range (1-1024)
-o, --output      CSV file for results (optional)
--threads         Number of concurrent threads (default: 100)
```

---

## Log Monitor (Bash)

### Run
```bash
# Tail /var/log/auth.log and alert on "Failed password"
./log_monitor.sh -f /var/log/auth.log -r "Failed password" -e admin@example.com

# Watch custom log, output matches to JSON
./log_monitor.sh -f myapp.log -r "ERROR|WARN" -j matches.json
```

### Options
```
-f, --file          Log file to watch (required)
-r, --regex         PCRE pattern to match (required)
-e, --email         Email address for alerts (optional)
-j, --json-output   Write matches to JSON file (optional)
```

---

## Sub‑Domain Enumerator (Node.js)

### Run
```bash
# Enumerate subdomains for example.com, output CSV
node subdomain_enum.js -d example.com -o subs.csv

# JSON output
node subdomain_enum.js -d example.org -j subs.json
```

### Options
```
-d, --domain       Target domain (required)
-o, --output       CSV file name (optional)
-j, --json         JSON output file name (optional)
```

---

## License
All scripts are released under the **MIT License** – you’re free to use, modify, and distribute them. See the `LICENSE` file for details.

---

*Disclaimer*: These tools are provided **as‑is** for defensive and educational purposes. Do not run them against systems you do **not** have explicit permission to test. Misuse may be illegal.