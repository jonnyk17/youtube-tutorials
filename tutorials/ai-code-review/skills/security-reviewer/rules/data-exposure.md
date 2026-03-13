# Sensitive Data Exposure

## Priority: MEDIUM

## Description

Sensitive data leaked through error messages, logs, API responses, or debug output. Includes passwords, tokens, PII, and internal system details.

## Vulnerable

```python
# Logging sensitive data
logger.info(f"User login: {email}, password: {password}")
logger.error(f"DB connection failed: {DATABASE_URL}")

# Returning internal errors to client
@app.exception_handler(Exception)
async def handle_error(request, exc):
    return JSONResponse({"error": str(exc), "traceback": traceback.format_exc()})

# Returning full user object including password hash
@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    return await db.get_user(user_id)  # Includes password_hash, ssn, etc.
```

## Fixed

```python
# Log without sensitive fields
logger.info(f"User login: {email}")
logger.error("DB connection failed")

# Generic error for clients, detailed error in logs
@app.exception_handler(Exception)
async def handle_error(request, exc):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse({"error": "Internal server error"}, status_code=500)

# Return only the fields the client needs
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    return await db.get_user(user_id)
```

## What to Check

- Logger calls that include passwords, tokens, or connection strings
- Error responses that expose stack traces, SQL queries, or internal paths
- API responses that return full database objects without filtering fields
- Debug mode enabled in production configs
- Sensitive data in URL query parameters (logged by web servers)
- PII (email, phone, address) in logs without masking
