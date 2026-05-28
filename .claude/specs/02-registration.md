# Spec: Registration

## Overview
This feature turns the existing `/register` page into a working sign-up flow. Right now `templates/register.html` already renders a POST form (name, email, password), but the `/register` route in `app.py` only handles GET and ignores submitted data. Step 2 adds POST handling to that route: it validates the submitted fields, hashes the password with werkzeug, inserts a new row into the `users` table created in Step 1, and redirects the new user to the login page. It exists at this point in the Spendly roadmap because every later feature (login/logout, profile, expense tracking) needs real user accounts in the database, and registration is the only way to create them outside of the seeded demo user.

## Depends on
- **Step 1 — Database Setup** (`01-database-setup.md`). Requires `get_db()`, `init_db()`, and the `users` table (`id`, `name`, `email` UNIQUE, `password_hash`, `created_at`) to be implemented and working.

## Routes
- `GET /register` — render the registration form (already exists; keep behaviour). — public
- `POST /register` — validate submitted name/email/password, create the user, redirect to `/login` on success or re-render with an error on failure. — public

No brand-new URL paths are introduced — the existing `/register` route is extended to also accept `POST`.

## Database changes
No database changes. The `users` table from Step 1 already has every column registration needs (`name`, `email` with a UNIQUE constraint, `password_hash`, `created_at` with a default). Verified against `database/db.py`.

## Templates
- **Create:** none.
- **Modify:** `templates/register.html` — no structural change required. It already posts to `/register`, shows `{{ error }}` when present, and links to login. Only touch it if you need to surface a success/flash message or preserve the entered name/email on validation error (optional, see Rules).

## Files to create
None. All work happens in existing files (`app.py`).

## New dependencies
No new dependencies. `werkzeug.security` (for `generate_password_hash`) and Flask's `request`, `redirect`, `url_for` are already available in the stack.

## Rules for implementation
- No SQLAlchemy or ORMs — use `sqlite3` via `get_db()`.
- Parameterised queries only — never use string formatting / f-strings to build SQL.
- Passwords hashed with werkzeug (`generate_password_hash`) — never store the plaintext password.
- Use CSS variables — never hardcode hex values (only relevant if `register.html` styling is touched).
- All templates extend `base.html`.
- Update the `/register` route to accept both methods: `@app.route("/register", methods=["GET", "POST"])`.
- Read form fields with `request.form` and strip whitespace from `name` and `email`; lowercase the email before storing/checking.
- Validate server-side before inserting: all three fields required; password minimum length 8 characters (matches the form's "Min. 8 characters" hint).
- Handle duplicate email gracefully — check for the existing email and/or catch `sqlite3.IntegrityError` from the UNIQUE constraint, then re-render `register.html` with a human-readable `error` rather than letting the app 500.
- On validation/duplicate failure, re-render `register.html` with an `error` message (HTTP 200) — do not redirect.
- On success, redirect to `url_for('login')` (do not auto-log-in — sessions arrive in Step 3).
- Always `conn.close()` the connection (use try/finally or a context manager) and `commit()` after insert.

## Definition of done
- `python app.py` starts with no errors and `GET http://localhost:5001/register` shows the form.
- Submitting the form with a new, valid name + email + password (≥8 chars) inserts exactly one row into `users` (verifiable: the email appears in the DB with a non-plaintext `password_hash`) and redirects to `/login`.
- Submitting with the seeded email `demo@spendly.com` (or any already-registered email) re-renders the register page with a visible error message and does **not** create a duplicate row or raise a 500.
- Submitting with a missing field or a password shorter than 8 characters re-renders the register page with a visible error and creates no row.
- The stored `password_hash` is a werkzeug hash (starts with `pbkdf2:` or `scrypt:`), never the raw password.
- No SQL in the route is built with string formatting — all queries use `?` placeholders.
