Read the Linear issue $ARGUMENTS using the Linear MCP tool.

If the issue has a parent issue, read that too for full context.
If the description references a spec file (e.g. `Spec: specs/feature.md`), read it.

Then follow this workflow:

1. Set the issue status to **In Progress**.
2. Create a branch following the convention in CLAUDE.md:
   - Format: `<prefix>/<issue-id-lowercase>-<slug>`
   - Determine prefix from issue labels: `feature/`, `fix/`, `cleanup/`, `docs/`
3. Implement the change described in the ticket.
4. Run the build command and confirm it passes.
5. Commit with the issue ID in the message: `<summary> (<ISSUE-ID>)`
6. Review your own diff (`git diff main`) for bugs, dead code, or issues.
7. Fix any critical issues found during self-review.
8. Push and create a PR with `gh pr create`.
   - PR body: summary, verification section, link to Linear issue.
9. Set the issue status to **In Review**.
10. Add a comment on the Linear issue with the PR URL.

If anything fails at any step, stop and report the error. Do not attempt workarounds.
