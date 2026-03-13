---
name: security-reviewer
description: Scans code for security vulnerabilities including OWASP top 10, hardcoded secrets, authentication issues, and injection attacks. Use when reviewing code for security, auditing a codebase, or before deploying to production.
---

# Security Reviewer

Focused security review that checks for vulnerabilities in code changes or across the codebase.

## When to Apply

- Reviewing any code that handles user input
- Code that touches authentication or authorization
- API endpoints and route handlers
- Database queries
- File uploads or file system operations
- Code that handles secrets, tokens, or credentials
- Before deploying to production

## What It Checks

| Priority | Category | Rules |
|----------|----------|-------|
| CRITICAL | Injection | SQL injection, command injection, XSS, path traversal |
| CRITICAL | Secrets | Hardcoded API keys, passwords, tokens, connection strings |
| HIGH | Authentication | Missing auth checks, insecure session handling, weak validation |
| HIGH | Input Validation | Unsanitized user input, missing type/length checks |
| MEDIUM | Dependencies | Known CVEs in packages |
| MEDIUM | Data Exposure | Sensitive data in logs, error messages, or responses |

## How to Use

```
Review my recent changes for security issues
```

```
Audit the codebase for security vulnerabilities
```

```
Check this API endpoint for injection vulnerabilities
```

## Rules

Read individual rule files in `rules/` for detailed checks with examples.
