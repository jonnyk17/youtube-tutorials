# OpenAI Codex for Developers: The Practical Complete Guide

Companion repo for the YouTube video. Everything shown in the video is here.

---

## What is Codex

Codex is OpenAI's AI coding agent. It is not a code completion tool — it is an agent. You give it a task, it reads your codebase, writes code, runs commands, and gives you a diff to review. You decide whether to accept it.

The key difference from tools like Copilot or Cursor's inline completion: Codex works on tasks, not keystrokes. You describe what you want done. It does the work. You review.

**This guide covers two surfaces: the Desktop App and the CLI.**

I have been using Claude Code daily for over a year and still do. But recently I have been spending more time with Codex on real client projects — specifically the desktop app. Working across multiple projects at once, each with its own session and context, is where it has clicked for me.

I do not use the VS Code extension in my daily workflow. I run the Codex app alongside VS Code rather than inside it. So I am not covering it here.

| Surface | What it is |
|---------|------------|
| **Desktop App** | Local supervised work, parallel tasks, multi-project sessions, diff review |
| **CLI** | Terminal workflow, interactive sessions, scriptable automation, justfile integration |

---

## Mental model: how Codex actually works

Before touching the product, get this model clear. It will make every other decision obvious.

**The core loop is always the same:**

```
Write a task brief → Run the agent → Review the diff → Accept, iterate, or discard
```

**The practical decision table:**

```
Working in your current checkout, want to supervise closely?   → Local (Desktop App)
Want parallel tasks that don't touch your working branch?      → Worktree (Desktop App)
In the terminal, want something scriptable?                    → CLI
Already in VS Code and want a quick edit?                      → VS Code extension
```

**Local** means Codex works directly in your current project directory. Use this for supervised, focused work — explain this code, make a small edit, add one test.

**Worktree** means Codex creates a separate Git worktree: same repository, separate directory on disk, separate branch. Multiple worktrees can run simultaneously without conflicting. This is the mechanism behind parallel local work.

**The async model:** Codex is built for delegation. You write the task, fire it, and move on. There is no back-and-forth mid-task. If the brief was vague, the result will be vague. This is different from Claude Code, which is conversational. Both are useful — they are for different kinds of work.

---

## How Codex is isolated from your machine

This trips everyone up at first, so let's make it simple.

When Codex runs a task, it does two things you might not expect: it reads your files, and it runs commands. It might run your test suite, a linter, a build script. That means it is actually executing code on your computer — not just generating text.

**The sandbox is the answer to: what is Codex allowed to do when it runs those commands?**

Think of it like this. You have a new contractor working on your house. There are three ways you could set up their access:

- They can walk through any room and look around, but they cannot touch anything
- They can work freely inside the house, but they cannot leave the property or access the safe
- They have a copy of your keys and can go anywhere, do anything

That is exactly the three sandbox modes:

| Mode | What it means in plain English |
|------|-------------------------------|
| `read-only` | Codex can look at files but cannot edit anything or run commands without your approval |
| `workspace-write` | Codex can read and edit files in your project and run normal commands, but it cannot touch the rest of your system. **This is the default.** |
| `danger-full-access` | No restrictions. Codex can do anything your user account can do. |

**The default (`workspace-write`) is the right choice for almost everything.** It means Codex can edit your code and run your tests, but it cannot read your SSH keys, write outside your project folder, or make unexpected network calls. It is contained to the work.

**When would you use `danger-full-access`?** Only when the task genuinely needs it. Running Docker commands. Hitting a localhost service that requires broader network access. If you are not sure whether you need it, you do not need it.

**What about Git worktrees — is that the same thing?**

No. These are two completely separate concepts that often get confused.

- **Sandboxing** controls what *processes* can do on your system (file access, network, system calls)
- **Worktrees** control which *files* Codex is working on

A worktree is just a second checkout of your Git repo in a separate folder. When Codex works in a worktree, it is editing files in that folder, not in your main working branch. So if it goes wrong, your main branch is untouched. You just discard the worktree.

You can run any sandbox mode with or without worktrees. They are independent.

**The practical summary:**

