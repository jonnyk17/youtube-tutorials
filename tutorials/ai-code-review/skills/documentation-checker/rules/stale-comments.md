# Stale Comments

## Priority: HIGH

## Description

Comments that describe code that no longer exists or behaves differently than described. These actively mislead anyone reading the code.

## Patterns to Check

### Comment describes deleted logic
```python
# Validates email format and checks against blocklist
def validate_email(email: str) -> bool:
    return "@" in email  # Blocklist check was removed months ago
```

### Comment describes different behavior
```javascript
// Returns null if user not found
async function getUser(id) {
  const user = await db.users.findUnique({ where: { id } });
  if (!user) throw new NotFoundError("User not found");  // Throws, doesn't return null
  return user;
}
```

### Comment references renamed variables or functions
```python
# Calls process_payment() to handle the transaction
def handle_order(order):
    charge_customer(order)  # Function was renamed but comment wasn't updated
```

## What to Check

- Read the comment, then read the code below it. Do they match?
- Look for function/variable names in comments that don't exist in the current code
- Look for behavioral descriptions (returns, throws, modifies) that don't match
- Look for "temporary" or "workaround" comments on permanent-looking code
