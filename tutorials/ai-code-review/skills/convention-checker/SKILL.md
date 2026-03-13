---
name: convention-checker
description: Checks code against project conventions defined in CLAUDE.md, AGENTS.md, and established patterns. Enforces naming, file structure, API design, and error handling patterns. Use when reviewing code for consistency.
---

# Convention Checker

Ensures code follows established project conventions. This skill reads your CLAUDE.md, AGENTS.md, and existing patterns to verify new code is consistent.

## When to Apply

- Reviewing any code changes
- After an agent writes new code
- When adding new files, functions, or API endpoints
- Before creating a pull request

## What It Checks

| Priority | Category | Rules |
|----------|----------|-------|
| HIGH | CLAUDE.md Compliance | Explicit rules defined in project CLAUDE.md |
| HIGH | API Design | REST conventions, error response format, status codes, pagination |
| MEDIUM | Naming | Variables, functions, files, directories follow project patterns |
| MEDIUM | File Structure | Code is in the right directory, follows project organization |
| MEDIUM | Error Handling | Consistent error handling patterns, proper error types |
| LOW | Import Order | Consistent import grouping and ordering |

## How to Use

```
Check if my code follows project conventions
```

```
Does this API endpoint follow our patterns?
```

```
Review this file for naming consistency
```

## Important

This skill is only as good as your CLAUDE.md. If your project doesn't have documented conventions, start there. The skill will still check for internal consistency (does the new code match existing patterns) but explicit rules are more reliable.

## Rules

Read individual rule files in `rules/` for detailed checks with examples.