- Leave the sandbox on `workspace-write` (the default). You get autonomous work inside your project without giving Codex access to the rest of your machine.
- Use worktrees when you want to run tasks in parallel or try something without touching your current branch.
- Only switch to `danger-full-access` if a specific task requires it and you understand what you are enabling.

**How to change the sandbox mode:**

In the Desktop App: use the permissions dropdown in the chat interface.

In the CLI: use `/permissions` during a session, or set a default in `~/.codex/config.toml`:

```toml
[sandbox]
mode = "workspace-write"  # read-only | workspace-write | danger-full-access
```

---

## Setup

**Desktop App:** Download from the official Codex page. Sign in with your OpenAI account.

**CLI:**
```bash
npm install -g @openai/codex
# or
brew install codex
```

Verify:
```bash
codex --version
```

**VS Code:** Install the OpenAI Codex extension from the Extensions panel.

**First thing to do in any new project:**
```bash
# Generate your AGENTS.md
/init
```

This creates the project instructions file Codex reads before every task. Edit it. The generated file is a starting point, not the finished thing. See [`01-setup/AGENTS.md`](01-setup/AGENTS.md) for a well-written example.

Copy [`01-setup/config.toml`](01-setup/config.toml) to `~/.codex/config.toml` to set your default reasoning level and approval mode.

---

## The task brief

**This is the single most important thing in this guide.** Task description quality is the biggest variable in output quality. Not the model. Not the settings. The brief.

Treat it like a ticket for a capable junior engineer. Give them context, scope, acceptance criteria, and what to avoid. Vague in, vague out.

**Bad:**
```
"Improve the API"
```

**Good:**
```
Goal: Add a /health endpoint that returns {"status": "ok"} with HTTP 200.
Context: Entry point is src/api/main.py. Follow the router pattern in src/api/routers/users.py.
Acceptance criteria:
  - GET /health returns 200 with {"status": "ok"}
  - Test exists at tests/api/test_health.py
Tests: pytest tests/api/test_health.py -x
Constraints: Do not modify existing routers. No new dependencies.
Non-goals: No auth, no DB check. Keep it simple.
```

The good version takes 3 minutes to write. It saves 20 minutes of correction.

See [`02-task-briefs/template.md`](02-task-briefs/template.md) for the full template.
See [`02-task-briefs/good-example.md`](02-task-briefs/good-example.md) and [`02-task-briefs/bad-example.md`](02-task-briefs/bad-example.md) for concrete examples.

---

## CLI tips

These are the things the docs mention but nobody shows you.

### 1. Resume a session

```bash
codex resume
```

Codex saves sessions. `codex resume` brings back the last one — full context intact. This is one of the most useful things in the product and most people never discover it.

### 2. Non-interactive mode (exec)

```bash
codex exec "add input validation to src/api/users.py"
```

Runs Codex without the interactive TUI. Scriptable, pipeable, works in CI. This is how Codex becomes part of your build tooling.

Capture output to a file:
```bash
codex exec "explain the auth flow in this codebase" > docs/auth-flow.md
```

### 3. Pipe stdin

```bash
cat error.log | codex "explain this error and suggest a fix"
```

You can pipe anything into Codex. Error logs, API responses, stack traces — give it the raw context and ask your question.

### 4. Wire into your justfile

See [`06-automation/justfile`](06-automation/justfile) for ready-to-use targets including:

```makefile
codex-review:
    codex exec "Review the current git diff. Flag anything wrong, missing tests, or inconsistent with the codebase."

codex-commit-msg:
    codex exec "Write a conventional commit message for the current diff. Output only the message."
```

### 5. One thread per task

This is a rule from the official best practices and it matters: use one thread per task, not one thread per project. When a thread accumulates too much context from multiple tasks, output quality degrades. Start fresh for each task.

### 6. Compact long sessions

```bash
/compact
```

When a session has been running for a while and the context is getting full, `/compact` summarizes the earlier conversation. Run it before starting a new subtask in the same session.

### 7. Fork before risky changes

```bash
/fork
```

Creates a new thread preserving the current transcript. Use this before attempting something that might not work — you keep your current state and can explore the alternative without losing context.

