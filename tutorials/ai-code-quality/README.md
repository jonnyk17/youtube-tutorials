# Improving AI-Generated Code Quality

A practical guide to getting high-quality code from AI coding agents. No theory — just patterns you can implement today.

## The Problem

AI agents write code that works but drifts. It passes tests, compiles, and does what you asked. But it also introduces subtle issues: duplicated logic, inconsistent patterns, leftover debug statements, missed edge cases, conventions it forgot about 40 messages into a session.

"AI slop" isn't about bad code. It's about code that's *fine* individually but degrades your codebase over time.

---

## Part 1: Out of the Box — Install These Two Plugins

Before building anything custom, start with what Anthropic already ships. Two plugins, two commands in your terminal.

### Install

```bash
claude plugins install code-simplifier
claude plugins install code-review
```

That's it. Now you have two new slash commands.

### `/simplify` — Clean Up What You Just Wrote

**What it is:** An Opus-powered agent that reads your recently modified code, checks the surrounding files for context, and **fixes what it finds** — it doesn't just report issues, it edits your code.

**When to use it:** After finishing a feature or logical unit of work. Think of it as "clean up my work before I commit."

**How to run it:** Type `/simplify` in your Claude Code session.

**What it catches:**
- Unnecessary complexity and deep nesting
- Redundant code and premature abstractions
- Duplicated logic that already exists elsewhere in the codebase
- Overly clever one-liners that hurt readability
- Nested ternaries (rewrites to switch/if-else)
- Comments that describe obvious code

**What makes it different from a linter:** It reads the *neighborhood* — the files around your changes. A linter can tell you a function is long. `/simplify` can tell you the function duplicates one in `utils/` three directories away.

### `/code-review` — Multi-Agent PR Review

**What it is:** A review pipeline that dispatches 8+ agents against a pull request, scores every finding for confidence, and only reports issues it's highly sure about.

**When to use it:** After pushing a branch and opening a PR.

**How to run it:** Type `/code-review <PR-number>` in Claude Code.

**The pipeline:**

```
Haiku: Is this PR eligible? (skip if closed, draft, already reviewed)
Haiku: Find all CLAUDE.md files in the repo
Haiku: Summarize the change

5 Sonnet agents review in parallel:
  #1 — CLAUDE.md compliance
  #2 — Shallow bug scan (obvious bugs only, no nitpicks)
  #3 — Git blame context (bugs visible from file history)
  #4 — Previous PR comments (recurring issues on these files)
  #5 — Code comment compliance

Haiku agents score each finding 0-100:
  0   = false positive
  25  = might be real
  50  = real but a nitpick
  75  = verified, will impact functionality
  100 = definitely real, will happen frequently

Filter: only findings >= 80 are reported
Post results as a GitHub PR comment
```

**Why the scoring matters:** This is how you avoid the "AI reviewer that flags 47 nitpicks" problem. It explicitly skips:
- Pre-existing issues (don't flag what you didn't write)
- Things linters/compilers already catch
- Pedantic nitpicks a senior engineer wouldn't mention
- Issues on lines the PR didn't modify

### The Out-of-the-Box Workflow

```
Write code
  |
  v
/simplify (clean up recently changed code)
  |
  v
git commit && git push && open PR
  |
  v
/code-review <PR#> (multi-agent review, posts to GitHub)
```

**This is already better than what most people are doing.** But these plugins are generic — they don't know your team's conventions, your project's patterns, or the specific bugs you keep hitting.

---

## Part 2: Make It Yours — REVIEW.md + Custom `/review` Command

The plugins are a great starting point, but they're black boxes. The `/code-review` plugin is literally one markdown file you can't edit without forking the plugin. It reads CLAUDE.md but doesn't know about REVIEW.md. And it only works on PRs — you can't use it before committing.

This is where you build your own.

### REVIEW.md — Your Team's Review Rules

Create a `REVIEW.md` at your repo root. This is a living document that encodes what your team cares about during review — the stuff no generic tool can know.

Three sections: what to flag, what style you prefer, and what to skip.

