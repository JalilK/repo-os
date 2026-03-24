# Repo Agent Rules

## Repo operating model

This repo uses ACP as a repo operating system.

The repo itself is the primary source of truth for

- requirements
- architecture
- verification
- repo policy
- progress
- next task

## Terminal execution law

This repo uses ACP as the preferred execution surface.

Before emitting terminal code, first look for an ACP command that covers the task.

If the task is a recurring repo workflow and no ACP command exists yet, create or extend the ACP command surface instead of repeating raw shell.

Use raw shell only for one-off operations, deep debugging, or bootstrap steps below the ACP abstraction layer.

## Fresh session law

At the start of a fresh session, use these commands first

- `./scripts/acp/acp.sh doctor`
- `./scripts/acp/acp.sh init`
- `./scripts/acp/acp.sh next`
- `./scripts/acp/acp.sh context export init`

Do not begin implementation before recovering current repo context.

## Existing repo migration law

When applying this ACP system to an existing repo, use the repo-os install command instead of manually copying files.
