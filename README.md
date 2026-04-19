<img width="1440" height="742" alt="image" src="https://github.com/user-attachments/assets/5224ad91-ffe4-41fc-a47b-1a8588552746" />


---
# 🕷 nn0nn

## 🕸 Passive recon & surface mapping tool for bug bounty hunters 🪲

> **nn0nn** crawls a target, crosses data from multiple passive sources and generates a structured report — without sending a single active probe. Designed to be the first step of any BBG engagement or web pentest before you touch any active recon tool.

---

## ✅ What it does

- Crawls the target and extracts endpoints, links, parameters, and forms
- Pulls and analyzes JavaScript files looking for secrets, tokens and hidden endpoints
- Inspects TLS certificate and security headers
- Enumerates subdomains passively via crt.sh
- Cross-references IPs and services with Shodan
- Correlates everything into a single unified report (JSON + HTML)

## ❗️What it does NOT do

The tool **nn0nn** is **strictly passive**. No fuzzing, no brute-force, no active scanning. If you want to fuzz, that's a different tool and a different scope.

---

## 💿 Installation

```bash
git clone https://github.com/DreddSec/nn0nn.git
cd nn0nn
pip install -e .
cp config.example.env .env   # add the keys here
nn0nn -t empresa.com
```

**Requirements**: Python 3.10+

---

## ℹ️ Usage

```bash
# Basic recon
nn0nn -t example.com

# With Shodan correlation
nn0nn -t example.com --shodan

# Custom output directory
nn0nn -t example.com -o ./reports/

# Verbose output
nn0nn -t example.com -v
```

### 🔄 Options

| Flag | Description |
|------|-------------|
| `-t`, `--target` | Target domain (required) |
| `-o`, `--output` | Output directory (default: `./output/`) |
| `--shodan` | Enable Shodan cross-reference |
| `--no-subdomains` | Skip subdomain enumeration |
| `-v`, `--verbose` | Verbose output |
| `--format` | Output format: `json` or `html` |

---

## 🔍 Passive sources

| Source | What it provides |
|--------|-----------------|
| Target crawl | Endpoints, links, forms, parameters, JS files |
| crt.sh | Passive subdomain enumeration via certificate transparency |
| Shodan | Open ports, services, banners, known vulns (optional) |
| TLS inspection | Certificate validity, expiry, cipher suites |
| HTTP headers | Security headers, server info, tech stack hints |

---

## 🤐 Secrets detection

> Looks for the following patterns inside JavaScript files and HTML source:

- AWS Access Keys (`AKIA...`)
- Google API Keys (`AIza...`)
- JWT tokens
- Generic API keys and Bearer tokens
- Hardcoded passwords and credentials
- Internal endpoints and IP addresses

---

## ‼️Disclaimer

> **nn0nn** is built for **authorized security testing only**. Only use it against targets you have explicit permission and authorization to test. The author is not responsible for misuse.
