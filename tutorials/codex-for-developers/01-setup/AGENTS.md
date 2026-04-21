# Project Name

## What this is

One sentence describing what the project does and what it runs on.

## How to run

```bash
just dev        # start the development server
just test       # run the test suite
just check      # lint + typecheck + test
```

## Project layout

```
src/            # application source
  api/          # API layer (routes, handlers)
  services/     # business logic
  models/       # data models
tests/          # test files mirror src/ structure
```

## Conventions

- All API routes live under `src/api/`. Follow the pattern in existing routers.
- Business logic goes in `src/services/`. Routers call services, not the other way around.
- Tests go in `tests/` and mirror the source path. `src/api/users.py` -> `tests/api/test_users.py`.
- Use the existing error handling pattern. Do not introduce new exception classes without asking.
- No new dependencies without checking if the stdlib covers it first.

## What to run before committing

```bash
just check
```

All three checks must pass. Do not commit with failing tests or type errors.

## Review instructions

See `code_review.md` for how to review changes before committing.
