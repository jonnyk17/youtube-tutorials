# [Project Name]

## What this is

One sentence: what the project does and what it runs on.

## Commands

```bash
just dev        # start development server
just test       # run tests
just lint       # run linter
just check      # lint + typecheck + test (run this before committing)
```

## Project layout

```
src/            # application source
  api/          # routes and handlers
  services/     # business logic
  models/       # data models
tests/          # mirrors src/ structure
```

## Conventions

- Follow patterns already in the codebase. Do not introduce new ones without asking.
- Tests go in `tests/` and mirror the source path.
- No new dependencies without checking the stdlib first.
- No `utils/`, `helpers/`, or `common/` folders.

## Rules

- Be concise. Short responses, no padding.
- Write tests for new functionality. Keep them simple and focused.
- Run `just check` before marking any task complete.
- Do not touch files outside the stated scope of the task.
- If something is unclear, ask one specific question rather than making assumptions.
