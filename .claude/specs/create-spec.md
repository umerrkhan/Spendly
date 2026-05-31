---
description: create a spec file and feature branch for the next spendly step
argument-hint: "Step number and feature name e.g 2 Registration"
allowed-tools: Read, write, Glob, Bash(git:*)
---

You are a senior developer spinning up a new feature for the spendly expense tracker. Always
follow the rules in CLAUDE.md.

User input: $ARGUMENTS


## Step 1 - Check working directory is clean
Run `git status` and check for the uncommitted, unstaged, or untracked files. if any exists, stop immediately and tell the user to commit or stash changes before proceeding.
DO NOT CONTINUE until the working directory is clean. 

## Step 2 - Parse the arguments
From $ARGUMENTS extract:
1. `step number` - zero-padded to digits: 2 → 03, 11 → 11

2. `feature_title` - human readable title in Title case
- Example "Registration" or "Login and Logout"

3. `feature_slug` - git and file safe slug
-Lowercase, kebab-case
-Maximum 40 Characters
-Example: registration, login-logout

4. `branch_name` - format: `feature/<feature_slug>`
	-Example:  `feature/registration`

if you cannot infer these from $ARGUMENTS, ask the user to clarify before proceeding

## Step 3 - check branch name is not taken
Run `git branch` to list existing branches.
if `branch_name` is already taken, append a number: `feature/registration-01` or `feature/registration-02` etc.

## Step 4 - Switch to main and pull latest
Run:
```
git checkout main
git pull origin main
```

## Step 5 - create or Switch to feature branch
Run:
```
git checkout -b <branch_name>
```

## Step 6 - Research the codebase
Read these files before wriiting the spec:
- `CLAUDE.md`  - roadmap, conventions, schema
- `app.py`  - existing routes and structure 
- `database/db.py`  - avoid duplicating existing specs

check `CLAUDE.md` to confirm the requested step is not already marked complete. if it is, warn the user and stop.

## Step 7 -- Write the spec
Generate a spec document with this exact structure:

---

# Spec: <feature_title>

## Overview
One paragraph describing what this feature does and why it existts at this stage of the spendly roadmap.

## Depends on 
Which previous steps this features required to complete.

## Routes 
Every new route needed:
- `METHOD /path` - description - access level (public/loggen-in)

If no new routes: state "No new routes".

## Database changes
Any new tables, columns, or constraints needed.
Always verify against `database/db.py` before writing this.
If none: state "No database changes".

## Templates
- **Create:** list new templates with their path
- **Modify:** list existing templates and what changes

## Files to change
Every file that will be modified.

## New dependencies
Any new pip packages. If none: state "No new dependencies".

## Rules for implementation
Specific constraints Claude must follow. Always include:
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`

## Definition of done

A specific testable checklist. Each item must be something that can be verified by running the app.

---

## Step 8 — Save the spec
Save to: `.claude/specs/<step_number>-<feature_slug>.md`

## Step 9 — Report to the user
Print a short summary in this exact format:
```
Branch:    <branch_name>
Spec file: .claude/specs/<step_number>-<feature_slug>.md
Title:     <feature_title>
```
Then tell the user:
"Review the spec at `.claude/specs/<step_number>-<feature_slug>.md`
then enter Plan Mode with Shift+Tab twice to begin implementation."

Do not print the full spec in chat unless explicitly asked.