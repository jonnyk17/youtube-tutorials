# Input Validation

## Priority: HIGH

## Description

Missing or insufficient validation of user input allows malformed, oversized, or malicious data into the system. Every piece of user input should be validated at the system boundary.

## Vulnerable

```python
# No validation on request body
@app.post("/api/users")
async def create_user(request: Request):
    data = await request.json()
    user = User(name=data["name"], email=data["email"])
    # No type checking, length limits, or format validation

# Trusting client-side IDs
@app.get("/api/invoices/{invoice_id}")
async def get_invoice(invoice_id: str):
    # No validation that invoice_id is a valid format
    return await db.get_invoice(invoice_id)
```

```javascript
// No validation on API input
export async function POST(request) {
  const { email, amount } = await request.json();
  // amount could be negative, email could be anything
  await processPayment(email, amount);
}
```

## Fixed

```python
from pydantic import BaseModel, EmailStr, Field

class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr

@app.post("/api/users")
async def create_user(request: CreateUserRequest):
    user = User(name=request.name, email=request.email)
```

```javascript
import { z } from "zod";

const PaymentSchema = z.object({
  email: z.string().email(),
  amount: z.number().positive().max(10000),
});

export async function POST(request) {
  const result = PaymentSchema.safeParse(await request.json());
  if (!result.success) {
    return Response.json({ error: result.error }, { status: 400 });
  }
  await processPayment(result.data.email, result.data.amount);
}
```

## What to Check

- API endpoints that read request body without schema validation
- Missing length limits on string inputs
- Numeric inputs without range checks (negative amounts, zero quantities)
- Email, URL, or phone inputs without format validation
- File uploads without type/size restrictions
- Path parameters used directly without format validation
- Missing Pydantic models (Python) or Zod schemas (TypeScript) on request handlers
