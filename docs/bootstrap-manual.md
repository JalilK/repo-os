# Bootstrap Manual

## Goal

Initialize a new repository with ACP memory, repo enforcement, CI, PR controls, and a local command surface.

## Supported stack

- swift-ios

## Commands

`python3 cli/repo_os.py init swift-ios <repo-name>`
`python3 cli/repo_os.py init-and-bootstrap swift-ios <repo-name>`
`python3 cli/repo_os.py install-base <repo-path>`

## What gets created

- ACP files
- local ACP command wrapper
- verification scripts
- GitHub policy files
- stack template files

## Delete a generated repo

`python3 cli/repo_os.py delete <repo-name> <repo-name>`

## Rule

Generated repos must always include command-first execution rules for LLM use.
Existing repos should receive the ACP layer through `install-base` instead of manual copying.
