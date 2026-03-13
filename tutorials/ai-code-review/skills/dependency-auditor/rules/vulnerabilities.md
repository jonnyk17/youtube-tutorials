# Known Vulnerabilities

## Priority: CRITICAL

## Description

Dependencies with known security vulnerabilities (CVEs) that have published fixes.

## How to Check

Run the package manager's built-in audit:

```bash
# Node.js
npm audit --json
bun pm audit

# Python
pip-audit
safety check
```

## What to Flag

- Any dependency with a CRITICAL or HIGH severity CVE
- Dependencies where a patched version is available
- Transitive dependencies with known vulnerabilities

## What NOT to Flag

- Vulnerabilities that only affect server-side code in a client-only package (or vice versa)
- Vulnerabilities with no available fix yet (note them but don't alarm)
- Dev dependencies with vulnerabilities (lower priority, but still note)
