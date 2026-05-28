---
description: Seed realistic dummy expenses for a specific user
argument-hint: "<user_id> <count> <months>"
allowed-tools: Read, Bash(python3:*)
---

Read database/db.py to understand the expenses table schema, the db connection pattern, and the database file name.

User input: $ARGUMENTS

## Step 1 — Parse arguments

Extract from $ARGUMENTS:
- user_id — integer
- count — integer, number of expenses to create
- months — integer, how many past months to spread them across

If any argument is missing or not a valid integer, stop and say:
"Usage: /seed-expenses <user_id> <count> <months>"