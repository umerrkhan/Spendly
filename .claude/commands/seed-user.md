---
description: Custom slash command to create a single dummy user in the database
allowed-tools: Read, Bash(python3:*)
---

Read `database/db.py` to understand the users table schema and the `get_db()` helper.

Then, write and run a script using bash that:

1. **Generates a realistic random user** using your own knowledge of common names across regions:
   - **Name:** A realistic Indian first and last name.
   - **Email:** Derived from the name with a random 2–3 digit number suffix (e.g., `wasif.abbas54@gmail.com`).
   - **Password:** `"dummypassword"` hashed with Werkzeug's `generate_password_hash`.
   - **Created_at:** Current datetime.

2. **Checks if the generated email already exists** in the user table. If it does, regenerate the email/user until it is unique. 

3. **Inserts the user into the database** using the same `get_db()` pattern found in `db.py`.

4. **Prints a clear confirmation message** in the console once the user is successfully created (e.g., including the generated name and email).