---
description: Review uncommitted changes against REVIEW.md guidelines
---

Review all uncommitted code changes against the project's review standards.

1. Read REVIEW.md from the repository root. This contains the review rules.
   If no REVIEW.md exists, fall back to CLAUDE.md.

2. Get changed files:
   - Staged changes: `git diff --staged --name-only`
   - Otherwise: `git diff --name-only HEAD`

3. Skip files matching patterns in the "Skip" section of REVIEW.md.

4. Launch 3 parallel agents to review the remaining files:

   Agent 1 — Rules Check:
   Check every "Always flag" rule in REVIEW.md against the diff.
   Record file, line number, rule violated, one-line fix suggestion.

   Agent 2 — Bug Scan:
   Look for logic errors, null access, unhandled errors, security issues.
   Only flag issues with >80% confidence. Skip linter/typecheck concerns.

   Agent 3 — Neighborhood Check:
   For each changed file, read 2-3 related files (imports, callers, tests).
   Look for: duplicated logic, broken contracts, missing test updates.

5. Assign severity per finding:
   - BUG: will break production
   - NIT: worth fixing, not blocking
   - PRE-EXISTING: exists but not introduced by these changes

6. Drop findings matching the "Skip" section.

7. Report grouped by file, severity first:

   ## Review Results
   ### path/to/file.py
   - **BUG** (line 42): Description. Fix: suggestion.
   - **NIT** (line 87): Description. Fix: suggestion.

   ### Summary
   - X bugs, Y nits found
   - Ready to commit: YES/NO
