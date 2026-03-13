# Naming Conventions

## Priority: MEDIUM

## Description

Inconsistent naming makes code harder to navigate. Check that new code matches the project's established patterns.

## What to Check

### Function and method naming
- Is the project using camelCase or snake_case for functions?
- New code should match. Don't mix styles.

### File naming
- Are files named in kebab-case, camelCase, PascalCase, or snake_case?
- Do component files match the component name? (`UserProfile.tsx` exports `UserProfile`)

### Variable naming
- Are booleans prefixed with `is`, `has`, `should`, `can`?
- Are arrays/lists pluralized? (`users` not `userList`)
- Are constants in UPPER_SNAKE_CASE?

### API routes
- What pattern does the project use? (`/api/v1/users` vs `/users` vs `/api/users`)
- Are routes plural or singular? (`/users` vs `/user`)
- Do query params use camelCase or snake_case?

## How to Check

Read 3-5 existing files in the same directory as the changed file. If the new code uses a different naming pattern, flag it. Always cite the existing pattern as evidence.
