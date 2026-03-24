#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[2]
progress_path = root / "agent" / "progress.yaml"
output_path = root / ".git" / "ACP_PR_BODY.md"

if not progress_path.exists():
    print("agent/progress.yaml not found")
    sys.exit(1)

progress = progress_path.read_text()

def extract(key: str, default: str) -> str:
    pattern = rf'^{re.escape(key)}:\s*"?(.*?)"?$'
    match = re.search(pattern, progress, flags=re.MULTILINE)
    return match.group(1) if match else default

current_milestone = extract("current_milestone", "Unknown milestone")
current_task = extract("current_task", "Unknown task")

body = f"""## What changed

Implemented work for {current_milestone} and {current_task}.

## Why this change exists

This change advances the active ACP task.

## Source of truth followed

- AGENT.md
- agent/design/requirements.md
- agent/design/architecture.md
- agent/design/verification-strategy.md
- agent/design/repo-rules.md
- agent/design/source-of-truth-files.md

## Automated verification

- [x] `./scripts/verify.sh verify`

## Manual verification

- [ ] Verified manually on the primary path
- [ ] Verified primary failure path
- [ ] Verified no obvious adjacent regression

## Risks

Describe real risks if any.

## ACP updates

- [x] `agent/progress.yaml` updated
- [x] ACP docs updated if repo reality changed
"""
output_path.write_text(body)
print(output_path)
