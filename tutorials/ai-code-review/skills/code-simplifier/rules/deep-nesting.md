# Deep Nesting

## Priority: MEDIUM

## Description

Code nested more than 3 levels deep is hard to read and reason about. Most deep nesting can be eliminated with early returns, guard clauses, or extraction.

## Vulnerable

```python
def process_order(order):
    if order:
        if order.status == "pending":
            if order.items:
                if order.payment:
                    if order.payment.verified:
                        # The actual logic, 5 levels deep
                        return fulfill(order)
    return None
```

## Fixed

```python
def process_order(order):
    if not order:
        return None
    if order.status != "pending":
        return None
    if not order.items:
        return None
    if not order.payment or not order.payment.verified:
        return None

    return fulfill(order)
```

## What to Check

- Functions with more than 3 levels of indentation
- Nested if/else chains that can be flattened with early returns
- Nested loops that can be extracted into helper functions
- Try/except blocks nested inside if blocks inside loops
