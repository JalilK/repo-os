#!/usr/bin/env python3
import os
import sys

body = os.environ.get("PR_BODY", "")

required_sections = [
    "## What changed",
    "## Why this change exists",
    "## Source of truth followed",
    "## Automated verification",
    "## Manual verification",
    "## Risks",
    "## ACP updates",
]

missing = [section for section in required_sections if section not in body]

if missing:
    print("Missing required PR sections")
    for section in missing:
        print(section)
    sys.exit(1)

if "- [x]" not in body and "- [X]" not in body:
    print("PR body must contain completed verification evidence")
    sys.exit(1)

print("PR body validation passed")
