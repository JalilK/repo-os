#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"

def fail(message: str) -> None:
    print(message)
    sys.exit(1)

def replace_tokens(path: Path, repo_name: str) -> None:
    if path.is_dir():
        return

    try:
        text = path.read_text()
    except UnicodeDecodeError:
        return

    bundle_id = f"com.example.{repo_name}"
    text = text.replace("APPNAME", repo_name)
    text = text.replace("BUNDLE_ID", bundle_id)
    text = text.replace("OWNER_HANDLE", "OWNER_HANDLE")
    path.write_text(text)

def rename_paths(root: Path, repo_name: str) -> None:
    for path in sorted(root.rglob("*APPNAME*"), reverse=True):
        new_name = path.name.replace("APPNAME", repo_name)
        path.rename(path.with_name(new_name))

def copy_template(src: Path, dest: Path) -> None:
    if not src.exists():
        fail(f"Template not found: {src}")
    shutil.copytree(src, dest, dirs_exist_ok=True)

def init_repo(stack: str, repo_name: str) -> None:
    if stack != "swift-ios":
        fail("Supported stacks: swift-ios")

    destination = Path.home() / "Desktop" / repo_name
    if destination.exists():
        fail(f"Destination already exists: {destination}")

    destination.mkdir(parents=True)

    copy_template(TEMPLATES / "base", destination)
    copy_template(TEMPLATES / "swift-ios", destination)

    rename_paths(destination, repo_name)

    for path in destination.rglob("*"):
        replace_tokens(path, repo_name)

    for relative in [
        ".githooks/pre-push",
        "scripts/acp/acp.sh",
        "scripts/acp/generate_pr_body.py",
        "scripts/check_pr_body.py",
    ]:
        target = destination / relative
        if target.exists():
            target.chmod(0o755)

    print(destination)

def doctor() -> None:
    print("repo-os doctor")
    print(f"templates base exists: {(TEMPLATES / 'base').exists()}")
    print(f"templates swift-ios exists: {(TEMPLATES / 'swift-ios').exists()}")

def explain_command_policy() -> None:
    print("Command-first law")
    print("Use ACP commands over raw shell whenever an ACP command exists.")
    print("If a recurring repo workflow has no ACP command yet, create or extend one.")

def main() -> None:
    if len(sys.argv) < 2:
        fail("Usage: repo_os.py <init|doctor|explain-command-policy> ...")

    command = sys.argv[1]

    if command == "init":
        if len(sys.argv) != 4:
            fail("Usage: repo_os.py init <stack> <repo-name>")
        init_repo(sys.argv[2], sys.argv[3])
    elif command == "doctor":
        doctor()
    elif command == "explain-command-policy":
        explain_command_policy()
    else:
        fail("Unknown command")

if __name__ == "__main__":
    main()
