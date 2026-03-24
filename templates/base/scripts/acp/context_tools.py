#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = ROOT / "agent" / "index" / "local.main.yaml"
PROGRESS_PATH = ROOT / "agent" / "progress.yaml"
OUTPUT_PATH = ROOT / ".git" / "ACP_CONTEXT.txt"

def fail(message: str) -> None:
    print(message)
    sys.exit(1)

def parse_index() -> list[dict[str, object]]:
    if not INDEX_PATH.exists():
        fail("agent/index/local.main.yaml not found")

    entries: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    in_applies = False

    for raw_line in INDEX_PATH.read_text().splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("indexed_files:"):
            continue

        if stripped.startswith("- path:"):
            if current:
                entries.append(current)
            current = {
                "path": stripped.split(":", 1)[1].strip(),
                "weight": 0.0,
                "kind": "",
                "description": "",
                "rationale": "",
                "applies": [],
            }
            in_applies = False
            continue

        if current is None:
            continue

        if stripped.startswith("weight:"):
            current["weight"] = float(stripped.split(":", 1)[1].strip())
            in_applies = False
        elif stripped.startswith("kind:"):
            current["kind"] = stripped.split(":", 1)[1].strip()
            in_applies = False
        elif stripped.startswith("description:"):
            current["description"] = stripped.split(":", 1)[1].strip()
            in_applies = False
        elif stripped.startswith("rationale:"):
            current["rationale"] = stripped.split(":", 1)[1].strip()
            in_applies = False
        elif stripped.startswith("applies:"):
            in_applies = True
        elif in_applies and stripped.startswith("- "):
            applies = current.get("applies", [])
            assert isinstance(applies, list)
            applies.append(stripped[2:].strip())
            current["applies"] = applies

    if current:
        entries.append(current)

    return entries

def select_entries(command_name: str) -> list[dict[str, object]]:
    entries = parse_index()
    applicable = []
    for entry in entries:
        applies = entry.get("applies", [])
        if isinstance(applies, list) and command_name in applies:
            applicable.append(entry)
    applicable.sort(key=lambda item: float(item.get("weight", 0.0)), reverse=True)
    return applicable

def read_progress() -> str:
    if not PROGRESS_PATH.exists():
        return "agent/progress.yaml not found"
    return PROGRESS_PATH.read_text()

def show_context(command_name: str) -> None:
    entries = select_entries(command_name)
    if not entries:
        print(f"No indexed files apply to command {command_name}")
        return

    print(f"ACP context for command {command_name}")
    print()
    for entry in entries:
        print(f"path: {entry['path']}")
        print(f"weight: {entry['weight']}")
        print(f"kind: {entry['kind']}")
        print(f"description: {entry['description']}")
        print(f"rationale: {entry['rationale']}")
        print()

def export_context(command_name: str) -> None:
    entries = select_entries(command_name)

    chunks: list[str] = []
    chunks.append(f"# ACP Context Export\n")
    chunks.append(f"## Command\n{command_name}\n")
    chunks.append("## Progress\n")
    chunks.append(read_progress().rstrip() + "\n")

    for entry in entries:
        rel_path = str(entry["path"])
        file_path = ROOT / rel_path
        chunks.append(f"\n## Indexed File\n")
        chunks.append(f"path: {rel_path}\n")
        chunks.append(f"weight: {entry['weight']}\n")
        chunks.append(f"kind: {entry['kind']}\n")
        chunks.append(f"description: {entry['description']}\n")
        chunks.append(f"rationale: {entry['rationale']}\n")
        if file_path.exists() and file_path.is_file():
            chunks.append("\n```text\n")
            chunks.append(file_path.read_text())
            if not chunks[-1].endswith("\n"):
                chunks.append("\n")
            chunks.append("```\n")
        else:
            chunks.append("\nMissing file\n")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("".join(chunks))
    print(OUTPUT_PATH)

def show_next() -> None:
    progress = read_progress()
    current_milestone = "Unknown"
    current_task = "Unknown"
    next_steps: list[str] = []

    for line in progress.splitlines():
        stripped = line.strip()
        if stripped.startswith("current_milestone:"):
            current_milestone = stripped.split(":", 1)[1].strip().strip('"')
        elif stripped.startswith("current_task:"):
            current_task = stripped.split(":", 1)[1].strip().strip('"')
        elif stripped.startswith("- "):
            next_steps.append(stripped[2:].strip().strip('"'))

    print("Current milestone")
    print(current_milestone)
    print()
    print("Current task")
    print(current_task)
    print()
    print("Next steps")
    if next_steps:
        for step in next_steps[:5]:
            print(f"- {step}")
    else:
        print("- No next steps recorded")

def main() -> None:
    if len(sys.argv) < 2:
        fail("Usage: context_tools.py <init|show|export|next> [command-name]")

    action = sys.argv[1]
    command_name = sys.argv[2] if len(sys.argv) > 2 else "init"

    if action == "init":
        print("ACP init context")
        print()
        show_context("init")
        print("Current progress")
        print()
        print(read_progress())
    elif action == "show":
        show_context(command_name)
    elif action == "export":
        export_context(command_name)
    elif action == "next":
        show_next()
    else:
        fail("Unknown action")

if __name__ == "__main__":
    main()
