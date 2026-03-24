# Repo Rules

## Branch and merge law

- No direct pushes to main
- All code reaches main through pull requests only
- Main must be protected
- Required status checks must pass before merge
- Required PR body must be complete
- Manual verification must be documented for user-visible changes

## ACP command enforcement

- Use `./scripts/acp/acp.sh` as the local ACP execution surface
- Pre-push verification is mandatory through `.githooks/pre-push`
- `acp pr create` must run local verification before opening a PR
- PR body must be generated from ACP state, not written ad hoc
- If a recurring repo workflow has no ACP command yet, add one
- Fresh sessions should use `acp init` and `acp context export` before implementation work
- LLM work should prefer ACP context export over ad hoc file guessing
