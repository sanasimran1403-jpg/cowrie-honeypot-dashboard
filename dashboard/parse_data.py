import json
from collections import Counter

LOG_FILE = "../var/log/cowrie/cowrie.json"

def get_dashboard_data():
    usernames = Counter()
    passwords = Counter()
    creds = Counter()
    sessions = set()
    downloads = []
    login_events = []

    with open(LOG_FILE) as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            sessions.add(entry.get("session"))
            eid = entry.get("eventid", "")

            if eid in ("cowrie.login.success", "cowrie.login.failed"):
                u = entry.get("username", "")
                p = entry.get("password", "")
                usernames[u] += 1
                passwords[p] += 1
                creds[f"{u}/{p}"] += 1
                login_events.append({
                    "timestamp": entry.get("timestamp", ""),
                    "src_ip": entry.get("src_ip", ""),
                    "username": u,
                    "password": p,
                    "success": eid == "cowrie.login.success"
                })

            if eid == "cowrie.session.file_download":
                downloads.append(entry.get("url", ""))

    return {
        "total_sessions": len(sessions),
        "top_usernames": usernames.most_common(5),
        "top_passwords": passwords.most_common(5),
        "top_combos": creds.most_common(5),
        "downloads": list(set(downloads)),
        "login_events": login_events[-20:]  # last 20
    }
