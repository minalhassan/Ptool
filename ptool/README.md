# 🛠️ PTool - AI-Powered Penetration Testing CLI

A production-grade command-line tool that generates penetration testing and CTF commands using Google Gemini AI.

## ✨ Features

- 🤖 **AI-Powered Command Generation** - Leverage Gemini AI for intelligent command suggestions
- 🎯 **Multiple Modes** - Recon, Web, Exploit, Privilege Escalation, CTF
- 🔒 **Safe Execution** - Built-in safety checks and user confirmation
- 📋 **Command History** - Track and reuse previous commands
- 📝 **Templates** - Predefined templates for common tasks
- 🎨 **Beautiful UI** - Rich terminal output with syntax highlighting
- 📎 **Clipboard Support** - Copy commands with one flag
- 💡 **Command Explanation** - Understand what each command does

## 🚀 Installation

### Prerequisites

- Python 3.8+
- Linux (tested on Kali Linux)
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Install

```bash
# Clone the repository
git clone <repository-url>
cd ptool

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install PTool
pip install -e .
📚 Usage
#Basic Command Generation
# Generate a command for a task
ptool generate "scan open ports" --target 192.168.1.1

# With mode specification
ptool generate "find hidden directories" --target example.com --mode web

# With flags
ptool generate "enumerate subdomains" --target example.com --stealth --fast
Quick Mode Commands
Bash

# Reconnaissance
ptool recon example.com
ptool recon 192.168.1.1 --task "full port scan" --fast

# Web testing
ptool web example.com --task "find SQL injection"
ptool web https://target.com --task "directory bruteforce" --execute

# CTF mode
ptool ctf "reverse shell needed" --hints "port 4444"
ptool ctf "crack this hash: 5f4dcc3b5aa765d61d8327deb882cf99"

Command Execution
Bash

# Generate and execute
ptool generate "quick nmap scan" --target 10.10.10.1 --execute

# Execute with auto-confirm
ptool execute "nmap -sV 192.168.1.1" --yes

# Explain a command
ptool explain "nmap -sS -sV -O -p- -T4 192.168.1.1"
Templates
Bash

# List all templates
ptool templates

# List category templates
ptool templates recon

# Use a template
ptool templates --use recon:full_scan --target 192.168.1.1

# Use template with clipboard copy
ptool templates --use web:dir_bruteforce --target example.com
History
Bash

# View history
ptool history

# View last 20 commands
ptool history --limit 20

# Clear history
ptool history --clear
Advanced Usage
Bash

# Complex task with context
ptool generate "bypass WAF" \
  --target example.com \
  --mode web \
  --context "ModSecurity detected" \
  --stealth

# Copy to clipboard
ptool generate "reverse shell" --copy

# No explanation (command only)
ptool generate "find SUID binaries" --no-explain
🎯 Examples
Example 1: Network Reconnaissance
Bash

$ ptool recon 192.168.1.0/24 --task "discover live hosts"

► Generating command...

╔════════════════════════════════════════╗
║              Command                   ║
╚════════════════════════════════════════╝

nmap -sn 192.168.1.0/24 -oG - | grep "Up" | cut -d' ' -f2

╔════════════════════════════════════════╗
║           Explanation                  ║
╚════════════════════════════════════════╝

This command performs a ping scan (-sn) on the
entire /24 subnet, outputs in greppable format,
filters for live hosts, and extracts IP addresses.

Risk Level: LOW

✓ Command copied to clipboard
Example 2: Web Application Testing
Bash

$ ptool web https://example.com --task "find admin panels"

► Generating command...

╔════════════════════════════════════════╗
║              Command                   ║
╚════════════════════════════════════════╝

ffuf -u https://example.com/FUZZ \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -mc 200,301,302,403 \
  -c -v

Risk Level: LOW
Example 3: CTF Challenge
Bash

$ ptool ctf "I have a PCAP file with suspicious traffic"

► Analyzing CTF challenge...

APPROACH:
1. Open PCAP in Wireshark
2. Look for HTTP/FTP traffic (unencrypted)
3. Follow TCP streams
4. Export objects
5. Check for unusual protocols

COMMANDS:
# Open in Wireshark
wireshark capture.pcap

# Or use tshark for CLI analysis
tshark -r capture.pcap -Y "http.request"

# Extract HTTP objects
tshark -r capture.pcap --export-objects http,./output

# Look for credentials
tshark -r capture.pcap -Y "http.request.method == POST"

TOOLS:
- Wireshark
- tshark
- tcpdump
- NetworkMiner