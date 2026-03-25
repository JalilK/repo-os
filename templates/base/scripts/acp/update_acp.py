#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None, capture: bool = False) -> str:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
    )
    return result.stdout.strip() if capture else ""


def fail(message: str) -> None:
    print(message)
    sys.exit(1)


def main() -> None:
    repo_root = Path.cwd()
    source_file = repo_root / "agent" / "acp-source.json"

    if not source_file.exists():
        fail(f"Missing ACP source file {source_file}")

    config = json.loads(source_file.read_text())
    repo_os_path = Path(config["repo_os_local_path"]).expanduser().resolve()
    branch = config.get("repo_os_branch", "main")
    auto_apply_overlay = bool(config.get("auto_apply_overlay", True))

    if not repo_os_path.exists():
        fail(f"repo-os path does not exist {repo_os_path}")

    if not (repo_os_path / ".git").exists():
        fail(f"repo-os path is not a git repo {repo_os_path}")

    if not (repo_os_path / "cli" / "repo_os.py").exists():
        fail(f"repo-os CLI not found at {repo_os_path / 'cli' / 'repo_os.py'}")

    print("Checking repo-os for ACP updates")
    run(["git", "fetch", "origin", branch], cwd=repo_os_path)

    local_sha = run(["git", "rev-parse", "HEAD"], cwd=repo_os_path, capture=True)
    remote_sha = run(["git", "rev-parse", f"origin/{branch}"], cwd=repo_os_path, capture=True)

    if local_sha != remote_sha:
        print("ACP update available")
        run(["git", "checkout", branch], cwd=repo_os_path)
        run(["git", "pull", "origin", branch], cwd=repo_os_path)
    else:
        print("ACP already up to date")

    repo_os_cli = repo_os_path / "cli" / "repo_os.py"

    print("Updating ACP base in current repo")
    run(["python3", str(repo_os_cli), "update-base", str(repo_root)])

    overlay_manifest = repo_root / "agent" / "overlay" / "manifest.json"
    if auto_apply_overlay and overlay_manifest.exists():
        print("Applying overlay")
        run(["python3", str(repo_os_cli), "apply-overlay", str(repo_root)])

    print("ACP update complete")


if __name__ == "__main__":
    main()
