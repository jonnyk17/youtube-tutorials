# Architecture: 5 Levels of AI Code Review

## AI Review vs Human Review

```
┌─────────────────────────────────────┐     ┌─────────────────────────────────────┐
│            AI REVIEW                 │     │           HUMAN REVIEW              │
│                                     │     │                                     │
│  Superior at:                       │     │  Superior at:                       │
│  pattern matching, speed,           │     │  judgement, context, strategy        │
│  consistency                        │     │                                     │
│                                     │     │  - Does this solve the problem?     │
│  - Security (OWASP, injection,      │     │  - Is this the right architecture?  │
│    secrets, XSS)                    │     │  - Does it meet acceptance criteria?│
│  - Bug detection (logic, null,      │     │  - Business logic verification      │
│    races, off-by-one)               │     │  - Will this break in 3 months?     │
│  - Style guide adherence            │     │  - Should we even build this?       │
│  - Scales to any volume             │     │                                     │
│  - Never gets tired                 │     │  5 min focused on the right things  │
│                                     │     │  > 30 min reading every line        │
└─────────────────────────────────────┘     └─────────────────────────────────────┘
```

## The Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   You write code with an AI agent (Claude Code, Cursor, etc.)   │
│                                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     QUALITY GATES (not review)                   │
│                                                                 │
│   Linting (ruff, eslint), formatting (black, prettier),         │
│   type checking (mypy, tsc). Deterministic. Automatic.          │
│   Run via hooks on every file edit. The foundation.             │
│                                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CODE REVIEW: LOCAL (before push)               │
│                                                                 │
│   Level 1: Read the Diff                                        │
│   Manual. 30 seconds. Correctness, blast radius, security.      │
│   Did the agent do only what you asked?                         │
│                                                                 │
│   Level 2: Self-Review                                          │
│   Prompt: "Review for bugs, security, over-engineering."        │
│   /simplify for cleanup. Same context. Quick.                   │
│                                                                 │
│   Level 3: Custom Review (REVIEW.md)                            │
│   Your rules, your stack, portable across any agent.            │
│   /blueprint:code-review or write your own command.             │
│   Stop hooks for automatic review on task completion.           │
│                                                                 │
│   Level 4: Third-Party Local Review                             │
│   /coderabbit:review (40+ scanners, SAST)                      │
│   Codex /review (4 presets, P0-P3 priority)                     │
│   Cross-model review: write with Claude, review with Codex.    │
│                                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                         git push
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CODE REVIEW: REMOTE (on the PR)                │
│                                                                 │
│   Level 5: CI Review                                            │
│                                                                 │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│   │    Codex      │  │  CodeRabbit  │  │  Anthropic           │  │
│   │  on GitHub    │  │     CI       │  │  /code-review        │  │
│   │              │  │              │  │  security-review      │  │
│   │  Full repo   │  │  40+ SAST    │  │                      │  │
│   │  access.     │  │  scanners.   │  │  4 parallel agents.  │  │
│   │  Tests its   │  │  Inline PR   │  │  Confidence scoring. │  │
│   │  hypotheses. │  │  comments.   │  │  $15-25/review       │  │
│   │  Included    │  │  Free for    │  │  (enterprise).       │  │
│   │  w/ ChatGPT. │  │  open source.│  │                      │  │
│   └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                                                 │
│   Cross-model: Claude writes, Codex reviews.                    │
│   Different models catch different things.                      │
│                                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       HUMAN REVIEW                              │
│                                                                 │
│   Architecture. Business logic. "Should we build this?"         │
│   What AI cannot judge.                                         │
│                                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                          MERGE
```

## What Each Level Catches

```
┌────────┬──────────────────────────────────────┬──────────────────────┐
│ Level  │ What it catches                      │ Cost / Effort        │
├────────┼──────────────────────────────────────┼──────────────────────┤
│ Gates  │ Lint errors, type errors, formatting │ Free. Automatic.     │
│ 1      │ Unexpected changes, wrong files      │ Free. 30 seconds.    │
│ 2      │ Obvious bugs, over-engineering       │ Free. 10 seconds.    │
│ 3      │ Project-specific rule violations     │ Free. Your rules.    │
│ 4      │ Security, SAST, coverage gaps        │ Free/Paid. Local.    │
│ 5      │ Architectural bugs, cross-file       │ Free/Paid. On PR.    │
│ Human  │ Business logic, architecture         │ Time. Judgement.     │
└────────┴──────────────────────────────────────┴──────────────────────┘
```

## The Key Insight

There is no perfect tool. AI catches things humans miss. Humans catch things AI misses. The value is in layering them.

Find a single reliable way to review locally. Layer CI on top as a safety net. Start simple. Add complexity only when you need it.
