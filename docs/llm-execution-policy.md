# LLM Execution Policy

## Command-first law

When terminal actions are needed, the LLM must prefer ACP commands over raw shell whenever an ACP command exists for that task.

## Raw shell allowed only when

- bootstrapping ACP itself
- installing system dependencies before ACP exists
- one-time debugging
- highly specific low-reuse tasks

## Dynamic command rule

If the task is repeated, workflow-critical, or likely to recur, the LLM should create or extend an ACP command instead of repeating raw shell.
