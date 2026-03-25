# repo-os

repo-os is a reusable bootstrap system for repositories that need ACP style project memory, command-first execution, verification discipline, PR enforcement, and repeatable repo lifecycle tooling.

## Core idea

Every generated repo should include

- ACP project memory
- repo policy enforcement
- CI verification
- pull request enforcement
- a local ACP CLI
- command-first LLM execution rules

## Primary commands

- `python3 cli/repo_os.py init swift-ios <repo-name>`
- `python3 cli/repo_os.py init-and-bootstrap swift-ios <repo-name>`
- `python3 cli/repo_os.py install-base <repo-path>`
- `python3 cli/repo_os.py update-base <repo-path>`
- `python3 cli/repo_os.py doctor`
- `python3 cli/repo_os.py explain-command-policy`
- `python3 cli/repo_os.py delete <repo-name> <repo-name>`

## Generated repo ACP commands

- `./scripts/acp/acp.sh doctor`
- `./scripts/acp/acp.sh init`
- `./scripts/acp/acp.sh start <feature-name> [milestone] [task]`
- `./scripts/acp/acp.sh status`
- `./scripts/acp/acp.sh next`
- `./scripts/acp/acp.sh context show [command]`
- `./scripts/acp/acp.sh context export [command]`
- `./scripts/acp/acp.sh verify`
- `./scripts/acp/acp.sh pr body`
- `./scripts/acp/acp.sh pr create`
- `./scripts/acp/acp.sh progress show`
- `./scripts/acp/acp.sh progress set-milestone <value>`
- `./scripts/acp/acp.sh progress set-task <value>`
- `./scripts/acp/acp.sh progress add-recent-work <value>`
- `./scripts/acp/acp.sh progress add-next-step <value>`
- `./scripts/acp/acp.sh progress add-blocker <value>`
- `./scripts/acp/acp.sh progress clear-blockers`
- `./scripts/acp/acp.sh progress mark-complete <status-key>`
- `./scripts/acp/acp.sh progress mark-in-progress <status-key>`
- `./scripts/acp/acp.sh complete`

## Output

Generated repos receive

- ACP folder structure
- design and verification docs
- local ACP command wrapper
- CI workflows
- PR template
- CODEOWNERS
- verification scripts
- command-first execution rules
