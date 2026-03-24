# LLM Terminal Execution Rules

## Core law

When terminal actions are needed, the LLM must prefer ACP commands over raw shell whenever an ACP command exists for that task.

## Required execution order

1. Check whether an ACP command already exists for the task
2. If it exists, use the ACP command
3. If it does not exist, decide whether the task deserves a new ACP command
4. Only emit raw terminal code when the task is one-off, low reuse, or too narrow for a stable command
5. If the task is repeated, workflow-critical, or likely to recur, create or extend the ACP command surface

## Command-first rule

Use ACP commands for these classes of tasks whenever possible

- starting feature work
- checking project status
- running repo verification
- generating PR bodies
- creating PRs
- completion checks
- updating progress state

## Raw shell allowed only when

- bootstrapping ACP itself
- installing system dependencies before ACP exists
- performing a one-time investigation
- debugging below the ACP abstraction layer

## Dynamic command creation rule

If a task has any of the following traits, prefer creating or extending an ACP command

- likely to recur
- part of the normal repo workflow
- required for correctness
- useful across features
- needed by future LLM sessions
