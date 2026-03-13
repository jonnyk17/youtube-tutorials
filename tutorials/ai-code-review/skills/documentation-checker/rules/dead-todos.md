# Dead TODOs

## Priority: HIGH

## Description

TODO, FIXME, HACK, and XXX comments that are no longer relevant. They clutter the codebase and create false urgency.

## Patterns to Check

### TODOs for completed work
```python
# TODO: Add input validation
def create_user(request: CreateUserRequest):  # Pydantic already validates
    ...
```

### TODOs referencing closed issues
```javascript
// TODO: Fix race condition in checkout (see #234)
// Issue #234 was closed 6 months ago
```

### Permanent "temporary" code
```python
# HACK: Temporary workaround for API timeout
# (Added 2 years ago, still here)
timeout = 60
```

### Vague TODOs with no actionable next step
```python
# TODO: Make this better
# TODO: Clean up later
# TODO: Refactor
```

## What to Do

- If the TODO's work is done, remove the comment
- If the TODO references a closed issue, remove it
- If the TODO has been there for 6+ months with no progress, either create an issue for it or remove it
- If the TODO is too vague to act on, remove it