```markdown
# Code Review Guidelines

## Always flag
- New API endpoints without corresponding integration tests
- Database migrations that aren't backward-compatible
- Error messages that leak internal details to users
- New dependencies added without justification in PR description
- Changes to authentication or authorization logic
- Raw SQL queries (must use parameterized queries)
- Functions over 50 lines
- Synchronous I/O in async functions

## Style preferences
- Prefer early returns over nested conditionals
- Prefer match statements over chained isinstance checks
- Use structured logging (key=value), not f-string interpolation in log calls
- Async functions that don't await anything should be synchronous

## Skip — do not flag these
- Generated files under src/gen/ or *_generated.*
- Formatting-only changes in *.lock files
- Changes to test fixtures and snapshots
- Import ordering (handled by tooling)
- Type annotation completeness (handled by mypy/tsc)
- Docstring presence (not required on internal functions)
```

**Why separate from CLAUDE.md?** Some rules don't make sense as code generation instructions. "Flag any new API route without an integration test" is a review concern — you don't want the agent refusing to write code until it also writes a test. `CLAUDE.md` tells the agent *how to write code*. `REVIEW.md` tells the reviewer *what to catch*.

**The "Skip" section is as important as the "Always flag" section.** Without it, the reviewer wastes your time on generated code, lock files, and things your linter already handles.

**Write rules like a checklist for a new hire.** If a rule requires subjective judgment ("is this code elegant?"), it produces inconsistent results. If a rule can be verified against the diff ("does this new endpoint have a test file?"), it produces reliable results.

### Custom `/review` Command — Local Review Before Committing

This is the custom command that reads REVIEW.md and reviews your **local, uncommitted changes**. No PR required.

Create `.claude/commands/review.md`:

```markdown
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
```

**Usage:** Type `/review` in Claude Code. It runs against your uncommitted changes, guided by your REVIEW.md.

### Why Build Your Own Instead of Using the Plugin?

