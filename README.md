<img width="1440" height="742" alt="image" src="https://github.com/user-attachments/assets/5224ad91-ffe4-41fc-a47b-1a8588552746" />


---
# 🕷 nn0nn

> Passive recon & surface mapping tool for bug bounty hunters.

**nn0nn** crawls a target, crosses data from multiple passive sources and generates a structured report — without sending a single active probe. Designed to be the first step of any BBG engagement or web pentest before you touch any active recon tool.

---

## What it does

- Crawls the target and extracts endpoints, links, parameters, and forms
- Pulls and analyzes JavaScript files looking for secrets, tokens and hidden endpoints
- Inspects TLS certificate and security headers
- Enumerates subdomains passively via crt.sh
- Cross-references IPs and services with Shodan
- Correlates everything into a single unified report (JSON + HTML)

## What it does NOT do

The tool **nn0nn** is **strictly passive**. No fuzzing, no brute-force, no active scanning. If you want to fuzz, that's a different tool and a different scope.

---

## Installation

```bash
git clone https://github.com/yourusername/nn0nn.git
cd nn0nn
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Requirements**: Python 3.10+

---

## Configuration

> Copy the example config and add your API keys:

```bash
cp config.example.env .env
```

```env
SHODAN_API_KEY=your_key_here
```

Shodan is optional. If no key is provided, nn0nn skips that module and runs everything else normally.

---

## Usage

```bash
# Basic recon
python main.py -t example.com

# With Shodan correlation
python main.py -t example.com --shodan

# Custom output directory
python main.py -t example.com -o ./reports/

# Verbose output
python main.py -t example.com -v
```

### Options

| Flag | Description |
|------|-------------|
| `-t`, `--target` | Target domain (required) |
| `-o`, `--output` | Output directory (default: `./output/`) |
| `--shodan` | Enable Shodan cross-reference |
| `--no-js` | Skip JavaScript analysis |
| `--no-subdomains` | Skip subdomain enumeration |
| `-v`, `--verbose` | Verbose output |
| `--format` | Output format: `json`, `html`, `both` (default: `both`) |

---

## 📋 Output

> It generates two files per run inside the output directory:

```
output/
└── example.com_2024-01-15_10-30/
    ├── report.json     ← structured data, feed it to other tools
    └── report.html     ← human-readable report
```

> The *JSON* output is designed to be piped into other tools like nuclei or your own scripts.

---

## Project structure

```
nn0nn/
├── main.py                  # entry point & CLI
├── requirements.txt
├── config.example.env
│
├── core/
│   ├── http_client.py       # shared httpx client
│   └── config.py            # settings & API keys loader
│
├── collectors/
│   ├── crawler.py           # links, endpoints, forms, parameters
│   ├── js_analyzer.py       # JS files download & secrets extraction
│   ├── ssl_inspector.py     # TLS cert & cipher inspection
│   ├── headers_analyzer.py  # security headers analysis
│   ├── subdomains.py        # passive subdomain enum via crt.sh
│   └── shodan_lookup.py     # Shodan API integration
│
├── analyzers/
│   ├── correlator.py        # merges all collector outputs
│   └── secrets_finder.py    # regex patterns for secrets & tokens
│
└── output/
    ├── json_exporter.py
    ├── html_reporter.py
    └── templates/
        └── report.html
```

---

## Passive sources

| Source | What it provides |
|--------|-----------------|
| Target crawl | Endpoints, links, forms, parameters, JS files |
| crt.sh | Passive subdomain enumeration via certificate transparency |
| Shodan | Open ports, services, banners, known vulns (optional) |
| TLS inspection | Certificate validity, expiry, cipher suites |
| HTTP headers | Security headers, server info, tech stack hints |

---

## Secrets detection

> Looks for the following patterns inside JavaScript files and HTML source:

- AWS Access Keys (`AKIA...`)
- Google API Keys (`AIza...`)
- JWT tokens
- Generic API keys and Bearer tokens
- Hardcoded passwords and credentials
- Internal endpoints and IP addresses

---

## Roadmap

- [ ] VirusTotal passive lookup
- [ ] WaybackMachine URL extraction
- [ ] Output to SQLite for persistent storage across runs
- [ ] Integration with nuclei templates on found endpoints

---

## ‼️ Disclaimer

> **nn0nn** is built for **authorized security testing only**. Only use it against targets you have explicit permission and authorization to test. The author is not responsible for misuse.
