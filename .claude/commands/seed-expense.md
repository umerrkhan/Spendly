---
description: Seed realistic dummy expenses for a specific user
argument-hint: "<user_id> <count> <months>"
allowed-tools: Read, Bash(python3:*)
---

Read `database/db.py` to understand the expenses table schema, the database connection pattern, and how the database filename/path is configured.

User input: $ARGUMENTS

## Step 1 — Parse arguments

Extract from $ARGUMENTS:
- `user_id` — integer
- `count` — integer (number of expenses to create)
- `months` — integer (how many past months to spread them across)

If any argument is missing or not a valid integer, stop and say exactly:
"Usage: /seed-expenses <user_id> <count> <months>"

## Step 2 — Verify user exists

Before generating anything, confirm that the `user_id` exists in the users table. If it does not, stop and say exactly:
"No user found with id <user_id>."

## Step 3 — Generate and insert expenses

Write and run a Python script that:

1. **Spreads expenses randomly** across the past `<months>` months relative to the current date.
2. **Uses these specific categories** with realistic Indian context descriptions and amounts (in ₹):
   - **Food:** 50–800 (Most common category)
   - **Transport:** 20–500
   - **Bills:** 200–3000
   - **Shopping:** 200–5000
   - **Other:** 50–1000
   - **Entertainment:** 100–1500 (Least common category)
   - **Health:** 100–2000 (Least common category)
3. **Distributes categories proportionally**, ensuring Food is the most frequent and Health/Entertainment are the least frequent.
4. **Imports or dynamically extracts** the database connection/filename configuration from `db.py` rather than hardcoding it.
5. **Uses parameterized queries exclusively** to prevent SQL injection (no string formatting/f-strings in SQL statements).
6. **Executes inserts within a single transaction**, ensuring a complete rollback if any single insertion fails.

## Step 4 — Confirm

Upon successful insertion, print a summary containing:
- The total number of expenses successfully inserted.
- The date range they span (Min Date to Max Date).
- A sample table or list of 5 of the inserted records.