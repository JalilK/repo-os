# Command Surface

## Local ACP entrypoint

- `./scripts/acp/acp.sh start <feature-name>`
- `./scripts/acp/acp.sh status`
- `./scripts/acp/acp.sh verify`
- `./scripts/acp/acp.sh pr body`
- `./scripts/acp/acp.sh pr create`
- `./scripts/acp/acp.sh complete`
- `./scripts/acp/acp.sh command suggest "<task description>"`

## Command meanings

@acp.status

- report current progress state

@acp.validate

- run local verification

@acp.pr.prepare

- generate a completed PR body from ACP state

## Enforcement rules

- pre-push hook runs verification
- `acp pr create` runs verification before PR creation
- recurring repo workflows should become ACP commands
