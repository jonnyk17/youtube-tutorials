# Architecture: 6 Levels of AI Code Review

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
│                       LOCAL (before push)                        │
│                                                                 │
│   Level 1: Read the Diff                                        │
│   Manual. 30 seconds. Did it do what you asked?                 │
│   Did it touch files you didn't expect?                         │
│                                                                 │
│   Level 2: Built-in Review Commands                             │
│   /review  -> general feedback on recent changes                │
│   /simplify -> reduce complexity, remove over-engineering       │
│   Same context window. Quick self-check.                        │
│                                                                 │
│   Level 3: Automated Checks (Hooks)                             │
│   Linting, formatting, type checking.                           │
│   Runs automatically on every edit via Claude Code hooks.       │
│   Deterministic. 100% precision. Zero effort.                   │
│                                                                 │
│   Level 4: Custom Review with REVIEW.md                         │
│   Your team's specific rules encoded in a file.                 │
│   /blueprint:code-review reads REVIEW.md automatically.         │
│   Stop hooks can trigger review on every task completion.       │
│                                                                 │
│   Level 5: Third-Party Local Review                             │
│   /coderabbit:review -> purpose-built review tool               │
│   40+ linters, SAST scanners, false positive filtering.         │
│   A step up from DIY review skills.                             │
│                                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                         git push
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       REMOTE (on the PR)                        │
│                                                                 │
│   Level 6: CI Review                                            │
│                                                                 │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│   │    Codex      │  │  CodeRabbit  │  │  Copilot / Anthropic │  │
│   │              │  │     CI       │  │     Code Review      │  │
│   │  Full repo   │  │  40+ SAST    │  │  Built into GitHub / │  │
│   │  access.     │  │  scanners.   │  │  Claude ecosystem.   │  │
│   │  Traces      │  │  Inline PR   │  │                      │  │
│   │  deps.       │  │  comments.   │  │                      │  │
│   │  Tests its   │  │  Free for    │  │                      │  │
│   │  hypotheses. │  │  open source.│  │                      │  │
│   └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                                                 │
│   Cross-model review: Claude writes, Codex reviews.             │
│   Different models catch different things.                      │
│                                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       HUMAN REVIEW                              │
│                                                                 │
│   Architecture decisions. Business logic. "Should we even       │
│   build this?" Integration concerns. What AI can't judge.       │
│                                                                 │
│   5 min of human review on the right things >                   │
│   30 min reading every line.                                    │
│                                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                          MERGE


## What Each Level Catches

┌────────┬──────────────────────────────────┬─────────────────────┐
│ Level  │ What it catches                  │ Cost / Effort       │
├────────┼──────────────────────────────────┼─────────────────────┤
│ 1      │ Unexpected changes, wrong files  │ Free. 30 seconds.   │
│ 2      │ Obvious bugs, over-engineering   │ Free. 10 seconds.   │
│ 3      │ Lint errors, type errors, format │ Free. Automatic.    │
│ 4      │ Project-specific rule violations │ Free. Automatic.    │
│ 5      │ Security, SAST, coverage gaps    │ Free/Paid. Local.   │
│ 6      │ Architectural bugs, cross-file   │ Free/Paid. On PR.   │
│ Human  │ Business logic, architecture     │ Time. On PR.        │
└────────┴──────────────────────────────────┴─────────────────────┘
```

## The Key Insight

Each level catches a different class of issue. No single level catches everything.
The earlier you catch a bug, the cheaper it is to fix.

```
Level 1-2:  "Did the agent do what I asked?"
Level 3:    "Is the code syntactically correct?"
Level 4:    "Does it follow our team's rules?"
Level 5:    "Is it secure and well-tested?"
Level 6:    "Does it work in the context of the full codebase?"
Human:      "Is this the right approach?"
```

Start at Level 1. Add layers as you need them.
