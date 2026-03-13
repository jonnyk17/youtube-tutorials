# Error Handling Patterns

## Priority: HIGH

## Description

Inconsistent error handling creates unpredictable behavior. Check that new code handles errors the same way as the rest of the codebase.

## What to Check

### API error responses
Does the project have a standard error format?
```json
// Common patterns:
{"error": "message"}
{"error": {"code": "NOT_FOUND", "message": "User not found"}}
{"errors": [{"field": "email", "message": "Invalid format"}]}
```

New endpoints should use the same format.

### Exception types
- Does the project define custom exceptions? New code should use them.
- Are errors caught at the right level? (route handler vs middleware vs service)

### Silent failures
```python
# Bad: swallowing errors
try:
    result = process(data)
except Exception:
    pass  # Silently fails

# Good: at minimum, log
try:
    result = process(data)
except ProcessingError as e:
    logger.error(f"Processing failed: {e}")
    raise
```

### Consistent status codes
- 400 for validation errors
- 401 for unauthenticated
- 403 for unauthorized
- 404 for not found
- 500 for unexpected errors

Check that new endpoints use the same codes as existing endpoints for the same situations.
