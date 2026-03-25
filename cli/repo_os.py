#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
DESKTOP = Path.home() / "Desktop"

BASE_COPY_PATHS = [
    "AGENT.md",
    "agent",
    ".github",
    ".githooks",
    "scripts/acp",
    "scripts/check_pr_body.py",
]

BASE_EXECUTABLES = [
    ".githooks/pre-push",
    "scripts/acp/acp.sh",
    "scripts/acp/generate_pr_body.py",
    "scripts/acp/update_progress.py",
    "scripts/acp/context_tools.py",
    "scripts/acp/doctor.py",
    "scripts/check_pr_body.py",
]

def fail(message: str) -> None:
    print(message)
    sys.exit(1)

def run(cmd: list[str], cwd: Path | None = None, capture: bool = False) -> str:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
    )
    return result.stdout.strip() if capture else ""

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

def copy_tree(src: Path, dest: Path) -> None:
    if not src.exists():
        fail(f"Template path not found {src}")
    shutil.copytree(src, dest, dirs_exist_ok=True)

def copy_file(src: Path, dest: Path) -> None:
    if not src.exists():
        fail(f"Template file not found {src}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)

def ensure_executables(repo_path: Path) -> None:
    for relative in BASE_EXECUTABLES:
        target = repo_path / relative
        if target.exists():
            target.chmod(0o755)

def initialize_repo_files(stack: str, repo_name: str) -> Path:
    if stack != "swift-ios":
        fail("Supported stacks are swift-ios")

    destination = DESKTOP / repo_name
    if destination.exists():
        fail(f"Destination already exists {destination}")

    destination.mkdir(parents=True)
    copy_tree(TEMPLATES / "base", destination)
    copy_tree(TEMPLATES / "swift-ios", destination)

    rename_paths(destination, repo_name)

    for path in destination.rglob("*"):
        replace_tokens(path, repo_name)

    ensure_executables(destination)
    return destination

def bootstrap_repo_path(destination: Path) -> None:
    if not destination.exists():
        fail(f"Repo path does not exist {destination}")

    if not (destination / ".git").exists():
        run(["git", "init"], cwd=destination)

    run(["git", "config", "core.hooksPath", ".githooks"], cwd=destination)
    ensure_executables(destination)

    has_commit = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=destination,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0

    if not has_commit:
        run(["git", "add", "."], cwd=destination)
        run(["git", "commit", "-m", "Bootstrap repo from repo-os template"], cwd=destination)

def install_base_into_existing_repo(repo_path: str) -> None:
    destination = Path(repo_path).expanduser().resolve()
    if not destination.exists():
        fail(f"Repo path does not exist {destination}")
    if not (destination / ".git").exists():
        fail(f"Target is not a git repo {destination}")

    for relative in BASE_COPY_PATHS:
        src = TEMPLATES / "base" / relative
        dest = destination / relative
        if src.is_dir():
            copy_tree(src, dest)
        else:
            copy_file(src, dest)

    ensure_executables(destination)
    run(["git", "config", "core.hooksPath", ".githooks"], cwd=destination)

    print("Installed base ACP layer into existing repo")
    print(destination)
    print("Review and customize these files next")
    print("  agent/design/requirements.md")
    print("  agent/design/architecture.md")
    print("  agent/design/source-of-truth-files.md")

def update_base_in_existing_repo(repo_path: str) -> None:
    destination = Path(repo_path).expanduser().resolve()
    if not destination.exists():
        fail(f"Repo path does not exist {destination}")
    if not (destination / ".git").exists():
        fail(f"Target is not a git repo {destination}")
    if not (destination / "scripts" / "acp" / "acp.sh").exists():
        fail("ACP base does not appear to be installed in target repo")

    before = run(["git", "status", "--short"], cwd=destination, capture=True)

    for relative in BASE_COPY_PATHS:
        src = TEMPLATES / "base" / relative
        dest = destination / relative
        if src.is_dir():
            copy_tree(src, dest)
        else:
            copy_file(src, dest)

    ensure_executables(destination)
    run(["git", "config", "core.hooksPath", ".githooks"], cwd=destination)

    after = run(["git", "status", "--short"], cwd=destination, capture=True)

    print("Updated ACP base layer in existing repo")
    print(destination)
    print()
    print("Changed files")
    if after:
        print(after)
    else:
        print("No changes")
    print()
    print("Previous git status snapshot")
    print(before if before else "Clean before update")

def init_repo(stack: str, repo_name: str, bootstrap: bool = False) -> None:
    destination = initialize_repo_files(stack, repo_name)
    if bootstrap:
        bootstrap_repo_path(destination)
        print("Initialized and bootstrapped repo")
        print(destination)
        print("Next commands")
        print(f"  cd {destination}")
        print("  ./scripts/acp/acp.sh doctor")
        print("  ./scripts/acp/acp.sh init")
        print("  ./scripts/acp/acp.sh next")
    else:
        print(destination)

def bootstrap_repo(repo_path: str) -> None:
    destination = Path(repo_path).expanduser().resolve()
    bootstrap_repo_path(destination)
    print("Bootstrapped repo")
    print(destination)

def init_and_bootstrap_repo(stack: str, repo_name: str) -> None:
    init_repo(stack, repo_name, bootstrap=True)

def delete_repo(repo_name: str, confirm_name: str | None, force: bool) -> None:
    destination = (DESKTOP / repo_name).resolve()

    if destination == ROOT.resolve():
        fail("Refusing to delete repo-os itself")
    if not destination.exists():
        fail(f"Repo does not exist {destination}")
    if destination.parent != DESKTOP.resolve():
        fail("Refusing to delete paths outside Desktop")

    is_git_repo = (destination / ".git").exists()
    if not is_git_repo and not force:
        fail("Target is not a git repo. Use --force if intended")

    if confirm_name != repo_name:
        print("Delete target")
        print(destination)
        print()
        print("Re-run with exact confirmation")
        print(f"python3 cli/repo_os.py delete {repo_name} {repo_name}")
        if not is_git_repo:
            print(f"python3 cli/repo_os.py delete {repo_name} {repo_name} --force")
        sys.exit(1)

    shutil.rmtree(destination)
    print("Deleted repo")
    print(destination)

def doctor() -> None:
    print("repo-os doctor")
    print(f"templates base exists {(TEMPLATES / 'base').exists()}")
    print(f"templates swift-ios exists {(TEMPLATES / 'swift-ios').exists()}")
    print(f"cli exists {(ROOT / 'cli' / 'repo_os.py').exists()}")

def explain_command_policy() -> None:
    print("Command-first law")
    print("Use ACP commands over raw shell whenever an ACP command exists.")
    print("If a recurring repo workflow has no ACP command yet, create or extend one.")

def main() -> None:
    if len(sys.argv) < 2:
        fail("Usage repo_os.py <init|bootstrap|install-base|update-base|delete|doctor|explain-command-policy> ...")

    command = sys.argv[1]

    if command == "init":
        if len(sys.argv) not in {4, 5}:
            fail("Usage repo_os.py init <stack> <repo-name> [--bootstrap]")
        bootstrap = len(sys.argv) == 5 and sys.argv[4] == "--bootstrap"
        if len(sys.argv) == 5 and sys.argv[4] != "--bootstrap":
            fail("Usage repo_os.py init <stack> <repo-name> [--bootstrap]")
        init_repo(sys.argv[2], sys.argv[3], bootstrap=bootstrap)

    elif command == "bootstrap":
        if len(sys.argv) != 3:
            fail("Usage repo_os.py bootstrap <repo-path>")
        bootstrap_repo(sys.argv[2])

    elif command == "init-and-bootstrap":
        if len(sys.argv) != 4:
            fail("Usage repo_os.py init-and-bootstrap <stack> <repo-name>")
        print("Deprecated")
        print("Use repo_os.py init <stack> <repo-name> --bootstrap")
        init_and_bootstrap_repo(sys.argv[2], sys.argv[3])

    elif command == "install-base":
        if len(sys.argv) != 3:
            fail("Usage repo_os.py install-base <repo-path>")
        install_base_into_existing_repo(sys.argv[2])

    elif command == "update-base":
        if len(sys.argv) != 3:
            fail("Usage repo_os.py update-base <repo-path>")
        update_base_in_existing_repo(sys.argv[2])

    elif command == "delete":
        if len(sys.argv) not in {3, 4, 5}:
            fail("Usage repo_os.py delete <repo-name> [confirm-name] [--force]")
        repo_name = sys.argv[2]
        confirm_name = None
        force = False
        for arg in sys.argv[3:]:
            if arg == "--force":
                force = True
            else:
                confirm_name = arg
        delete_repo(repo_name, confirm_name, force)

    elif command == "doctor":
        doctor()

    elif command == "explain-command-policy":
        explain_command_policy()

    else:
        fail("Unknown command")

if __name__ == "__main__":
    main()
