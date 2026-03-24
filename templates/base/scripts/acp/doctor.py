#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

required_paths = [
    "AGENT.md",
    "agent/design/requirements.md",
    "agent/design/architecture.md",
    "agent/design/verification-strategy.md",
    "agent/design/repo-rules.md",
    "agent/design/source-of-truth-files.md",
    "agent/design/llm-terminal-execution-rules.md",
    "agent/commands/README.md",
    "agent/index/local.main.yaml",
    "agent/progress.yaml",
    ".github/pull_request_template.md",
    ".github/workflows/ci.yml",
    ".github/workflows/pr-body.yml",
    ".githooks/pre-push",
    "scripts/verify.sh",
    "scripts/acp/acp.sh",
    "scripts/acp/generate_pr_body.py",
    "scripts/acp/update_progress.py",
    "scripts/acp/context_tools.py",
    "scripts/acp/doctor.py",
    "scripts/check_pr_body.py",
]

failures: list[str] = []

for relative in required_paths:
    if not (ROOT / relative).exists():
        failures.append(f"missing file {relative}")

if shutil.which("git") is None:
    failures.append("git not found in PATH")

if shutil.which("python3") is None:
    failures.append("python3 not found in PATH")

hooks_path = subprocess.run(
    ["git", "config", "--get", "core.hooksPath"],
    cwd=ROOT,
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
    text=True,
).stdout.strip()

if hooks_path != ".githooks":
    failures.append("git core.hooksPath is not set to .githooks")

if not (ROOT / ".git").exists():
    failures.append("repo is not initialized as a git repository")

if failures:
    print("ACP doctor failed")
    for item in failures:
        print(f"- {item}")
    sys.exit(1)

print("ACP doctor passed")