### 8. Tune reasoning effort

Set reasoning effort inside an interactive session with `/model` — you can switch mid-session without restarting.

| Level | When to use |
|-------|-------------|
| `low` | Fast, well-scoped tasks where speed matters |
| `medium` | Default. Most everyday work |
| `high` | Complex changes, refactors, debugging |
| `extra-high` | Long agentic tasks, security analysis, multi-file reasoning |

Higher reasoning takes longer and costs more. The default (`medium`) is right for most things.

### 9. Fast mode

```bash
/fast
```

Toggles fast mode on or off. When on, tasks run quicker but cost more credits. Use it for low-risk bounded work: formatting, docstrings, small edits. Turn it off for anything complex where getting it wrong is expensive. Check current state with `/fast status`.

### 10. Plan before you build

```bash
/plan
```

Or `Shift+Tab` to enter plan mode. Codex gathers context and writes a plan before touching any code. Review and approve the plan. For anything non-trivial, catching a wrong direction at the plan stage is much cheaper than catching it after 200 lines of code.

---

## Desktop App tips

### 1. Local vs Worktree: know when to use each

**Local:** You are supervising. Codex works in your current checkout. You see changes as they happen. Use this for focused, small tasks where you want to stay close.

**Worktree:** You want isolation. Codex creates a separate directory with its own branch. Your current checkout is untouched. Use this when:
- You want to try something without disturbing active work
- You want multiple tasks running in parallel

### 2. Parallel tasks with worktrees

Fire three tasks simultaneously. Each gets its own worktree on disk — its own directory, its own branch. They do not share files. When one finishes, review its diff, accept or discard, move on. The others are still running.

The professional rhythm: start of a session, write task briefs for everything well-scoped on your list, fire them all, go do the work that needs your brain, come back and review.

**Verify it yourself:** While tasks are running, check:
```bash
git worktree list
```
You will see the active worktree entries.

### 3. Handoff

You start something locally and decide you want to step away and let it run in the background. Handoff moves the work from a local session into a background worktree. You come back when it finishes.

### 4. Use /plan for complex tasks

Same as CLI: for anything where the scope is large or the direction is uncertain, use `/plan` first. Let Codex build a plan, review it, then execute.

### 5. The app has more in it than you think

Most people only ever use the task input box. Here is what else is in there.

**Open in VS Code.** When Codex is working in a worktree, click to open that worktree directly in VS Code. This is how to browse what Codex is actually doing — full editor view, separate window, the separation is intentional.

**Integrated terminal.** Every session has a built-in terminal scoped to the worktree directory. Run the test suite, check Git state, inspect a file — without leaving the app.

**Git workflow.** Staged changes, diff review, and commit — all from inside the app. You do not need to switch to the terminal for basic Git operations.

**Comment on diff lines.** When Codex produces a diff, you can leave comments on specific lines — exactly like a PR review. This changes review from binary (accept/reject) to conversational. You can say "this line is wrong, here is why" and iterate on just that part.

**Keyboard shortcuts worth knowing:**

| Shortcut | What it does |
|----------|-------------|
| `Cmd + Enter` | Submit the task |
| `Cmd + K` | Open command palette |
| `Cmd + /` | Toggle sidebar |
| `Escape` | Stop the current task |

### 6. Plugins

Plugins connect Codex to external tools. Instead of context-switching to a browser, you describe the task in natural language and Codex handles the tool interaction.

**The Linear plugin** is the one I use most. It gives Codex direct access to your Linear issues.

Install: Settings > Plugins > search "Linear" > Install. Authenticate when prompted.

What it enables:
- "Show me all open bugs assigned to me"
- "Create an issue for the pagination bug we just found"
- "Mark ENG-142 as in progress"
- Start a task brief directly from an issue: fetch the issue, use its description and acceptance criteria as your brief, mark it done with a comment when the diff is merged

This removes the copy-paste loop between your issue tracker and your coding session entirely.

See [`05-plugins/README.md`](05-plugins/README.md) for the full walkthrough and a list of other useful plugins.