This is what the [everything-claude-code](https://github.com/affaan-m/everything-claude-code) repo did — they wrote their own review commands and agents. Here's why:

1. **The plugin only works on PRs** — you can't review before committing
2. **The plugin is a black box** — one markdown file you can't edit without forking
3. **The plugin doesn't read REVIEW.md** — it only checks CLAUDE.md
4. **You can't customize the agents** — maybe you want a security-focused agent, or framework-specific checks (React hooks, N+1 queries, etc.)
5. **A markdown file in your repo is a tool you control** — edit the agents, change the threshold, add checks, remove noise

### How `/review` Differs from `/code-review`

| | `/code-review` (plugin) | `/review` (custom) |
|---|---|---|
| **Scope** | PR on GitHub | Local uncommitted changes |
| **When** | After opening a PR | Before committing |
| **Rules source** | CLAUDE.md only | REVIEW.md (your rules) |
| **Agents** | 5 Sonnet + Haiku scoring | 3 agents (you control) |
| **Posts to GitHub** | Yes | No |
| **Editable** | No (plugin) | Yes (your markdown file) |

**They're complementary, not competing.** Use `/review` locally as your first pass, `/code-review` on the PR as the second pass. Two review layers, different scopes.

### Local vs. Remote Review

This is an important distinction:

**Local review** (`/review`, `/simplify`):
- Runs in your Claude Code session, on your machine
- Reviews uncommitted/staged changes
- Fast feedback loop — fix issues before they reach the PR
- Only you see the results
- Reads your local REVIEW.md

**Remote review** (`/code-review`, GitHub Action):
- Runs against a PR on GitHub
- Reviews the full diff between branches
- Results are visible to the team (posted as PR comments)
- Acts as a quality gate before merge
- Can be automated in CI

**Both are valuable. Neither replaces the other.** Local review catches issues early (cheaper to fix). Remote review catches what you missed and creates a visible record for the team.

---

## Part 3: Advanced — Custom Code Review Agent

If you want even more control, you can create a full agent definition (not just a slash command). This is the same pattern the `/code-review` plugin uses internally, but you own every detail.

Create `.claude/agents/code-reviewer.md`:

```markdown
---
name: code-reviewer
description: Multi-agent code review guided by REVIEW.md
model: sonnet
---

You are a senior code reviewer. You review code changes using the project's
REVIEW.md guidelines and best practices from the Anthropic code review plugin.

## Process

### Step 1: Load review rules
Read REVIEW.md from the repository root. If it doesn't exist, read CLAUDE.md.
Extract three lists:
- MUST_FLAG: rules from "Always flag"
- STYLE: rules from "Style preferences"
- SKIP_PATTERNS: patterns from "Skip"

### Step 2: Determine scope
Check if you were given a PR number or local changes:
- PR number provided: use `gh pr diff <number>` to get the diff
- No PR number: use `git diff --staged` (or `git diff HEAD` if nothing staged)

Get the list of changed files. Remove any matching SKIP_PATTERNS.

### Step 3: Dispatch parallel review agents

Launch these agents in parallel:

**Agent 1 — REVIEW.md Compliance (Sonnet)**
For each changed file, read the diff and check against every rule in MUST_FLAG.
For each violation: record file path, line number, the rule text, and a fix.
Tag as severity NIT if it's a STYLE rule, BUG if it's a MUST_FLAG rule.

**Agent 2 — Bug Detection (Sonnet)**
Read each changed file's diff. Look for:
- Logic errors and off-by-one mistakes
- Null/undefined access without guards
- Unhandled error paths and missing catch blocks
- Security issues (injection, auth bypass, secrets in code)
- Race conditions in async code
- Resource leaks (unclosed connections, file handles)

Only flag issues with >80% confidence of being real bugs.
Skip anything a linter, type checker, or compiler would catch.
Tag all findings as BUG.

**Agent 3 — Neighborhood Review (Sonnet)**
For each changed file:
- Read 2-3 related files (imports, callers, test files)
- Check if changes are consistent with surrounding code patterns
- Look for duplicated logic that already exists nearby
- Check if test files need updating for the changes
- Verify that function contracts (params, return types) are maintained

Tag findings as BUG if a contract is broken, NIT otherwise.

**Agent 4 — REVIEW.md Skip Verification (Haiku)**
Take all findings from Agents 1-3. For each finding:
- Check if the file or issue type matches any SKIP_PATTERNS
- Check if the issue is pre-existing (exists on the base branch too)
- Check if the finding is something a linter would catch
- Score confidence 0-100 using this rubric:
  - 0: false positive, doesn't survive scrutiny
  - 25: might be real, can't verify
  - 50: real but a nitpick, not important for this PR
  - 75: verified real issue, will impact functionality
  - 100: definitely real, evidence confirms it
- Drop any finding scoring below 75

### Step 4: Report

Group remaining findings by file, severity first:

## Code Review

### path/to/file.py
- **BUG** (line 42): [description] — REVIEW.md rule: "[rule text]"
  Fix: [one-line suggestion]
- **NIT** (line 87): [description]
  Fix: [one-line suggestion]

### path/to/other.py
- **PRE-EXISTING** (line 12): [description] — not introduced by this change

### Summary
| Severity | Count |
|----------|-------|
| BUG      | X     |
| NIT      | Y     |
| PRE-EXISTING | Z |

**Ready to merge: YES/NO** (NO if any BUG findings remain)

If no issues found: "No issues found. Reviewed N files against M rules."

## Important
- NEVER flag formatting, import ordering, or type annotations
- NEVER flag issues on lines that weren't changed (unless they're in MUST_FLAG)
- Pre-existing bugs get tagged PRE-EXISTING, not BUG
- When unsure, don't flag it — false positives erode trust in the reviewer
- If a finding matches a SKIP_PATTERNS entry, drop it silently
```

### Using the Custom Agent

You can invoke it from Claude Code:

```
# Review local changes
Review my uncommitted changes using the code-reviewer agent

# Review a specific PR
Use the code-reviewer agent to review PR #42
```

Or create a slim slash command that dispatches it. Create `.claude/commands/review.md`:

```markdown
---
description: Review code changes against REVIEW.md (local or PR)
---

Use the code-reviewer agent to review changes.

If a PR number is provided as $ARGUMENTS, review that PR.
Otherwise, review uncommitted local changes.
```

### How This Compares

| | Plugin `/code-review` | Custom agent |
|---|---|---|
| Reads REVIEW.md | No | Yes |
| Local + PR review | PR only | Both |
| Number of agents | 5 Sonnet + Haiku | 3 Sonnet + 1 Haiku (configurable) |
| Git blame analysis | Yes (Agent #3) | No (add if you want) |
| Previous PR comments | Yes (Agent #4) | No (add if you want) |
| Confidence scoring | Yes (0-100, threshold 80) | Yes (0-100, threshold 75) |
| Skip patterns | No | Yes (from REVIEW.md) |
| Editable | No | Yes — it's your markdown file |

The plugin has two agents the custom version doesn't: git blame history and previous PR comment analysis. You can add those as Agent 5 and Agent 6 if you want them. The custom version has REVIEW.md integration and local review, which the plugin doesn't.

**You don't have to choose.** Run your custom `/review` locally, run the plugin `/code-review` on PRs. Two passes, different perspectives.

---

## Part 4: Automation — Hooks and CI

### Hooks — Deterministic Quality Gates (Every Edit, Free)

Hooks are shell commands that fire automatically at lifecycle events. They're not LLM calls — they're scripts. They don't forget instructions at message 40.

**The rule: if you can express it as a deterministic script, it should be a hook, not a prompt instruction.**

Put hooks in `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "python3 -c \"import json,sys,subprocess; d=json.load(sys.stdin); f=d.get('tool_input',{}).get('file_path',''); subprocess.run(['ruff','format',f],capture_output=True) if f.endswith('.py') else None; print(json.dumps(d))\""
        }],
        "description": "Auto-format Python files after edit"
      },
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "python3 -c \"import json,sys,subprocess,re; d=json.load(sys.stdin); f=d.get('tool_input',{}).get('file_path',''); subprocess.run(['npx','prettier','--write',f],capture_output=True) if re.search(r'\\\\.(ts|tsx|js|jsx)$',f) else None; print(json.dumps(d))\""
        }],
        "description": "Auto-format JS/TS files after edit"
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "python3 -c \"import json,sys,re; d=json.load(sys.stdin); f=d.get('tool_input',{}).get('file_path',''); content=open(f).read() if f else ''; sys.exit(1) if re.search(r'(?i)(api[_-]?key|secret|token|password)\\\\s*[=:]\\\\s*[\\\\\\\"\\\\\\'][^\\\\\\\"\\\\\\']+',content) else print(json.dumps(d))\""
        }],
        "description": "Block edits that introduce hardcoded secrets"
      }
    ]
  }
}
```

**Why auto-format matters:** Claude approximates your style but doesn't read your `ruff.toml` or `.prettierrc`. Without this hook, every AI edit creates formatting noise in diffs. Your reviewer wastes time on whitespace instead of logic.

**Why secrets blocking matters:** A PreToolUse hook that exits non-zero **blocks the edit entirely**. The agent physically cannot write a hardcoded API key to a file. Too important to leave to probability.

### GitHub Action — Automatic PR Review (Every PR)

The safety net that always fires, whether anyone remembers or not.

`.github/workflows/review.yml`:

```yaml
name: Code Review
on:
  pull_request:
    types: [opened, reopened, ready_for_review]

jobs:
  review:
    if: ${{ !github.event.pull_request.draft }}
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            You are a code reviewer. Review this pull request.

            First read REVIEW.md at the repository root. It has three sections:
            - "Always flag": check every change against these rules
            - "Style preferences": flag as nits only
            - "Skip": ignore these files and patterns completely

            Also read any CLAUDE.md files for additional context.

            For each finding, tag severity:
            - BUG: must fix before merge
            - NIT: worth fixing, not blocking
            - PRE-EXISTING: exists but not introduced by this PR

            Only report findings with >80% confidence.
            Post as a single PR comment.
          claude_args: "--max-turns 5 --model claude-sonnet-4-6"
```

**Setup:** Install the Claude GitHub App (`/install-github-app` or https://github.com/apps/claude), add `ANTHROPIC_API_KEY` to repository secrets.

**Cost control:** Sonnet with 5 turns on a small PR costs ~$0.50-2.00. Use `--max-turns 3` for budget mode, `--model claude-opus-4-6` for deeper review on critical repos.

---

## Part 5: The Role of Human Review

AI review doesn't replace human review. Here's why:

**What AI review catches that humans miss:**
- The single-line change that breaks auth (Anthropic's internal case)
- Pre-existing bugs in adjacent code (the TrueNAS encryption key cache wipe)
- REVIEW.md rule violations that humans forget to check
- Issues at scale — humans skim 1,000-line PRs, agents read every line

**What humans catch that AI review misses:**
- "This feature shouldn't exist" — architectural and product judgment
- "This is technically correct but the wrong abstraction" — design taste
- "We tried this approach last quarter and it didn't work" — institutional memory not in any markdown file
- Cross-system implications that span multiple repos
- Whether the PR even solves the right problem

**The right framing:** AI review checks the trees. Humans check the forest. AI handles the mechanical checklist ("does every endpoint have a test?") so humans can focus on the judgment calls ("is this the right endpoint to build?").

**Where to put human review in the workflow:**

```
Write code
  ├── Hooks (mechanical, every edit)
  v
/simplify (neighborhood cleanup)
  v
/review (check against REVIEW.md)
  v
git push && open PR
  v
GitHub Action reviews (automated, posts to PR)
  v
Human reviewer reads AI findings + applies judgment    <-- here
  v
Approve and merge
```

AI review is the pre-filter. It handles the 80% of review that's mechanical so the human reviewer can spend their time on the 20% that requires judgment.

---

## The Complete Workflow

```mermaid
flowchart TB
    subgraph "While Writing (automatic)"
        A[Agent writes code] --> B[PostToolUse hooks fire]
        B -->|format, lint, secrets| A
    end

    subgraph "Local Review (manual)"
        A --> C[/simplify]
        C -->|clean up neighborhood| D[/review]
        D -->|check REVIEW.md rules| E{Issues?}
        E -->|BUGs found| F[Fix and re-review]
        F --> D
        E -->|Clean| G[git commit & push]
    end

    subgraph "Remote Review (automatic)"
        G --> H[GitHub Action reviews PR]
        H --> I[Human reviewer]
        I --> J[Merge]
    end
```

### Files You Need

```
your-project/
├── CLAUDE.md                          # How to write code (agent reads this always)
├── REVIEW.md                          # What to catch during review (your team's rules)
├── .claude/
│   ├── settings.json                  # Hooks (format, secrets, debug warnings)
│   ├── commands/
│   │   └── review.md                  # Custom /review command
│   └── agents/
│       └── code-reviewer.md           # Full custom review agent (optional, advanced)
└── .github/
    └── workflows/
        └── review.yml                 # GitHub Action for automatic PR review
```

### What Goes Where

| Quality concern | Where | Why |
|----------------|-------|-----|
| Formatting | Hook | Deterministic. Your formatter config is the source of truth. |
| Hardcoded secrets | Hook (blocking) | Too important for probability. Block the edit entirely. |
| Debug statements | Hook (warning) | Warn, don't block — sometimes intentional during dev. |
| Code duplication | `/simplify` | Requires reading surrounding files. Only an LLM can do this. |
| Your team's rules | `/review` + REVIEW.md | Project-specific. No generic tool knows these. |
| Bugs in the diff | GitHub Action or `/code-review` | Needs full diff context. |
| Architecture decisions | Human review | AI checks the trees. Humans check the forest. |

---

## Summary

| Step | Tool | Type | Cost |
|------|------|------|------|
| 1. Install plugins | `code-simplifier`, `code-review` | Out of the box | API usage |
| 2. Write REVIEW.md | Your team's review rules | Your markdown file | Free |
| 3. Create `/review` command | Custom command reading REVIEW.md | Your markdown file | API usage |
| 4. Add hooks | Format, secrets, debug warnings | Deterministic scripts | Free |
| 5. Add GitHub Action | Automatic PR review | CI automation | API usage |
| 6. (Optional) Custom agent | Full multi-agent reviewer | Your markdown file | API usage |

**Start with step 1.** Install the plugins, use `/simplify` and `/code-review` as-is. See if generic review is enough.

**When it's not enough, do step 2-3.** Write your REVIEW.md, create the custom command. This is where the real value is — your team's specific rules, encoded and version-controlled.

**Steps 4-5 make it automatic.** Hooks for the mechanical stuff, GitHub Action for PR review. Nobody has to remember anything.

**Step 6 if you want full control.** A custom agent with 4 parallel reviewers, REVIEW.md integration, confidence scoring, skip patterns. You own every detail.

The pattern: **start generic, make it specific, then automate it.**

---

## Go Further

### Anthropic Managed Code Review (Team/Enterprise)

Anthropic launched a managed Code Review product in March 2026. It auto-triggers on every PR with zero setup beyond installing the GitHub App. It natively reads both CLAUDE.md and REVIEW.md. Results appear as inline annotations with collapsible reasoning showing how the agent verified each finding.

**The numbers (Anthropic's internal results):**
- PRs receiving substantive review comments went from 16% to 54%
- Less than 1% of findings marked incorrect by engineers
- Large PRs (1,000+ lines): 84% get findings, averaging 7.5 issues
- Small PRs (under 50 lines): 31% get findings, averaging 0.5 issues

**Notable catches:** A single-line auth-breaking change that human reviewers waved through. A pre-existing type mismatch in TrueNAS open-source middleware that was silently wiping the encryption key cache on every sync — found in adjacent code, not even in the diff.

**Cost:** $15-25 per review, scaling with PR size and complexity. Currently only available on Team and Enterprise plans.

**The honest take:** The results are impressive, but $15-25/review adds up fast. For most individual developers and small teams, the workflow in this guide gets you 80% of the value at 5% of the cost. The managed product makes sense when reviewer time is your bottleneck and $15/review is trivial compared to engineering salaries.

### Third-Party AI Code Review Tools

If you want an off-the-shelf solution without building your own, these are worth looking at:

| Tool | What it does | Free tier |
|------|-------------|-----------|
| [CodeRabbit](https://coderabbit.ai) | AI PR review with inline comments. Learns from your feedback (thumbs up/down on findings). Supports GitHub, GitLab, Bitbucket. | Free for open source |
| [Sourcery](https://sourcery.ai) | Python-focused AI review and auto-refactoring. Suggests cleaner patterns. | Free (limited) |
| [Qodo](https://qodo.ai) (formerly CodiumAI) | AI test generation + code review. Focuses on test coverage gaps. | Free (limited) |
| [Codacy](https://codacy.com) | Automated code quality, security scanning, and coverage tracking. | Free for open source |
| [Ellipsis](https://ellipsis.dev) | AI code review for GitHub PRs. Focuses on bugs over style. | Paid |

The main difference between these and the approach in this guide: these are hosted services you give repository access to. The REVIEW.md + custom command + GitHub Action approach runs on your own API key, with your own rules, and you control every detail. Trade-off: more setup, more control.

---

## Resources

- [Claude Code Review docs](https://code.claude.com/docs/en/code-review) — managed Code Review product documentation (REVIEW.md format, setup, pricing)
- [Claude Code official plugins](https://github.com/anthropics/claude-plugins-official/tree/main/plugins) — all first-party Anthropic plugins (browse the source)
- [code-review plugin source](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-review) — the actual `/code-review` command (one markdown file — read it to understand what it does)
- [code-simplifier plugin source](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-simplifier) — the `/simplify` agent definition
- [Claude Code GitHub Action](https://github.com/anthropics/claude-code-action) — run Claude in CI on PRs and issues
- [everything-claude-code](https://github.com/affaan-m/everything-claude-code) — community plugin with custom review commands, hooks, and agents (the repo that inspired much of this guide)
- [Claude Code hooks documentation](https://code.claude.com/docs/en/hooks) — how to write PreToolUse and PostToolUse hooks
