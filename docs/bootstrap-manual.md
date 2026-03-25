# Bootstrap Manual

## Goal

Initialize or maintain a repository with ACP memory, repo enforcement, CI, PR controls, and a local command surface.

## Supported stack

- swift-ios

## Commands

`python3 cli/repo_os.py init swift-ios <repo-name>`
`python3 cli/repo_os.py init swift-ios <repo-name> --bootstrap`
`python3 cli/repo_os.py install-base <repo-path>`
`python3 cli/repo_os.py update-base <repo-path>`
`python3 cli/repo_os.py update-stack swift-ios <repo-path> <repo-name>`

## What gets created

- ACP files
- local ACP command wrapper
- verification scripts
- GitHub policy files
- stack template files

## Update an existing repo

Use `update-base` when ACP is already installed and you want to pull the latest repo-os base layer into an existing repo.

Use `update-stack` when you need updated stack template files rendered for a specific existing repo name.

## Delete a generated repo

`python3 cli/repo_os.py delete <repo-name> <repo-name>`

## Rule

Generated repos must always include command-first execution rules for LLM use.
