---
name: plan
description: Write a short implementation plan or spec before coding. Use when starting new work, when requirements are unclear, when a ticket needs explicit boundaries, or when a change touches multiple files or interfaces.
---

# Plan

## When to use

- Starting a new feature or meaningful change
- A Linear ticket is good, but still needs a cleaner implementation plan
- Requirements, boundaries, or success criteria are unclear
- The change touches multiple files, interfaces, config, or data flow

## Process

1. Read the ticket, product context, and relevant code before planning.
2. Restate the goal in plain English.
3. If something important is ambiguous, ask concise clarifying questions or state assumptions clearly.
4. For small or medium tasks, write a short working plan.
5. For larger multi-hour tasks, write a longer living plan instead of jumping straight into code.

## What the plan should contain

- Goal
- Context
- Scope
- Non-goals
- Proposed steps
- Risks
- Verification

## Output shape

For a short plan, keep it brief and practical.

Example:

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

For a larger task, expand the same structure into a longer living document with clearer scope, risks, and verification.

## Rules

- Keep the plan as short as the task allows.
- Do not write a greenfield design if the codebase already has patterns to follow.
- Call out schema, config, CLI, API, or file-format changes explicitly.
- Make requirements specific enough that someone can review the implementation against them.
- If the request is tiny and obvious, skip the long plan and move straight to a lightweight spec.
- If the plan starts getting long because the task is too big, split the work.
