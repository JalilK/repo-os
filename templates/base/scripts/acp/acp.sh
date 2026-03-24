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

show_last_commit() {
  if git rev-parse --verify HEAD >/dev/null 2>&1; then
    git log -1 --oneline
  else
    echo "No commits yet"
  fi
}

case "$COMMAND" in
  init)
    python3 scripts/acp/context_tools.py init
    ;;
  start)
    FEATURE="${2:-feature}"
    MILESTONE="${3:-Feature Work}"
    TASK="${4:-Implement $FEATURE}"
    BRANCH="feat/${FEATURE// /-}"
    require_clean_worktree
    git checkout -b "$BRANCH"
    python3 scripts/acp/update_progress.py start-feature "$FEATURE" "$MILESTONE" "$TASK"
    echo "Started feature branch $BRANCH"
    echo "Updated ACP progress for feature $FEATURE"
    ;;
  status)
    echo "=== ACP STATUS ==="
    echo "Branch"
    git branch --show-current
    echo
    echo "Last commit"
    show_last_commit
    echo
    echo "Progress"
    python3 scripts/acp/update_progress.py show
    ;;
  next)
    python3 scripts/acp/context_tools.py next
    ;;
  context)
    SUB="${2:-show}"
    TARGET="${3:-init}"
    if [ "$SUB" = "show" ]; then
      python3 scripts/acp/context_tools.py show "$TARGET"
    elif [ "$SUB" = "export" ]; then
      python3 scripts/acp/context_tools.py export "$TARGET"
    else
      echo "Unknown context subcommand $SUB"
      exit 1
    fi
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
  progress)
    SUB="${2:-show}"
    shift 2 || true
    python3 scripts/acp/update_progress.py "$SUB" "$@"
    ;;
  complete)
    ./scripts/verify.sh verify
    echo "Verification passed"
    echo "Open PR or merge only if PR checks are green and manual verification is documented"
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
    echo "acp init"
    echo "acp start <feature-name> [milestone] [task]"
    echo "acp status"
    echo "acp next"
    echo "acp context show [command]"
    echo "acp context export [command]"
    echo "acp verify"
    echo "acp pr body"
    echo "acp pr create"
    echo "acp progress show"
    echo "acp progress set-milestone <value>"
    echo "acp progress set-task <value>"
    echo "acp progress add-recent-work <value>"
    echo "acp progress add-next-step <value>"
    echo "acp progress add-blocker <value>"
    echo "acp progress clear-blockers"
    echo "acp complete"
    echo 'acp command suggest "<task description>"'
    ;;
esac
