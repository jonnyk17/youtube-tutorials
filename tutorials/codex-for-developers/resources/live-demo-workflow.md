# Live Demo Workflow

Use this when you want to show Codex in a real engineering workflow.

## The demo shape

### Step 1: plan

Pull `GRA-141` from Linear and use the work-plan skill to create a lightweight implementation plan.

Restate the ticket in plain English, identify scope and non-goals, and produce a short plan that is appropriate for one focused implementation session.

Do not code yet.

Then review the plan on screen and tweak it if needed.

### Step 2: execute

Now implement `GRA-141` against the approved plan.

Create or switch to a Git branch for `GRA-141` if needed, make the code changes, run the relevant tests, run the review skill, and summarize the result.

Keep scope tight:

- minimal Postgres persistence for scraped jobs
- jobs table only
- upsert/dedupe behavior
- CSV export still works
- no API/UI/enrichment work

## The key line to say

> Linear is the source of truth for the work. The branch is the scope. The plan is the intent. Tests and review are the quality gate.

## What to show on screen

- the product spec
- the Linear ticket
- the short plan
- the plan review and tweaks
- the branch name
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
- "We make a short plan so implementation is deliberate."
- "We review the plan before we write code."
- "Then we open a branch so the work is isolated."
- "Then we let Codex implement against that plan."
- "Then we verify with tests and a review pass."
- "Only then do we commit."
