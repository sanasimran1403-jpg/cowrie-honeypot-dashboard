import json
from collections import Counter

log_file = "var/log/cowrie/cowrie.json"

usernames = Counter()
passwords = Counter()
creds = Counter()
commands = Counter()
sessions = set()
downloads = []

with open(log_file) as f:
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

        if eid == "cowrie.command.input":
            commands[entry.get("input", "")] += 1

        if eid == "cowrie.session.file_download":
            downloads.append(entry.get("url", ""))

print(f"Total unique sessions: {len(sessions)}\n")

print("Top attempted usernames:")
for u, c in usernames.most_common(5):
    print(f"  {u}: {c}")

print("\nTop attempted passwords:")
for p, c in passwords.most_common(5):
    print(f"  {p}: {c}")

print("\nTop username/password combos:")
for combo, c in creds.most_common(5):
    print(f"  {combo}: {c}")

print("\nTop commands executed:")
for cmd, c in commands.most_common(10):
    print(f"  {cmd}: {c}")

print(f"\nFile download attempts: {len(downloads)}")
for url in set(downloads):
    print(f"  {url}")
