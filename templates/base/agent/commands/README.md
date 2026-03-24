# Command Surface

## Local ACP entrypoint

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
- `./scripts/acp/acp.sh complete`
- `./scripts/acp/acp.sh command suggest "<task description>"`

## Command meanings

@acp.init

- load indexed repo context for a fresh session
- show current progress state

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
- progress changes should use ACP progress commands instead of manual YAML edits when possible
- `acp start` should update progress state automatically
- `acp context export` should be used when an LLM needs a current context pack
