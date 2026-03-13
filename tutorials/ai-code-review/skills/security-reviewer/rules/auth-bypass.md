# Authentication and Authorization Bypass

## Priority: HIGH

## Description

Missing or improperly implemented auth checks allow unauthorized access to protected resources. This includes missing middleware, broken access control, and insecure session handling.

## Vulnerable

```python
# FastAPI: endpoint without auth dependency
@app.get("/api/admin/users")
async def list_users():
    return await db.get_all_users()

# Checking user role client-side only
@app.delete("/api/posts/{post_id}")
async def delete_post(post_id: int, current_user: User = Depends(get_current_user)):
    # Missing: check if current_user owns this post
    await db.delete_post(post_id)
```

```javascript
// Next.js: API route without auth check
export async function GET(request) {
  const users = await db.users.findMany();
  return Response.json(users);
}

// Checking permissions only in the UI
{isAdmin && <DeleteButton />}  // But the API endpoint has no check
```

## Fixed

```python
@app.get("/api/admin/users")
async def list_users(current_user: User = Depends(get_current_admin)):
    return await db.get_all_users()

@app.delete("/api/posts/{post_id}")
async def delete_post(post_id: int, current_user: User = Depends(get_current_user)):
    post = await db.get_post(post_id)
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    await db.delete_post(post_id)
```

```javascript
export async function GET(request) {
  const session = await auth();
  if (!session?.user?.role === "admin") {
    return Response.json({ error: "Unauthorized" }, { status: 403 });
  }
  const users = await db.users.findMany();
  return Response.json(users);
}
```

## What to Check

- API endpoints (GET, POST, PUT, DELETE) without auth middleware or dependency
- Delete/update operations without ownership checks (IDOR)
- Admin routes without role verification
- Auth checks that only exist in the frontend (UI hides button but API is open)
- Session tokens without expiration
- Password reset flows without proper token validation
