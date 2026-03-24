# Verification Strategy

## Verification model

This repo uses two verification lanes.

Fast lane runs on every pull request and is the merge gate.

Deep lane runs on demand and on schedule for slower system validation.

## Command-first rule

Use ACP and verification commands instead of ad hoc shell for recurring repo workflows.

## Fresh session recovery

Use these commands for a fresh session

- `./scripts/acp/acp.sh init`
- `./scripts/acp/acp.sh next`
- `./scripts/acp/acp.sh context show init`
- `./scripts/acp/acp.sh context export init`

## Fast lane

- lint
- build
- test
- pr-body

## Deep lane

- optional slower system validation

## Manual verification rule

For every user-visible change, the PR must document manual verification.

## Canonical local commands

- `./scripts/verify.sh verify`
- `./scripts/acp/acp.sh verify`
- `./scripts/acp/acp.sh pr body`
- `./scripts/acp/acp.sh pr create`
- `./scripts/acp/acp.sh context export init`
