# Project Name

One sentence describing what this project does.

Read `docs/product-spec.md` when a task touches product direction, scope, phases, or user workflow.

## Communication
- Keep responses concise and practical.
- Prefer a short summary plus commands/files changed over long explanations.
- Ask questions instead of guessing.

## Repository Shape
- `backend/` contains all Python code.
- `frontend/` Bun/TypeScript UI.
- `docs/` contains product and phase planning docs.

## Commands
```bash
just dev        # start development server
just test       # run tests
just check      # lint + typecheck + test
```

## Linear Workflow

Linear project: `Your Project Name`.

Agents have access to Linear MCP for viewing project status and tickets.

Use Linear as the source of truth for current work:
- Pick up tickets from Linear.
- Move a ticket to `In Progress` when starting work.
- Keep implementation scoped to that ticket unless the user asks otherwise.
- Move the ticket to `Done` once the work is implemented and verified.
- Prefer high-level tickets over many tiny tasks while the product direction is still evolving.
