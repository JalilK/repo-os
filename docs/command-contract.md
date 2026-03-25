# Command Contract

## repo-os commands

- `repo-os init <stack> <repo-name>`
- `repo-os init <stack> <repo-name> --bootstrap`
- `repo-os install-base <repo-path>`
- `repo-os update-base <repo-path>`
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

## generated repo verification commands

- `verify.sh lint`
- `verify.sh build`
- `verify.sh test`
- `verify.sh verify`

## canonical command law

If two commands do the same job, document one canonical command and treat the other as compatibility only.
