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
- `python3 cli/repo_os.py doctor`
- `python3 cli/repo_os.py explain-command-policy`
- `python3 cli/repo_os.py delete <repo-name> <repo-name>`

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
