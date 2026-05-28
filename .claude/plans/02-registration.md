# Implementation Plan — Step 2: Registration

All changes are confined to **`app.py`**. No new files, no DB changes, no template changes required.

## 1. Update imports (`app.py`, line 1)
Current:
```python
from flask import Flask, render_template
```
Add `request`, `redirect`, `url_for`:
```python
from flask import Flask, render_template, request, redirect, url_for
```
Also import the hasher and sqlite3 at the top:
```python
import sqlite3
from werkzeug.security import generate_password_hash
```
(`get_db` is already imported on line 3 — reuse it.)

## 2. Rewrite the `/register` route (currently lines 21–23)
Change the decorator to accept both methods and split the logic by `request.method`:

```
@app.route("/register", methods=["GET", "POST"])
def register():
    # GET → render the empty form (unchanged behaviour)
    # POST → validate, hash, insert, redirect/re-render
```

**POST branch flow:**

1. **Read & normalise input**
   - `name = request.form.get("name", "").strip()`
   - `email = request.form.get("email", "").strip().lower()`
   - `password = request.form.get("password", "")` (no strip — passwords can legitimately contain spaces)

2. **Server-side validation** (re-render `register.html` with an `error` string + HTTP 200 on any failure; preserve `name`/`email` back into the template so the user doesn't retype):
   - All three fields non-empty → else `error = "All fields are required."`
   - `len(password) >= 8` → else `error = "Password must be at least 8 characters."`
   - (Optional, low cost) basic `@` presence check on email.

3. **Insert with duplicate handling** — open `get_db()`, wrap in `try/finally` so the connection always closes:
   - Hash: `password_hash = generate_password_hash(password)`
   - Parameterised insert: `INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)` with `(name, email, password_hash)`.
   - `conn.commit()`
   - Catch `sqlite3.IntegrityError` (UNIQUE email violation) → re-render with `error = "An account with that email already exists."` and no duplicate row.

4. **On success** → `return redirect(url_for("login"))` (no auto-login; sessions are Step 3).

## 3. Template (`templates/register.html`) — minor optional touch
- It already renders `{{ error }}` (lines 16–18), so the error path works with zero edits.
- **Optional improvement** to satisfy "preserve entered values": add `value="{{ name or '' }}"` to the name input and `value="{{ email or '' }}"` to the email input, and pass `name`/`email` into `render_template` on the error path. Password field is intentionally left blank.

## Decision points / notes
- **Duplicate-email strategy:** rely on catching `sqlite3.IntegrityError` (atomic, race-free) rather than a pre-`SELECT`. This is the cleaner approach; a pre-check `SELECT` is redundant.
- **No flash messaging** is introduced — the spec keeps success as a plain redirect to `/login`. A "registered successfully" banner would require either sessions/flash (Step 3 territory) or a query param, so it's deliberately out of scope.

## Verification (matches spec "Definition of done")
1. `python app.py` → `GET /register` shows form.
2. Register a fresh email (password ≥8) → redirects to `/login`; verify one new row in `users` with a `pbkdf2:`/`scrypt:` hash.
3. Register `demo@spendly.com` → error shown, no 500, no duplicate row.
4. Submit missing field / 7-char password → error shown, no row created.
