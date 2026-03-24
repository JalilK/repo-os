# Bootstrap Manual

## Goal

Initialize a new repository with ACP memory, repo enforcement, CI, PR controls, and a local command surface.

## Supported stack

- swift-ios

## Command

`python3 cli/repo_os.py init swift-ios <repo-name>`
`python3 cli/repo_os.py init-and-bootstrap swift-ios <repo-name>`

## What gets created

- ACP files
- local ACP command wrapper
- verification scripts
- GitHub policy files
- stack template files

## Rule

Generated repos must always include command-first execution rules for LLM use.
