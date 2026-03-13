---
name: documentation-checker
description: Finds documentation rot including stale comments, outdated README sections, dead TODOs, and missing documentation for public APIs. Use periodically to keep docs honest.
---

# Documentation Checker

Finds documentation that has drifted from the code. Stale docs are worse than no docs because they actively mislead.

## When to Apply

- Periodically (weekly or monthly)
- After major refactors
- When onboarding new team members reveals confusion
- Before releases

## What It Checks

| Priority | Category | Rules |
|----------|----------|-------|
| HIGH | Stale Comments | Comments that describe code that no longer exists or behaves differently |
| HIGH | Dead TODOs | TODO/FIXME/HACK comments older than 3 months or referencing completed work |
| MEDIUM | README Drift | README instructions that don't match current setup, commands, or structure |
| MEDIUM | Missing Docs | Public functions, APIs, or modules with no documentation |
| LOW | Changelog | CHANGELOG not updated for recent changes |

## How to Use

```
Check for outdated documentation across the project
```

```
Find stale comments that don't match the code
```

```
Are there any dead TODOs that should be resolved?
```

## Philosophy

Good documentation is accurate documentation. A comment that says "this function validates email" when it actually validates phone numbers is worse than no comment at all. Flag inaccuracy aggressively. Flag missing docs only for public APIs and complex logic.

## Rules

Read individual rule files in `rules/` for detailed checks with examples.