### 7. Review the diff properly

When a task completes, you get a diff. Do not just scan it. Read it like a code review:

- Does it do what the task brief asked?
- Are the tests real or just asserting the happy path?
- Does it follow your project conventions?
- Did it touch anything outside the stated scope?

See [`03-review/code_review.md`](03-review/code_review.md) for the full review checklist. Reference it from your `AGENTS.md` so Codex applies it automatically with `/review`.

---

## Subagents

Codex can spawn parallel agents to handle specific subtasks, but only if you ask explicitly. Say "use parallel agents" or "delegate these in parallel" — it does not happen automatically.

Good use case:

> "Spawn one agent to look for security issues, one to find test gaps, and one for anything that looks fragile. Summarise the findings."

The subagents return summaries to the main thread. This keeps your main conversation clean and avoids context rot from verbose intermediate output (logs, stack traces, test results piling up).

Worth trying once you are comfortable with the basics.

---

## AGENTS.md: the context layer most developers ignore

Every task Codex runs reads `AGENTS.md` first. What belongs in it:

- How to run tests (`just test`, `pytest -x`, etc.)
- How to run the linter and type checker
- Project layout — where things live
- Conventions — naming, patterns to follow, what to avoid
- A reference to `code_review.md`

The quality difference between a blank `AGENTS.md` and a well-written one is real. Same task, same model, different context — noticeably different output.

Max 32KB. Does not support imports or references to other files. Everything that matters has to be inline.

See [`01-setup/AGENTS.md`](01-setup/AGENTS.md) for a well-structured example to copy and edit.

---

## Skills

Skills extend Codex with reusable workflows. A Skill is a `SKILL.md` file: frontmatter with `name` and `description`, full instructions in the body.

Store them at:
- `~/.agents/skills/` — personal, available in all projects
- `.agents/skills/` — repo-local, shared with your team

**Demo these through the CLI.** It is the clearest way to see what is happening — you can watch Codex load the skill instructions and apply them. Start the CLI in a project that has a skill installed, describe a task matching the skill, and Codex picks it up automatically.

```bash
# Add a skill globally
mkdir -p ~/.agents/skills/commit
# copy 04-skills/example-skill/SKILL.md there

# Start Codex in any project — the skill is now available everywhere
codex
```

See [`04-skills/example-skill/SKILL.md`](04-skills/example-skill/SKILL.md) for a working example (the `commit` skill).

Good first skills to write: commit (shown), code review, generate changelog, write tests for a file.

---

## Honest take: Codex vs Claude Code

Use both. They are not competing for the same use case.

**Codex wins on:**
- Parallel local work (worktrees)
- Well-scoped tasks with clear acceptance criteria
- Scriptable automation via `codex exec`
- Anything you would write a ticket for

**Claude Code wins on:**
- Interactive debugging where you are discovering the problem as you go
- Complex architectural decisions that require back-and-forth
- Long exploratory sessions where the acceptance criteria do not exist yet
- Anything where you need to redirect mid-task

The rule: if you can write a good task brief, reach for Codex. If you cannot, reach for Claude Code.

---

## Files in this repo

| File | What it is |
|------|-----------|
| [`01-setup/AGENTS.md`](01-setup/AGENTS.md) | Well-written AGENTS.md example to copy and edit |
| [`01-setup/config.toml`](01-setup/config.toml) | Default `~/.codex/config.toml` |
| [`02-task-briefs/template.md`](02-task-briefs/template.md) | Task brief template |
| [`02-task-briefs/good-example.md`](02-task-briefs/good-example.md) | Concrete good task brief |
| [`02-task-briefs/bad-example.md`](02-task-briefs/bad-example.md) | What not to do and why |
| [`03-review/code_review.md`](03-review/code_review.md) | Review checklist for diffs |
| [`04-skills/example-skill/SKILL.md`](04-skills/example-skill/SKILL.md) | Example skill (commit) |
| [`05-plugins/README.md`](05-plugins/README.md) | Plugin setup, Linear walkthrough |
| [`06-automation/justfile`](06-automation/justfile) | `codex exec` targets for your justfile |
