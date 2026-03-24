# Command First Execution Pattern

Before giving shell commands, ask

Does this task belong to the long-term workflow of the repo

If yes, it should probably become an ACP command.

## Good fit for a new ACP command

- repeated across features
- part of repo hygiene
- part of verification
- part of PR preparation
- part of release readiness
- part of state tracking

## Bad fit for a new ACP command

- rare
- investigatory
- temporary debugging
- deeply tool-specific one-offs
