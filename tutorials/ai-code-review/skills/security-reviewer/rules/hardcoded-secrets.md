# Hardcoded Secrets

## Priority: CRITICAL

## Description

API keys, passwords, tokens, and connection strings embedded directly in source code. These get committed to version control and exposed to anyone with repo access.

## Vulnerable

```python
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgresql://admin:password123@prod-db.example.com/mydb"
SECRET_KEY = "my-super-secret-key-do-not-share"

headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
```

```javascript
const STRIPE_KEY = "sk_live_1234567890";
const client = new S3Client({ credentials: { accessKeyId: "AKIA...", secretAccessKey: "..." } });
```

## Fixed

```python
import os

API_KEY = os.environ["API_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]
```

```javascript
const STRIPE_KEY = process.env.STRIPE_SECRET_KEY;
```

## What to Check

- Variables named `key`, `secret`, `token`, `password`, `credential`, `auth`
- Strings that look like API keys (prefixed with `sk_`, `pk_`, `AKIA`, `ghp_`, `xoxb-`)
- Connection strings with embedded credentials
- Base64-encoded JWT tokens
- `.env` files committed to version control (check .gitignore)
- Hardcoded values in config files that should use environment variables
