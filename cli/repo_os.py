#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"

def fail(message: str) -> None:
    print(message)
    sys.exit(1)

def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)

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

def initialize_repo_files(stack: str, repo_name: str) -> Path:
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

    return destination

def bootstrap_repo_path(destination: Path) -> None:
    if not destination.exists():
        fail(f"Repo path does not exist: {destination}")

    if not (destination / ".git").exists():
        run(["git", "init"], cwd=destination)

    run(["git", "config", "core.hooksPath", ".githooks"], cwd=destination)

    for relative in [
        ".githooks/pre-push",
        "scripts/acp/acp.sh",
        "scripts/acp/generate_pr_body.py",
        "scripts/check_pr_body.py",
    ]:
        target = destination / relative
        if target.exists():
            target.chmod(0o755)

    has_commit = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=destination,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0

    if not has_commit:
        run(["git", "add", "."], cwd=destination)
        run(["git", "commit", "-m", "Bootstrap repo from repo-os template"], cwd=destination)

def init_repo(stack: str, repo_name: str) -> None:
    destination = initialize_repo_files(stack, repo_name)
    print(destination)

def bootstrap_repo(repo_path: str) -> None:
    destination = Path(repo_path).expanduser().resolve()
    bootstrap_repo_path(destination)
    print("Bootstrapped repo:")
    print(destination)
    print("Next commands:")
    print("  ./scripts/acp/acp.sh status")
    print('  ./scripts/acp/acp.sh command suggest "describe your next task"')

def init_and_bootstrap_repo(stack: str, repo_name: str) -> None:
    destination = initialize_repo_files(stack, repo_name)
    bootstrap_repo_path(destination)
    print("Initialized and bootstrapped repo:")
    print(destination)
    print("Next commands:")
    print("  cd " + str(destination))
    print("  ./scripts/acp/acp.sh status")
    print('  ./scripts/acp/acp.sh command suggest "describe your next task"')

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
        fail("Usage: repo_os.py <init|bootstrap|init-and-bootstrap|doctor|explain-command-policy> ...")

    command = sys.argv[1]

    if command == "init":
        if len(sys.argv) != 4:
            fail("Usage: repo_os.py init <stack> <repo-name>")
        init_repo(sys.argv[2], sys.argv[3])
    elif command == "bootstrap":
        if len(sys.argv) != 3:
            fail("Usage: repo_os.py bootstrap <repo-path>")
        bootstrap_repo(sys.argv[2])
    elif command == "init-and-bootstrap":
        if len(sys.argv) != 4:
            fail("Usage: repo_os.py init-and-bootstrap <stack> <repo-name>")
        init_and_bootstrap_repo(sys.argv[2], sys.argv[3])
    elif command == "doctor":
        doctor()
    elif command == "explain-command-policy":
        explain_command_policy()
    else:
        fail("Unknown command")

if __name__ == "__main__":
    main()
