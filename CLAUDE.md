# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

**Spendly** is a personal expense-tracker web app (Flask + SQLite, currency ₹). It is a **teaching scaffold** — most features are intentionally unimplemented stubs that a student fills in step-by-step. Read the placeholder strings in `app.py` (e.g. `"Logout — coming in Step 3"`) and the comments in `database/db.py` as the curriculum spec: they declare what each Step is supposed to add and the function signatures expected.

Implication: when asked to "implement X," check whether X corresponds to a numbered Step and stay within that step's scope. Don't preemptively wire up later steps.

## Commands

The virtualenv is `venv-1/` (not the conventional `venv/`). Activate it before running Python/pip so packages land in the venv and not the system Python:

```powershell
# PowerShell (interactive terminal)
.\venv-1\Scripts\Activate.ps1
```

```bash
# Bash tool / Git Bash — activation only lasts one shell invocation, so chain it
source ./venv-1/Scripts/activate && <command>
```

| Task | Command |
| --- | --- |
| Install deps | `pip install -r requirements.txt` |
| Run dev server | `python app.py` → http://localhost:5001 (debug mode on) |
| Run all tests | `pytest` |
| Run a single test | `pytest path/to/test_file.py::test_name` |

There is no lint or build step.

## Architecture

Flat single-file Flask app — no blueprints, no app factory. The request flow is:

```
Browser → route in app.py → render_template("X.html")
       → templates/X.html extends base.html
       → response links static/css/style.css + static/js/main.js
```

- **`app.py`** — every route. Function names matter: templates build URLs with `url_for('<function_name>')`, so renaming a view function silently breaks links in templates. The placeholder routes (`/logout`, `/profile`, `/expenses/...`) return literal strings and exist only so `url_for` resolves — replace them when implementing the corresponding Step.
- **`database/db.py`** — currently empty except for a docstring naming the three functions to implement: `get_db()` (SQLite connection with `row_factory` and foreign keys), `init_db()` (`CREATE TABLE IF NOT EXISTS`), `seed_db()` (dev sample data). The SQLite file is `expense_tracker.db` (gitignored).
- **`templates/`** — Jinja templates. `base.html` owns the navbar, footer, font preconnects, and the global CSS/JS includes; every other page does `{% extends "base.html" %}` and fills `{% block title %}` / `{% block content %}` / `{% block scripts %}`.
- **`static/css/style.css`** — all styles, vanilla CSS. **`static/js/main.js`** — vanilla JS, currently just a placeholder comment; loaded sitewide from `base.html`.

No ORM, no auth library, no JS build step — keep new code consistent with that minimal stack unless the user explicitly asks otherwise.

## Working in this repo — gotchas

- **Bash tool on Windows strips backslashes.** `.\venv-1\Scripts\...` arrives as `.venv-1Scripts...` and fails. Use forward slashes (`./venv-1/Scripts/activate`) or the PowerShell tool when paths must use backslashes.
- **Activate the venv inside the same Bash call** that runs `pip` / `python`. Each Bash invocation is a fresh shell — a previous `source ...activate` does not persist. Without this, pip installs into the Windows Store Python's user site-packages instead of the venv.
- **`venv-1/` is not gitignored.** `.gitignore` lists `venv/`, so the actual `venv-1/` directory is tracked. Don't commit further changes inside it; if asked to fix this, prefer renaming to `venv/` or adding `venv-1/` to `.gitignore` over rewriting history.
- **Port 5001** is the dev server port (not Flask's default 5000) — set explicitly in `app.run(...)`.
