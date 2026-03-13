# SQL Injection

## Priority: CRITICAL

## Description

SQL injection occurs when user input is concatenated directly into SQL queries. Attackers can modify the query to read, modify, or delete data.

## Vulnerable

```python
# String concatenation in SQL
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# String formatting in SQL
query = "SELECT * FROM users WHERE name = '%s'" % username
cursor.execute(query)
```

```javascript
// Template literals in SQL
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);
```

## Fixed

```python
# Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# SQLAlchemy
stmt = select(User).where(User.id == user_id)
```

```javascript
// Parameterized query
db.query("SELECT * FROM users WHERE id = $1", [userId]);
```

## What to Check

- Any string concatenation or f-string inside a SQL query
- Any `.execute()`, `.query()`, or `.raw()` call with interpolated variables
- ORM `.raw()` or `.execute()` calls that bypass the query builder
- Dynamic table or column names from user input
