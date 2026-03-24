#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

COMMAND="${1:-help}"

require_clean_worktree() {
  if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "Working tree is not clean"
    git status --short
    exit 1
  fi
}

case "$COMMAND" in
  start)
    FEATURE="${2:-feature}"
    BRANCH="feat/${FEATURE// /-}"
    require_clean_worktree
    git checkout -b "$BRANCH"
    echo "Started feature branch $BRANCH"
    ;;
  status)
    echo "=== ACP STATUS ==="
    echo "Branch"
    git branch --show-current
    echo
    echo "Last commit"
    git log -1 --oneline
    echo
    echo "Progress"
    cat agent/progress.yaml
    ;;
  verify)
    ./scripts/verify.sh verify
    ;;
  pr)
    SUB="${2:-create}"
    if [ "$SUB" = "body" ]; then
      PR_BODY_FILE="$(python3 scripts/acp/generate_pr_body.py)"
      cat "$PR_BODY_FILE"
    elif [ "$SUB" = "create" ]; then
      ./scripts/verify.sh verify
      PR_BODY_FILE="$(python3 scripts/acp/generate_pr_body.py)"
      gh pr create --fill --body-file "$PR_BODY_FILE"
    else
      echo "Unknown pr subcommand $SUB"
      exit 1
    fi
    ;;
  complete)
    ./scripts/verify.sh verify
    echo "Verification passed"
    ;;
  command)
    SUB="${2:-}"
    if [ "$SUB" = "suggest" ]; then
      shift 2
      TASK="$*"
      echo "Task description"
      echo "$TASK"
      echo
      echo "Decision rule"
      echo "If this task is recurring, workflow-critical, or likely to recur, create or extend an ACP command."
      echo "Otherwise use raw shell."
    else
      echo "Unknown command subcommand"
      exit 1
    fi
    ;;
  help|*)
    echo "Commands"
    echo "acp start <feature-name>"
    echo "acp status"
    echo "acp verify"
    echo "acp pr body"
    echo "acp pr create"
    echo "acp complete"
    echo 'acp command suggest "<task description>"'
    ;;
esac
