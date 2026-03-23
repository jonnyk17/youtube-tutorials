# 5 Levels of AI Code Review

Companion repo for the video. Everything you need to set up a complete AI code review pipeline.

## The 5 Levels

```
QUALITY GATES (set up first, not review)
└── Linting, formatting, type checking via hooks

LOCAL (before push)
├── Level 1: Read the Diff (manual, 30 seconds)
├── Level 2: Self-Review (/simplify, prompt it)
├── Level 3: Custom Review with REVIEW.md (write your own, /blueprint:code-review)
└── Level 4: Third-Party Local Review (CodeRabbit, Codex /review)

REMOTE (on the PR)
└── Level 5: CI Review (Codex on GitHub, CodeRabbit CI, claude-code-security-review)
```

Start at Level 1. Add layers as your codebase grows.

## Quick Start

### Quality Gates: Automated Hooks

Copy the hooks config into your project:

```bash
cp hooks/settings.json .claude/settings.local.json
```

This runs ruff on every Python file edit. Swap for your stack's linter.

### Level 3: Custom Review with REVIEW.md

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

Or write your own review command. See `examples/codex-review-prompt.md` for an excellent reference prompt to adapt.

### Level 4: CodeRabbit Local Review

```bash
# Install CodeRabbit CLI
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
coderabbit auth login

# Install the Claude Code plugin
/plugin install coderabbit

# Review your changes
/coderabbit:review
```

### Level 5: CI Review

**Codex on GitHub:**
- Enable in your Codex web settings
- Every PR gets automatically reviewed
- Included with ChatGPT Plus subscription

**CodeRabbit on GitHub:**
- Install the GitHub App: https://github.com/apps/coderabbitai
- Free for open source

**Claude Code Security Review (GitHub Action):**
- https://github.com/anthropics/claude-code-security-review
- Security-focused review using Opus. Covers OWASP, injection, auth, secrets, XSS.

## Files in This Repo

```
ai-code-review/
├── README.md
├── ARCHITECTURE.md                      # Visual diagram of all 5 levels
├── hooks/
│   ├── settings.json                    # Post-edit lint hook (ruff)
│   └── stop-hook.json                   # Stop hook for automatic AI review
└── examples/
    ├── REVIEW.md                        # Example review rules for your project
    ├── codex-review-prompt.md           # OpenAI's review prompt (great reference)
    ├── agents-md-review.md              # Review section for agents.md (Codex)
    └── real-world-reviews.md            # Real examples + key takeaway
```

## Related

- [Blueprint plugin](https://github.com/owainlewis/blueprint) - Full SDLC workflow including /code-review with REVIEW.md support
- [CodeRabbit](https://coderabbit.ai) - AI code review (local CLI + GitHub App)
- [Codex](https://openai.com/codex) - OpenAI's coding agent with built-in /review
- [Codex review prompt source](https://github.com/openai/codex/blob/main/codex-rs/core/review_prompt.md) - One of the best review prompts available
- [claude-code-security-review](https://github.com/anthropics/claude-code-security-review) - Anthropic's security-focused GitHub Action
- [Greptile](https://greptile.com) - Codebase-aware code review
