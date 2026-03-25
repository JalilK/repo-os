# Command Contract

## repo-os commands

- `repo-os init <stack> <repo-name>`
- `repo-os init-and-bootstrap <stack> <repo-name>`
- `repo-os install-base <repo-path>`
- `repo-os doctor`
- `repo-os explain-command-policy`
- `repo-os delete <repo-name> <repo-name>`

## generated repo commands

- `acp doctor`
- `acp init`
- `acp start <feature-name> [milestone] [task]`
- `acp status`
- `acp next`
- `acp context show [command]`
- `acp context export [command]`
- `acp verify`
- `acp pr body`
- `acp pr create`
- `acp progress show`
- `acp progress set-milestone <value>`
- `acp progress set-task <value>`
- `acp progress add-recent-work <value>`
- `acp progress add-next-step <value>`
- `acp progress add-blocker <value>`
- `acp progress clear-blockers`
- `acp progress mark-complete <status-key>`
- `acp progress mark-in-progress <status-key>`
- `acp complete`

## command-first law

If a recurring repo workflow can be represented as an ACP command, use or create the ACP command.
If ACP is being applied to an existing repo, use `repo-os install-base`.
