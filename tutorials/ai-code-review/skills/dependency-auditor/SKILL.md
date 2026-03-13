---
name: dependency-auditor
description: Audits project dependencies for outdated packages, known vulnerabilities, unused dependencies, and duplicates. Use periodically or before releases to keep dependencies healthy.
---

# Dependency Auditor

Checks the health of your project's dependency tree. Finds security vulnerabilities, outdated packages, unused dependencies, and duplicates.

## When to Apply

- Periodically (weekly or before releases)
- After adding new dependencies
- When investigating build size or performance issues
- During security audits
- Before deploying to production

## What It Checks

| Priority | Category | Rules |
|----------|----------|-------|
| CRITICAL | Vulnerabilities | Known CVEs via npm audit, pip audit, or equivalent |
| HIGH | Outdated | Major version behind, unmaintained packages (no updates in 12+ months) |
| MEDIUM | Unused | Dependencies in package.json/pyproject.toml not imported anywhere |
| MEDIUM | Duplicates | Two packages doing the same thing (e.g., axios and fetch wrapper, moment and dayjs) |
| LOW | Size | Unusually large dependencies for what they provide |

## How to Use

```
Audit my project dependencies for security issues
```

```
Find unused dependencies in this project
```

```
Are any of my dependencies outdated or unmaintained?
```

## Rules

Read individual rule files in `rules/` for detailed checks with examples.
