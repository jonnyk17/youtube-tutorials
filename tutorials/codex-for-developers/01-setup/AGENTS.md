# Project Name

One sentence on what this product does and who it is for.

Read `docs/product-spec.md` when a task touches product direction, scope, or user workflow.

## Commands

See `justfile` for all available commands. Run `just` to list them.

## Commit conventions

Include the Linear ticket identifier when work maps to a ticket:

```
GRA-141 Add minimal Postgres persistence
```

Use a plain message for housekeeping work not tied to a ticket.

## Linear workflow

Linear project: `[Project Name]`.

- Pick up tickets from the backlog
- Move a ticket to `In Progress` when starting work
- Keep implementation scoped to that ticket unless asked otherwise
- Move the ticket to `Done` once the work is implemented and verified

## Rules

- Keep responses concise. Short summary plus files changed, not long explanations.
- Ask rather than guess when requirements are unclear.
- Prefer boring, obvious patterns over abstractions.
