#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROGRESS = ROOT / "agent" / "progress.yaml"

if not PROGRESS.exists():
    print("agent/progress.yaml not found")
    sys.exit(1)

text = PROGRESS.read_text()

def replace_scalar(key: str, value: str) -> str:
    import re
    pattern = rf'^{key}:\s*.*$'
    replacement = f'{key}: "{value}"'
    if re.search(pattern, text, flags=re.MULTILINE):
        return re.sub(pattern, replacement, text, flags=re.MULTILINE)
    return text + f'\n{replacement}\n'

def add_list_item(section: str, value: str) -> str:
    marker = f"{section}:\n"
    if marker not in text:
        return text + f"\n{section}:\n  - \"{value}\"\n"
    idx = text.index(marker) + len(marker)
    return text[:idx] + f'  - "{value}"\n' + text[idx:]

def clear_blockers() -> str:
    import re
    pattern = r"^blockers:.*?$"
    if re.search(pattern, text, flags=re.MULTILINE):
        return re.sub(pattern, "blockers: []", text, flags=re.MULTILINE)
    return text + "\nblockers: []\n"

cmd = sys.argv[1] if len(sys.argv) > 1 else ""
arg = sys.argv[2] if len(sys.argv) > 2 else ""

if cmd == "show":
    print(text)
    sys.exit(0)

if cmd == "set-milestone":
    text = replace_scalar("current_milestone", arg)
elif cmd == "set-task":
    text = replace_scalar("current_task", arg)
elif cmd == "add-recent-work":
    text = add_list_item("recent_work", arg)
elif cmd == "add-next-step":
    text = add_list_item("next_steps", arg)
elif cmd == "add-blocker":
    text = add_list_item("blockers", arg)
elif cmd == "clear-blockers":
    text = clear_blockers()
else:
    print("Usage")
    print("  update_progress.py show")
    print("  update_progress.py set-milestone <value>")
    print("  update_progress.py set-task <value>")
    print("  update_progress.py add-recent-work <value>")
    print("  update_progress.py add-next-step <value>")
    print("  update_progress.py add-blocker <value>")
    print("  update_progress.py clear-blockers")
    sys.exit(1)

PROGRESS.write_text(text)
print(PROGRESS)
