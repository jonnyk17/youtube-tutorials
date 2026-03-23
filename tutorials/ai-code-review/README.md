# 6 Levels of AI Code Review

Companion repo for the video. Everything you need to set up a complete AI code review pipeline.

## The 6 Levels

```
LOCAL (before push)
├── Level 1: Read the Diff (manual, 30 seconds)
├── Level 2: Built-in Commands (/review, /simplify)
├── Level 3: Automated Checks (hooks for linting, formatting)
├── Level 4: Custom Review with REVIEW.md (/blueprint:code-review)
└── Level 5: Third-Party Local Review (CodeRabbit)

REMOTE (on the PR)
└── Level 6: CI Review (Codex, CodeRabbit CI, Copilot)
```

Start at Level 1. Add layers as your codebase grows.

## Quick Start

### Level 3: Automated Hooks

Copy the hooks config into your project:

```bash
cp hooks/settings.json .claude/settings.local.json
```

This runs ESLint on every file edit. Swap `eslint` for your linter (ruff, mypy, prettier, etc.).

### Level 4: Custom Review with REVIEW.md

1. Copy the example REVIEW.md to your project root:

```bash
cp examples/REVIEW.md ./REVIEW.md
```

2. Edit it with your team's specific rules.

3. Install Blueprint and run a review:

```bash
# Install Blueprint plugin
/plugin marketplace add owainlewis/blueprint
/plugin install blueprint@owainlewis-blueprint

# Review your changes
/blueprint:code-review
```

### Level 5: CodeRabbit Local Review

```bash
# Install CodeRabbit CLI
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
coderabbit auth login

# Install the Claude Code plugin
/plugin install coderabbit

# Review your changes
/coderabbit:review
```

### Level 6: CI Review

**Codex on GitHub:**
- Enable in your Codex web settings
- Every PR gets automatically reviewed
- Included with ChatGPT Pro subscription

**CodeRabbit on GitHub:**
- Install the GitHub App: https://github.com/apps/coderabbitai
- Every PR gets automatically reviewed
- Free for open source

## Files in This Repo

```
ai-code-review/
├── README.md                    # This file
├── hooks/
│   ├── settings.json            # Claude Code hooks config (Level 3)
│   └── stop-hook.json           # Stop hook for automatic review (Level 4)
├── examples/
│   ├── REVIEW.md                # Example REVIEW.md for your project (Level 4)
│   └── agents-md-review.md      # Example agents.md review section for Codex (Level 6)
└── ARCHITECTURE.md              # Visual diagram of all 6 levels
```

## Related

- [Blueprint plugin](https://github.com/owainlewis/blueprint) - Full SDLC workflow including /code-review
- [CodeRabbit](https://coderabbit.ai) - AI code review (local CLI + GitHub App)
- [Codex](https://openai.com/codex) - OpenAI's coding agent with built-in code review
