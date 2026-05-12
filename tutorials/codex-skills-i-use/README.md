# 7 Codex Skills I Use As An AI Engineer

Companion repo for the YouTube video. Seven agent skills that handle the majority of my day-to-day work as a solo AI engineer, packaged up so you can clone them and use them yourself.

> The thesis: you don't need hundreds of skills to be productive with AI coding agents. You need a small number of focused, well-written ones — most under 30 lines — that act as standard operating procedures for things you do every day.

## The skills

Grouped by phase of work. Three of these aren't for the agent at all — they're for **you**, for thinking, comprehension, and design before any code gets written.

### Plan & Design

| # | Skill | For | What it does |
|---|---|---|---|
| 1 | [Design Doc](./resources/skills/design-doc) | Human | Think through architecture and tradeoffs before handing off to an agent. The kind of doc a working engineer at Google or Amazon would write. |
| 2 | [Spec](./resources/skills/spec) | Agent | Turn a feature or concept into an agent-ready brief — requirements, approach, constraints. Aligns the agent before any code is written. |
| 3 | [Plan](./resources/skills/plan) | Agent | Break a spec into discrete tasks an agent can execute one by one, and push them to GitHub Issues or Linear. |
| 4 | [Excalidraw Diagram](./resources/skills/excalidraw-diagram) | Human | Generate clean technical diagrams from a prompt. |
| 5 | [Explain Visually](./resources/skills/explain-visually) | Human | Generate an HTML walkthrough of any concept, codebase, or architecture. Richer than markdown, scannable in the browser. |

### Code

| # | Skill | For | What it does |
|---|---|---|---|
| 6 | [Refactor](./resources/skills/refactor) | Code | Improve code quality without changing behavior. Adapted from the Claude Code simplify pattern. |

### Review

| # | Skill | For | What it does |
|---|---|---|---|
| 7 | [Address PR Feedback](./resources/skills/address-pr-feedback) | Agent | Read review comments on a GitHub PR, apply the fixes, reply to each thread. Automates the post-review loop. |

## Install

Codex looks for skills in two places:

- **`~/.codex/skills/`** — user-level, available across every project.
- **`<repo>/.codex/skills/`** — project-level, scoped to one codebase.

### User-level (most common)

```bash
git clone https://github.com/owainlewis/youtube-tutorials
cd youtube-tutorials/tutorials/codex-skills-i-use
mkdir -p ~/.codex/skills
cp -r resources/skills/* ~/.codex/skills/
```

### Project-level

```bash
cd <your-project>
mkdir -p .codex/skills
cp -r /path/to/youtube-tutorials/tutorials/codex-skills-i-use/resources/skills/* .codex/skills/
```

### Verify

Open Codex in any project:

```bash
codex
```

Then `/skills` to list available skills. The seven above should appear. Invoke any of them with `$<skill-name>`, e.g. `$spec` or `$explain-visually`.

## Layout

```
codex-skills-i-use/
├── README.md
└── resources/
    └── skills/
        ├── spec/
        ├── explain-visually/
        ├── plan/
        ├── design-doc/
        ├── excalidraw-diagram/
        ├── address-pr-feedback/
        └── refactor/
```

Each skill is a folder containing a `SKILL.md` file. Some include scripts or references; check the folder for details.

## Watch the video

(Link added after publication.)
