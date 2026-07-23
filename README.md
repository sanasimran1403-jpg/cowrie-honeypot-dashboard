Honeypot Threat Intelligence Dashboard

A self-hosted SSH/Telnet honeypot built on Cowrie, deployed to capture real-world attacker behavior across multiple analysis layers: live credential-attack logging, a Flask-based real-time threat dashboard, and a full dark-themed PDF report with MITRE ATT&CK mapping and S&S branding.

Overview

SSH brute-forcing remains one of the most common automated attack vectors against internet-facing servers. This project demonstrates the full detection-to-reporting pipeline a SOC analyst would build around a deception sensor:

    Deploy a Cowrie honeypot simulating a vulnerable Linux server over SSH/Telnet
    Redirect real SSH traffic (port 22) to the honeypot via iptables NAT rules
    Capture attacker sessions — login attempts, executed commands, file download behavior
    Parse and aggregate captured logs into structured threat statistics
    Visualize findings in a live terminal-styled dashboard
    Report everything in a professional dark-themed PDF with MITRE ATT&CK mapping

All attack sessions were captured end-to-end against live simulated SSH traffic, not just synthetic examples.

Environment:

    Platform: Ubuntu 24.04 (VirtualBox) + Python 3.12
    Target: Self-hosted Cowrie SSH/Telnet sensor
    Tools: iptables, Flask, ReportLab

Feature Coverage — 4/4
# 	Feature 	Technique 	Result
1 	Honeypot Deployment 	Cowrie SSH/Telnet emulation + iptables redirect (22→2222) 	Live sensor accepting real traffic
2 	Session Capture 	JSON event logging — logins, commands, downloads, TTY replay 	Full attacker session reconstruction
3 	Log Analysis 	Python aggregation — top usernames, passwords, credential combos 	Structured threat statistics
4 	Reporting 	Flask dashboard + ReportLab PDF with MITRE ATT&CK mapping 	Portfolio-ready threat report
Setup

cd dashboard
python3 -m venv ../cowrie-env
source ../cowrie-env/bin/activate
pip install flask reportlab

Usage

# Run the live dashboard
python3 app.py
# then open http://<host-ip>:5000

# Generate the PDF threat report
python3 generate_report.py

1. Honeypot Deployment

Command:

sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222
cowrie start

Deployment logic: real sshd is moved off port 22, and iptables NAT redirects all inbound port 22 traffic to Cowrie's listener on 2222 — so the honeypot transparently receives all SSH connection attempts.

Result: Sensor live and accepting connections, fingerprinted as a standard Debian SSH server.
2. Session Capture

Command:

# Captured automatically for every connection
tail -f var/log/cowrie/cowrie.json

Detection logic: every session — login attempt (success/failure), each interactive command, and any file download — is logged as structured JSON, plus a full TTY recording for session replay via `playlog`.

Result:

Sessions Logged   : 19
Login Attempts    : 19 (multiple successful fake logins)
Commands Captured : whoami, uname -a, cat /etc/passwd, wget <payload>
File Downloads     : 1 payload fetch attempt

3. Log Analysis Engine

Aggregation across 4 dimensions:
Category 	Metric 	Example Signal
Usernames 	Frequency count 	root, admin, ubuntu, test, user
Passwords 	Frequency count 	root123, 123456, password, toor
Credential Combos 	Username/password pairing 	root/root123, ubuntu/123456
Payloads 	Download URL tracking 	wget/curl fetch attempts

Result:

Top Username     : root (5 attempts)
Top Password     : root123 (5 attempts)
Top Combo        : root/root123, ubuntu/123456
Unique Usernames : 5

4. Threat Reporting

Command:

python3 generate_report.py
# outputs dashboard/honeypot_report.pdf

Reporting logic: aggregated statistics are rendered into both a live Flask dashboard (matrix-rain themed, glass-panel UI) and a static PDF report mapping observed behavior to MITRE ATT&CK techniques.

Result:

Report Generated : honeypot_report.pdf
MITRE Techniques  : T1110, T1078, T1105, T1082
Dashboard         : Live at :5000, real-time session table

Repository Structure

cowrie-honeypot-dashboard/
├── README.md
├── .gitignore
├── analyze_logs.py           # standalone log analysis script
└── dashboard/
    ├── app.py                # Flask application
    ├── parse_data.py         # log parsing + aggregation logic
    ├── generate_report.py    # ReportLab PDF report generator
    ├── sample_log.json       # sanitized sample of captured sessions
    ├── logo.png
    ├── honeypot_report.pdf
    └── templates/
        └── dashboard.html    # matrix-rain themed dashboard UI

Tech Stack
Tool 	Version 	Purpose
Python 	3.12 	Core language
Cowrie 	3.0.6 	SSH/Telnet honeypot engine
Flask 	3.1 	Live dashboard web server
ReportLab 	latest 	Dark-themed PDF reports
iptables 	— 	Traffic redirection (NAT)
Twisted 	26.4 	Cowrie's underlying async framework
Key Learnings

    Deploying and hardening a Cowrie honeypot sensor, including transparent port redirection via iptables NAT
    Understanding attacker reconnaissance patterns — common credential pairs, post-login enumeration commands, payload staging behavior
    Mapping observed telemetry to the MITRE ATT&CK framework (T1110, T1078, T1105, T1082) for structured threat classification
    Building a live Flask dashboard with a custom terminal-styled, glassmorphism UI over raw JSON telemetry
    Generating professional dark-themed PDF reports with ReportLab — watermarks, evidence tables, production-quality output

Known Limitations

    Currently deployed on an isolated home network (VirtualBox NAT) — attacker traffic was simulated rather than sourced from live internet-wide scanning
    Session data reflects a limited capture window rather than long-term production telemetry
    Credential/command detection is log-based only — no active response or automated IP blocking is implemented
    Dashboard has no authentication layer — not intended for public-facing deployment as-is

Author

Sana Simran GitHub: @sanasimran1403-jpg

    Disclaimer: This honeypot was deployed and tested in an isolated lab environment for educational and authorized security research purposes only. Never deploy deception infrastructure on networks or systems you do not own or have explicit permission to monitor.
