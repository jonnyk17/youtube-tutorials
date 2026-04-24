# OpenAI Codex For Developers — Recording Guide

This README is the on-camera reference. Each section is one edit cut. Key line is what to anchor on. Demo steps are what to show.

---

## Section order

```
Hook → Three Ways → CLI → VS Code → Desktop App → Live Demo (Linear) → Automations → Pricing → System Layer + Tips → Outro
```

Boring stuff (pricing, setup) comes AFTER the demos. People care about cost once they've seen the value.

---

## SECTION 1 — Hook (talking head, ~1.5 min)

**Key line:** "This is the complete guide to OpenAI Codex."

- By the end you will know how to use it like a professional developer
- We will cover the CLI, the desktop app, and a full live demo where I build real features on a client project using Linear
- All files and resources are linked in the description

**Credibility (brief):** 20 years as a software engineer. Principal engineer, engineering manager, director of engineering. Currently building AI systems freelance and running an AI community.

**Honest framing:** I am not going to hype this. There are many good AI coding agents. Codex is worth your attention in 2026 because OpenAI models are genuinely top tier for coding.

---

## SECTION 2 — Three Ways to Use Codex (~30 sec, transition to screen share)

**Key line:** "There are three different ways to use Codex."

1. **The CLI** — if you like working in the terminal
2. **The desktop app** — the one I reach for most, designed for parallel work
3. **The VS Code extension** — if you want to stay inside your editor

> I use the desktop app and CLI most. That is what this video covers.

---

## SECTION 3 — CLI (screen share, ~3 min)

**Key line:** "Let's get straight into it. Here's how to install and use the CLI."

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

### Four things to show

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

No TUI, just output. This is where Codex becomes developer tooling, not just an app. Composes with the shell, justfiles, Git, CI.

### Sessions persist

```bash
codex resume       # opens a picker
codex resume --last
```

Your sessions are saved. You can always come back to where you left off.

### Demo steps

1. Run the install command
2. Open `codex`, type `/` to show the command list
3. Run `/init` in a real project, show the generated AGENTS.md
4. Run one `codex exec` task
5. Show `codex resume` opening the session picker

---

## SECTION 4 — VS Code Extension (~20 sec)

**Key line:** "There is also a VS Code extension if you prefer to stay inside your editor."

- Extensions panel, search Codex, install
- I keep Codex outside VS Code as a separate window. That is a preference, not a rule.

> Move on. The desktop app is where the video lives.

---

## SECTION 5 — Desktop App (screen share, ~7 min)

### 5a. Two modes that matter

**Key line:** "Two modes. Local for supervised work. Worktree for parallel isolated work."

| Mode | Use it for |
|---|---|
| Local | Small supervised tasks in your current checkout |
| Worktree | Isolated parallel work without touching your main branch |

---

### 5b. Local mode

**Key line:** "Local is supervised edits plus diff review. Nothing more."

- Works directly in the project directory you have open
- Use for small focused tasks: explain this module, add one test, one small fix
- Start from a clean Git state, write the task, let Codex work, check `/diff`

**Demo:** Give Codex one small task. Show it running. Show `/diff`.

---

### 5c. Worktree mode

**Key line:** "Worktrees let you run multiple Codex tasks without touching your current branch."

- Git worktrees give you multiple checkouts of the same repo on disk at the same time
- Each task gets its own directory and working state. Tasks do not block each other.
- Fire two or three tasks in parallel. Go do something else. Come back and review the diffs.

**Demo:** Fire two prepared tasks in Worktree. Show both running. Open a terminal in one worktree and run `git status`. Switch back to main checkout and show it is clean.

**Key moment:** Multiple tasks running, your current branch untouched.

---

### 5d. UI tour

**Key line:** "Most people never go past the task input box. Here is what is actually in the app."

Walk through in this order:

1. **Open in VS Code** — click to open the worktree directly in VS Code. I keep both windows side by side.
2. **Integrated terminal** — run commands in the worktree without switching windows
3. **Git diff view** — staged changes, commit from inside the app
4. **Line comments on diffs** — leave a comment on a specific line. Review is conversational, not binary accept/reject.
5. **Keyboard shortcuts** — `Cmd+Enter` submit, `Cmd+K` command palette, `Escape` stop

**Key moment:** Line commenting on diffs. Most viewers will not know this exists.

---

## SECTION 6 — Live Demo: Linear Workflow (screen share, ~5 min)

**Key line:** "Let me show you how I actually work on a real client project."

This is the peak value section. Show the Linear plugin in action. The point is: no context switching, no copy-paste, the whole loop stays inside Codex.

### Before you record

- Clean Git state
- AGENTS.md already set up (show it briefly, explain what it does)
- Linear plugin installed and authenticated
- One real ticket picked in advance — know the ID and the acceptance criteria
- A second smaller ticket ready to fire in Worktree

### Setup: install the Linear plugin

Before starting the workflow, show this once:

