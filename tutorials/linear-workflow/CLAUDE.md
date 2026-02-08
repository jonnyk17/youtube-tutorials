# CLAUDE.md

## Project

- Runtime: Bun
- Build: `bun run build`

## Linear Integration

- Fetch issues using the Linear MCP tool.
- Always read the parent issue (if one exists) for full context before starting work.
- If a description references a spec file (`Spec: specs/<feature>.md`), read it before implementing.
- Set issue status to **In Progress** when starting, **In Review** after PR creation.
- Issue lifecycle: Backlog → Todo → In Progress → In Review → Done (Done happens after merge, not by you).

## Branching

Branch format: `<prefix>/<issue-id-lowercase>-<slug>`

Prefix is determined by issue labels:
- `feature/` — label: `feature` (or no relevant label)
- `fix/` — label: `bug`
- `cleanup/` — label: `cleanup` or `tech-debt`
- `docs/` — label: `docs`

Example: `feature/proj-12-add-user-auth`

## Commits

- Message format: `<summary> (<ISSUE-ID>)` — e.g. `Add auth middleware (PROJ-12)`
- Never amend existing commits. Always create new fixup commits.
- Never force push.
- Never commit code that doesn't build. Run `bun run build` first.

## Pull Requests

Create with `gh pr create`. PR body must include:
- Summary of changes
- Verification section: `bun run build` result, files changed
- Link to the Linear issue

## Self-Review (required before pushing)

After implementation is complete, review your work before pushing:

1. Run `bun run build` and confirm it passes.
2. Launch a sub-agent to review the diff between this branch and main.
   Check for: bugs, unused imports, dead code, empty catch blocks,
   security issues, over-engineering, missing error handling.
   Classify findings as Critical (must fix), Warning (should fix), or Nit (optional).
3. Fix all Critical issues.
4. Re-run `bun run build` after any fixes.

## Error Handling

If anything fails — build, git push, PR creation — stop immediately and report the error. Do not attempt workarounds silently.
