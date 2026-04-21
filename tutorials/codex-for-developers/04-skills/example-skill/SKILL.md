---
name: commit
description: Stage changes, write a conventional commit message, and push to the current branch.
---

# Commit

Stage all changes, write a conventional commit message based on the diff, and push.

## Steps

1. Run `git diff --staged` and `git diff` to understand what changed.
2. Write a commit message following the conventional commits format:
   `type(scope): short description`
   Types: feat, fix, refactor, test, docs, chore
3. Run the project's check command before committing:
   ```bash
   just check
   ```
4. If checks pass, commit and push:
   ```bash
   git add -A
   git commit -m "<message>"
   git push
   ```
5. If checks fail, report what failed. Do not commit.

## Rules

- Never use `--no-verify`.
- Never commit if tests or type checks are failing.
- Keep the subject line under 72 characters.
- Do not add "Co-authored-by" or tool attribution lines.
