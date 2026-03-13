# Code Duplication

## Priority: HIGH

## Description

Copy-pasted code blocks that are identical or nearly identical. Duplication makes maintenance harder because changes need to be made in multiple places.

## When to Flag

- **3+ copies** of the same logic (not 2. Two copies are often fine.)
- **Near-identical functions** that differ only in one parameter
- **Repeated patterns** across files that should be a shared utility

## When NOT to Flag

- Two similar blocks that serve different purposes and will likely diverge
- Test code that repeats setup (test clarity is worth some repetition)
- Simple one-liners repeated in different contexts

## Example

```python
# Repeated in user_router.py
async def get_user(user_id: int):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Repeated in order_router.py
async def get_order(order_id: int):
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Repeated in product_router.py
async def get_product(product_id: int):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
```

## Simplified

```python
# Shared utility
async def get_or_404(model, record_id: int):
    record = await db.get(model, record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return record
```

## What to Check

- Functions with identical structure but different model/table names
- Repeated error handling blocks
- Repeated validation logic
- Repeated API response formatting
