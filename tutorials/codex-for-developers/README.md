# OpenAI Codex For Developers

A practical guide to using OpenAI Codex as a professional developer. Covers the CLI, desktop app, Linear workflow, automations, and the system layer that makes it all work well.

---

## Contents

- [Three Ways to Use Codex](#three-ways-to-use-codex)
- [CLI](#cli)
- [VS Code Extension](#vs-code-extension)
- [Desktop App](#desktop-app)
- [Live Demo: Linear Workflow](#live-demo-linear-workflow)
- [Automations](#automations)
- [Pricing](#pricing)
- [System Layer](#system-layer)
- [Quick Tips](#quick-tips)
- [Codex vs Claude Code](#codex-vs-claude-code)

---

## Three Ways to Use Codex

1. **The CLI** — if you like working in the terminal
2. **The desktop app** — designed for parallel work across multiple projects
3. **The VS Code extension** — if you want to stay inside your editor

---

## CLI

### Install

```bash
npm install -g @openai/codex
# or
brew install codex
```

Worth knowing: it is a Rust binary under the hood. npm is just the installer.

### Open it

```bash
codex
```

Clean, minimal TUI. Type `/` to see built-in slash commands.

### Useful slash commands

| Command | What it does |
|---|---|
| `/init` | Generate an AGENTS.md for this project — do this first in any new repo |
| `/diff` | See what changed during a task |
| `/fork` | Copy the session before trying something risky |
| `/compact` | Summarise earlier context when the session gets long |

### Non-interactive mode

```bash
codex exec "add input validation to src/api/users.py"
```

No TUI, just output. This is where Codex becomes developer tooling rather than just an app. Composes with the shell, justfiles, Git, and CI.

Pipe something in:

```bash
cat error.log | codex exec "Explain this error and suggest a fix"
```

### Sessions persist

```bash
codex resume       # opens a picker
codex resume --last
```

Sessions are saved. You can always come back to where you left off.

---

## VS Code Extension

Available from the VS Code extensions panel — search for Codex and install. Useful if you prefer to stay inside your editor. The desktop app and CLI cover everything in this guide.

---

## Desktop App

### Two modes that matter

| Mode | Use it for |
|---|---|
| Local | Small supervised tasks in your current checkout |
| Worktree | Isolated parallel work without touching your main branch |

### Local mode

Local works directly in the project directory you have open. Use it for small focused tasks: explain a module, add one test, make one small fix.

Start from a clean Git state, write the task, let Codex work, then check `/diff` before accepting anything.

### Worktree mode

Git worktrees give you multiple checkouts of the same repo on disk at the same time. Each Codex task gets its own directory and working state. Tasks do not block each other.

The practical workflow: fire two or three tasks in parallel, get on with something else, come back and review the diffs. Your main checkout stays clean throughout.

### What is actually in the app

Beyond the task input box:

- **Open in VS Code** — when working in a worktree, open it directly in VS Code. Useful for browsing changes while Codex is still running.
- **Integrated terminal** — run commands in the worktree without switching windows
- **Git diff view** — staged changes, commit from inside the app
- **Line comments on diffs** — leave a comment on a specific line rather than accepting or rejecting the whole diff. Keeps review conversational.
- **Keyboard shortcuts** — `Cmd+Enter` submit, `Cmd+K` command palette, `Escape` stop

---

## Live Demo: Linear Workflow

This is the workflow I use on real client projects. The Linear plugin keeps the full loop inside Codex — no context switching, no copy-pasting between tools.

### Install the Linear plugin

Settings > Plugins > Browse > Linear > Install

Plugins give Codex access to external tools from within the session. Install only what you actually use — each plugin adds context overhead.

See: [`05-plugins/README.md`](05-plugins/README.md)

### The three context layers

Before starting any task, make sure Codex has three things:

1. `AGENTS.md` — standing rules. How tests run, project layout, commit conventions, the Linear workflow.
2. A Linear ticket — today's task. Outcome, acceptance criteria, constraints. Not implementation steps.
3. `docs/product-spec.md` (if relevant) — what the product is, what is out of scope.

AGENTS.md holds the standing rules. The ticket holds today's work. Together, that is enough context for a strong implementation pass.

### The workflow

**Step 1 — Pull the ticket from Linear**

```
Show me the details for [ticket ID]
```

Codex reads the title, description, and acceptance criteria directly from Linear. No copy-paste needed.

**Step 2 — Run the task**

Fire the task. While it is running, fire a second smaller ticket in Worktree. You do not need to sit and watch — that is the point of the parallel workflow.

**Step 3 — Review the diff**

When the task completes, review the diff the same way you would review a PR from a junior engineer:

- Did it meet the goal in the ticket?
- Did it stay in scope?
- Are the tests meaningful?
- Did it touch anything it should not have?

Accept what looks right. Flag anything that needs a tweak. Iterate on the specific lines, not the whole diff.

**Step 4 — Close the loop in Linear**

```
Mark [ticket ID] as done and add a comment summarising what was built
```

Ticket in Linear, built with Codex, diff reviewed, ticket closed. No manual status updates.

---

## Automations

The desktop app can run recurring tasks on a schedule. Useful for maintenance work that is easy to forget.

### Example: check for stale dependencies

Create a new automation with a prompt like:

```
Check this project for stale or outdated dependencies. List anything that is significantly behind with a short note on whether it is worth updating.
```

Set it to run weekly. You get a dependency health check without having to remember it.

Other useful examples:

- **Weekly summary** — `Summarise what changed in this repo this week`
- **Branch check-in** — `Check if there are any open branches older than two weeks`

---

## Pricing

Everything covered in this guide is available on the standard $20 a month ChatGPT Plus plan. Not a pro plan, not an API-only setup — full access to the desktop app, the CLI, and the full model.

Rate limits are better than most people expect. For focused supervised work, the $20 plan goes a long way. Heavy parallel worktree use will burn through it faster.

---

## System Layer

### AGENTS.md

The operating manual for Codex on a project. Include: what the product does, how to run tests, commit conventions, and the Linear workflow if you use it.

Keep it short. Do not put things in AGENTS.md that Codex can figure out from the repo itself — that kind of detail gets stale fast.

Run `/init` in any project to generate a starting point.

See: [`01-setup/AGENTS.md`](01-setup/AGENTS.md)

### Skills

Reusable workflows stored as a `SKILL.md` file. Use them when you repeat the same kind of task across projects: code review, release notes, planning, security checks.

Type `$` in Codex to see available skills. Store personal skills in `~/.agents/skills/` and they are available in every project.

See: [`04-skills/plan-skill/SKILL.md`](04-skills/plan-skill/SKILL.md)

---

## Quick Tips

- **Fork** — `/fork` copies the current session into a new thread. Use it before trying something risky so you keep your progress and can explore a different direction.
- **Fast mode** — `/fast` runs tasks quicker but costs more credits. Good for low-stakes work like formatting or docstrings.
- **Mention files** — `/mention path/to/file` when you want Codex to look at a specific file rather than guessing.
- **Subagents** — ask explicitly: `Spawn one agent to check for security issues, one for test gaps, one for anything brittle. Summarise the findings.`

---

## Codex vs Claude Code

They are not competing for the same use case.

| Codex | Claude Code |
|---|---|
| Delegation | Conversation |
| Parallel tasks | Interactive debugging |
| Ticket-shaped work | Exploratory work |
| Reviewable diffs | Back-and-forth reasoning |

If you can write a clear plan or spec, reach for Codex. If you are still figuring out the problem, reach for Claude Code.

---

## Resources in this repo

| File | What it is |
|---|---|
| [`01-setup/AGENTS.md`](01-setup/AGENTS.md) | Real AGENTS.md example |
| [`config.toml.example`](config.toml.example) | Safe default config |
| [`codex-permissions-guide.md`](codex-permissions-guide.md) | Permissions reference |
| [`02-plans-and-specs/template.md`](02-plans-and-specs/template.md) | Task brief template |
| [`02-plans-and-specs/good-example.md`](02-plans-and-specs/good-example.md) | Good task brief example |
| [`04-skills/plan-skill/SKILL.md`](04-skills/plan-skill/SKILL.md) | Example skill file |
| [`05-plugins/README.md`](05-plugins/README.md) | Plugins guide |
| [`06-automation/justfile`](06-automation/justfile) | justfile targets |
| [`resources/live-demo-workflow.md`](resources/live-demo-workflow.md) | Live demo workflow |
| [`resources/plan-template.md`](resources/plan-template.md) | Short plan template |

---

If you want to go deeper on building with AI tools professionally, I run [AI Engineer](https://skool.com/ai-engineer) — a community for engineers doing serious work with these tools.
