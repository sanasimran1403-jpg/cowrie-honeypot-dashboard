# Cowrie Honeypot — Threat Intelligence Dashboard

A self-hosted SSH/Telnet honeypot built on [Cowrie](https://github.com/cowrie/cowrie), deployed to
capture real-world attacker behavior — brute-force login attempts, command execution, and malware
download patterns. Includes a custom Flask-based threat intelligence dashboard and an automated
PDF report generator that maps observed activity to MITRE ATT&CK techniques.

## Features
- Cowrie SSH/Telnet honeypot with iptables port redirection (22 → 2222)
- Log parsing and analysis (`analyze_logs.py`) — top usernames, passwords, credential combos
- Live Flask dashboard with terminal-style UI and matrix-rain visual theme
- Automated PDF threat report (ReportLab) with MITRE ATT&CK mapping

## MITRE ATT&CK Mapping
| Technique ID | Name | Observed Behavior |
|---|---|---|
| T1110 | Brute Force | Repeated login attempts with common credential pairs |
| T1078 | Valid Accounts | Successful fake logins using weak/default credentials |
| T1105 | Ingress Tool Transfer | wget/curl attempts to fetch external payloads |
| T1082 | System Information Discovery | Commands like `uname -a`, `cat /etc/passwd` |

## Stack
Python, Flask, Cowrie, ReportLab, iptables

## Screenshots
*(add dashboard screenshot here)*

## Disclaimer
Deployed and tested in an isolated lab environment (VirtualBox) for educational and
research purposes as part of a cybersecurity portfolio.
