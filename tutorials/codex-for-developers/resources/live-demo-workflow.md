# Live Demo Workflow

Use this when you want to show Codex in a real engineering workflow.

## The demo shape

1. Open the product context
2. Pull the ticket from Linear
3. Create a branch from the ticket ID
4. Restate the goal in plain English
5. Write a short plan
6. Implement the change
7. Run tests
8. Run a review pass
9. Commit with the ticket ID
10. Push or open a PR

## The key line to say

> Linear is the source of truth for the work. The branch is the scope. The plan is the intent. Tests and review are the quality gate.

## What to show on screen

- the product spec
- the Linear ticket
- the branch name
- the short plan
- the implementation diff
- the test run
- the review pass
- the commit message

## Why this is a strong workflow

- the task scope is clear
- the work is isolated
- the implementation is deliberate
- the output is reviewable

## Ticket format that works well

```text
Goal
Context
Proposed shape / scope
Acceptance criteria
Constraints
Out of scope
```

Useful constraints section:

```text
Constraints
- Keep this minimal.
- Preserve the existing CLI workflow.
- Do not add UI or API work outside this ticket.
- Prefer boring local patterns over abstractions.
```

## Example lightweight plan

```md
# GRA-141 Plan

Goal: persist scraped jobs into Postgres while keeping CSV export.

Steps:
1. Add DB configuration and connection setup.
2. Define minimal `jobs` table.
3. Implement job upsert logic.
4. Wire scraper CLI to persist jobs.
5. Keep CSV export optional.
6. Add tests for upsert and rerun behavior.
7. Run review and cleanup.
```

## Suggested narration

- "We start from the ticket because the ticket is the scope."
- "We open a branch so the work is isolated."
- "We make a short plan so implementation is deliberate."
- "Then we let Codex implement against that plan."
- "Then we verify with tests and a review pass."
- "Only then do we commit."
