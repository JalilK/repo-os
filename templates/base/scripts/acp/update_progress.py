#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROGRESS = ROOT / "agent" / "progress.yaml"

if not PROGRESS.exists():
    print("agent/progress.yaml not found")
    sys.exit(1)

text = PROGRESS.read_text()

def replace_scalar(content: str, key: str, value: str) -> str:
    pattern = rf'^{re.escape(key)}:\s*.*$'
    replacement = f'{key}: "{value}"'
    if re.search(pattern, content, flags=re.MULTILINE):
        return re.sub(pattern, replacement, content, flags=re.MULTILINE)
    return content.rstrip() + f'\n{replacement}\n'

def replace_mapping_value(content: str, section: str, key: str, value: str) -> str:
    pattern = rf'(^{re.escape(section)}:\n(?:  .*?\n)*)'
    match = re.search(pattern, content, flags=re.MULTILINE)
    if not match:
        block = f'{section}:\n  {key}: {value}\n'
        return content.rstrip() + "\n" + block
    block = match.group(1)
    line_pattern = rf'^  {re.escape(key)}:\s*.*$'
    new_line = f'  {key}: {value}'
    if re.search(line_pattern, block, flags=re.MULTILINE):
        new_block = re.sub(line_pattern, new_line, block, flags=re.MULTILINE)
    else:
        new_block = block + new_line + "\n"
    return content[:match.start(1)] + new_block + content[match.end(1):]

def replace_list(content: str, key: str, items: list[str]) -> str:
    pattern = rf'^{re.escape(key)}:\n(?:  - .*?\n)*'
    replacement = key + ":\n" + "".join(f'  - "{item}"\n' for item in items)
    if re.search(pattern, content, flags=re.MULTILINE):
        return re.sub(pattern, replacement, content, flags=re.MULTILINE)
    return content.rstrip() + "\n" + replacement

def add_list_item(content: str, key: str, value: str) -> str:
    pattern = rf'^{re.escape(key)}:\n((?:  - .*?\n)*)'
    match = re.search(pattern, content, flags=re.MULTILINE)
    if match:
        existing = match.group(1)
        replacement = f"{key}:\n{existing}  - \"{value}\"\n"
        return re.sub(pattern, replacement, content, flags=re.MULTILINE)
    return content.rstrip() + f'\n{key}:\n  - "{value}"\n'

def clear_list(content: str, key: str) -> str:
    pattern = rf'^{re.escape(key)}:\n(?:  - .*?\n)*'
    replacement = f"{key}: []\n"
    if re.search(pattern, content, flags=re.MULTILINE):
        return re.sub(pattern, replacement, content, flags=re.MULTILINE)
    return content.rstrip() + f'\n{key}: []\n'

cmd = sys.argv[1] if len(sys.argv) > 1 else ""

if cmd == "show":
    print(text)
    sys.exit(0)

elif cmd == "set-milestone":
    value = sys.argv[2]
    text = replace_scalar(text, "current_milestone", value)

elif cmd == "set-task":
    value = sys.argv[2]
    text = replace_scalar(text, "current_task", value)

elif cmd == "add-recent-work":
    value = sys.argv[2]
    text = add_list_item(text, "recent_work", value)

elif cmd == "add-next-step":
    value = sys.argv[2]
    text = add_list_item(text, "next_steps", value)

elif cmd == "add-blocker":
    value = sys.argv[2]
    text = add_list_item(text, "blockers", value)

elif cmd == "clear-blockers":
    text = clear_list(text, "blockers")

elif cmd == "mark-complete":
    key = sys.argv[2]
    if key.startswith("milestone_"):
        text = replace_mapping_value(text, "milestone_status", key, "complete")
    elif key.startswith("task_") or "_task_" in key:
        text = replace_mapping_value(text, "task_status", key, "complete")
    else:
        print("mark-complete expects a milestone_... or ...task... key")
        sys.exit(1)

elif cmd == "mark-in-progress":
    key = sys.argv[2]
    if key.startswith("milestone_"):
        text = replace_mapping_value(text, "milestone_status", key, "in_progress")
    elif key.startswith("task_") or "_task_" in key:
        text = replace_mapping_value(text, "task_status", key, "in_progress")
    else:
        print("mark-in-progress expects a milestone_... or ...task... key")
        sys.exit(1)

elif cmd == "start-feature":
    feature_name = sys.argv[2]
    milestone = sys.argv[3] if len(sys.argv) > 3 else "Feature Work"
    task = sys.argv[4] if len(sys.argv) > 4 else f"Implement {feature_name}"

    text = replace_scalar(text, "current_milestone", milestone)
    text = replace_scalar(text, "current_task", task)
    text = clear_list(text, "blockers")
    text = replace_list(text, "recent_work", [f"Started feature branch for {feature_name}"])
    text = replace_list(text, "next_steps", [f"Implement {feature_name}", "Run local verify", "Prepare PR from ACP state"])

else:
    print("Usage")
    print("  update_progress.py show")
    print("  update_progress.py set-milestone <value>")
    print("  update_progress.py set-task <value>")
    print("  update_progress.py add-recent-work <value>")
    print("  update_progress.py add-next-step <value>")
    print("  update_progress.py add-blocker <value>")
    print("  update_progress.py clear-blockers")
    print("  update_progress.py mark-complete <status-key>")
    print("  update_progress.py mark-in-progress <status-key>")
    print("  update_progress.py start-feature <feature-name> [milestone] [task]")
    sys.exit(1)

PROGRESS.write_text(text)
print(PROGRESS)
