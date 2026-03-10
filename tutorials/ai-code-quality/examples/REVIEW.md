# Code Review Guidelines

## Always flag
- New API endpoints without corresponding integration tests
- Database migrations that aren't backward-compatible
- Error messages that leak internal details to users
- New dependencies added without justification in PR description
- Changes to authentication or authorization logic
- Raw SQL queries (must use parameterized queries)
- Functions over 50 lines

## Style preferences
- Prefer early returns over nested conditionals
- Use structured logging (key=value), not f-string interpolation in log calls
- Async functions that don't actually await anything should be synchronous
- Prefer explicit error types over generic Exception catches

## Skip — do not flag these
- Generated files under `src/gen/` or `*_generated.*`
- Formatting-only changes in `*.lock` files
- Changes to test fixtures and snapshots
- Import ordering (handled by tooling)
- Type annotation completeness (handled by mypy/tsc)
- Docstring presence (not required on internal functions)