Settings > Plugins > Browse > Linear > Install

> Plugins give Codex access to external tools without you leaving the session. Linear is the one I use every day.

See: [`05-plugins/README.md`](05-plugins/README.md)

### The three context layers

Show these briefly before starting the task:

1. `AGENTS.md` — standing rules. How tests run, project layout, the Linear workflow.
2. Linear ticket — today's task. Outcome, acceptance criteria, constraints. Not implementation steps.
3. `docs/product-spec.md` (if relevant) — what the product is, what is out of scope.

> AGENTS.md is the standing rules. The ticket is today's work. Together, that is everything Codex needs.

### The workflow

**Step 1 — Pull the ticket from Linear**

Ask Codex to fetch the ticket:

> "Show me the details for [ticket ID]"

Codex reads the title, description, and acceptance criteria directly from Linear.

> "I do not need to copy-paste anything. Codex has the ticket. It knows the AGENTS.md. That is everything it needs."

**Step 2 — Fire the task**

Run it. While it is working, fire a second smaller ticket in Worktree.

> "I am not sitting here watching. I am getting on with something else while Codex works."

**Step 3 — Review the diff**

Walk through the diff. Accept what looks right. Flag one thing to tweak if there is one.

> "Codex produced a diff. My job is to review it like a PR from a junior engineer."

**Step 4 — Close the loop in Linear**

> "Mark that ticket as done and add a comment summarising what was built."

> Full loop. Ticket in Linear, built with Codex, diff reviewed, ticket closed. No context switching, no manual status updates.

---

## SECTION 7 — Automations (screen share, ~1.5 min)

**Key line:** "One more feature worth showing: automations."

Automations let you set up recurring tasks that run on a schedule, without you having to remember them.

### Good example: check for stale dependencies

In the desktop app, create a new automation:

> "Check this project for stale or outdated dependencies. List anything that is significantly behind with a short note on whether it is worth updating."

Set it to run weekly.

> "Now I get a dependency health check every week without thinking about it. This is the kind of maintenance work that always slips if you have to do it manually."

Other examples worth mentioning:
- Weekly standup summary: "Summarise what changed in this repo this week"
- Branch check-in: "Check if there are any open branches older than two weeks"

> Automations are for repeated jobs you would otherwise forget to do.

---

## SECTION 8 — Pricing (talking head, ~45 sec)

**Key line:** "Everything I just showed you is available on the $20 a month ChatGPT Plus plan."

- Standard $20 plan. Not pro, not API-only. Full access to the desktop app, CLI, and the full model.
- Rate limits are better than I expected. I have not hit a wall in normal use on real client work.
- If you are on the fence, the $20 plan is a reasonable place to start.

> This section comes AFTER the demo because now they understand what $20 buys.

---

## SECTION 9 — System Layer + Tips (screen share, ~3 min)

**Key line:** "A few things that will make you significantly better at using this."

### AGENTS.md

The operating manual for Codex on a project. Test commands, project layout, commit conventions, and the Linear workflow. Keep it short.

> Do not put things in AGENTS.md that Codex can figure out itself. That gets stale fast and creates noise.

Run `/init` to generate a starting point.

See: [`01-setup/AGENTS.md`](01-setup/AGENTS.md)

### Skills

Reusable workflows stored as a `SKILL.md` file. Use when you repeat the same kind of task across projects.

Type `$` in Codex to see your available skills.

Store personal skills in `~/.agents/skills/` and they are available everywhere.

> A skill is a reusable playbook for a task you do often. Write it once, use it everywhere.

See: [`04-skills/plan-skill/SKILL.md`](04-skills/plan-skill/SKILL.md)

### Quick tips

- **Fork** — `/fork` copies the current session before trying something risky. You keep your progress and can explore a different direction.
- **Fast mode** — `/fast` runs tasks quicker but costs more credits. Use for low-stakes work like formatting or docstrings.
- **Mention files** — `/mention path/to/file` when you want Codex to look at a specific file instead of guessing.
- **Subagents** — ask explicitly: "Spawn one agent to check for security issues, one for test gaps, one for anything brittle. Summarise the findings."

---

## SECTION 10 — Honest Take + Outro (talking head, ~1 min)

**Key line:** "I really like Codex. The desktop app has become a genuine part of my daily workflow."

- Multiple sessions, multiple projects, clean diff review. It feels like a proper developer tool.
- I still use Claude Code every day. They are not competing for the same thing.
  - Codex is for delegation: well-scoped tasks, parallel work, things you can hand off and review
  - Claude Code is for interactive reasoning: debugging, architecture, figuring things out as you go
- Use both.

**CTA:**

Companion repo is linked in the description. Everything I showed today is in there.

AI Engineer on Skool — $79 a month, built for engineers doing real work with these tools. Link in the description.

If you are a company building AI systems and want someone to do it for you, my agency Gradient Work handles that.

Subscribe if this was useful. One video a week.

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
