# Step 1 — Database Setup: Implementation Plan

## Context
`database/db.py` is currently a docstring-only stub. This step establishes the SQLite data layer that every later curriculum step (auth, profile, expense CRUD) depends on. We implement three functions in `database/db.py`, create a two-table schema (`users`, `expenses`), and wire `app.py` to build + seed the DB once on startup inside `app.app_context()`. CLAUDE.md fixes the DB filename as `expense_tracker.db` (gitignored), so we use that rather than `spendly.db`.

## Files to Modify
- `database/db.py` — replace the stub with `get_db`, `init_db`, `seed_db`.
- `app.py` — import the three functions and call `init_db()` + `seed_db()` inside `app.app_context()` on startup.

## Files to Create
None.

## Implementation

### `database/db.py`

Module-level setup:
```python
import sqlite3
from datetime import date
from pathlib import Path
from werkzeug.security import generate_password_hash

DB_PATH = Path(__file__).resolve().parent.parent / "expense_tracker.db"
```

**`get_db()`**
- `conn = sqlite3.connect(DB_PATH)`
- `conn.row_factory = sqlite3.Row`
- `conn.execute("PRAGMA foreign_keys = ON;")`
- return `conn`
- Caller is responsible for closing the connection (use `with conn:` or explicit `conn.close()`). No `g`-based caching in this step — added later when routes actually need it.

**`init_db()`**
- Open a connection via `get_db()`.
- Execute two `CREATE TABLE IF NOT EXISTS` statements (idempotent — safe to call repeatedly):
  - `users`: `id INTEGER PRIMARY KEY AUTOINCREMENT`, `name TEXT NOT NULL`, `email TEXT UNIQUE NOT NULL`, `password_hash TEXT NOT NULL`, `created_at TEXT DEFAULT (datetime('now'))`.
  - `expenses`: `id INTEGER PRIMARY KEY AUTOINCREMENT`, `user_id INTEGER NOT NULL REFERENCES users(id)`, `amount REAL NOT NULL`, `category TEXT NOT NULL`, `date TEXT NOT NULL`, `description TEXT`, `created_at TEXT DEFAULT (datetime('now'))`.
- `conn.commit()`, then close.

**`seed_db()`**
- Open a connection.
- `SELECT COUNT(*) FROM users` — if `> 0`, close and return (no duplication).
- Insert the demo user with a parameterized `INSERT`:
  - name: `"Demo User"`, email: `"demo@spendly.com"`, password_hash: `generate_password_hash("demo123")`.
- Capture `cursor.lastrowid` as `user_id`.
- Build 8 sample expense rows covering all 7 categories (Food, Transport, Bills, Health, Entertainment, Shopping, Other) — one per category plus one repeat (e.g. a second Food row). Dates spread across the current month, computed as `date.today().replace(day=N).isoformat()` for varied `N` values (clamp `N` to ≤ 28 so the seed never overflows month length).
- `cursor.executemany("INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)", rows)`.
- `conn.commit()`, then close.

### `app.py`

Add the import alongside the existing Flask import:
```python
from database.db import get_db, init_db, seed_db
```

After `app = Flask(__name__)` and before the route definitions, add:
```python
with app.app_context():
    init_db()
    seed_db()
```

`get_db` is imported now so later steps can use it without re-touching `app.py`.

## Rules Compliance Checklist
- No ORM — raw `sqlite3` only.
- Every SQL value passed via `?` placeholders; no f-strings / `%`-formatting in SQL.
- `PRAGMA foreign_keys = ON;` set inside `get_db()` so it applies to every connection.
- `amount` stored as `REAL`.
- Passwords hashed via `werkzeug.security.generate_password_hash`.
- Categories drawn from the fixed 7-item list.

## Verification

1. Remove any stale DB (none currently exists): `Remove-Item expense_tracker.db -ErrorAction SilentlyContinue`.
2. Activate venv and start the server:
   ```powershell
   .\venv-1\Scripts\Activate.ps1
   python app.py
   ```
   Expect: no exceptions; landing page renders at http://localhost:5001.
3. In a second shell (venv active), confirm seed data and schema:
   ```powershell
   python -c "from database.db import get_db; c=get_db(); print(list(c.execute('SELECT name,email FROM users'))); print(c.execute('SELECT COUNT(*) FROM expenses').fetchone()[0])"
   ```
   Expect: one `Demo User / demo@spendly.com` row and `8`.
4. Verify idempotency — stop and re-run `python app.py`, then re-run the query above. Counts must stay at 1 user / 8 expenses (proves `seed_db()` early-return works and `init_db()` is safe to re-run).
5. Verify FK enforcement is live on a fresh connection:
   ```powershell
   python -c "from database.db import get_db; c=get_db(); print(c.execute('PRAGMA foreign_keys').fetchone()[0])"
   ```
   Expect: `1`.
6. Verify category coverage:
   ```powershell
   python -c "from database.db import get_db; c=get_db(); print(sorted({r[0] for r in c.execute('SELECT DISTINCT category FROM expenses')}))"
   ```
   Expect all 7 categories present.
