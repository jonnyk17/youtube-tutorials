# AI Code Review Skills for Claude Code

A collection of focused code review skills, hooks, and agent configurations for Claude Code. Each skill is a specialized reviewer that checks for one category of issues. Run them individually or as a team for comprehensive review.

## The Problem

AI-generated code has 1.7x more issues than human-written code. 75% more logic bugs. 41% higher churn rate. Nearly 40% of committed code is now AI-generated, and review capacity hasn't kept up.

These skills help you catch issues before they ship.

## Skills

| Skill | What It Checks |
|-------|---------------|
| **security-reviewer** | OWASP top 10, hardcoded secrets, auth issues, injection, input validation |
| **code-simplifier** | Unnecessary complexity, dead code, duplication, over-engineering |
| **convention-checker** | CLAUDE.md compliance, naming, file structure, API patterns |
| **dependency-auditor** | Outdated packages, known CVEs, unused deps, duplicates |
| **documentation-checker** | Stale comments, outdated README, missing docs, dead TODOs |

## Quick Start

### Install a single skill

Copy any skill folder into your project's `.claude/skills/` directory:

```bash
cp -r skills/security-reviewer .claude/skills/
```

### Install all skills

```bash
cp -r skills/* .claude/skills/
```

### Install hooks (auto-lint, auto-format on every edit)

Copy the hooks configuration into your Claude Code settings:

```bash
# Project-level (recommended)
cat hooks/settings.json
# Merge into your .claude/settings.json
```

## Usage

### Review current changes

Ask Claude to use a specific reviewer:

```
Review my recent changes for security issues
```

```
Simplify the code I just wrote
```

```
Check if my code follows project conventions
```

### Run all reviewers as a team

```
Run a full code review on my recent changes using all review skills
```

### Periodic codebase audit

```
Audit the entire codebase for security vulnerabilities
```

```
Find all outdated dependencies and known CVEs
```

```
Check for documentation rot across the project
```

## Automatic Review (Hooks)

The `hooks/` directory contains Claude Code hook configurations that run checks automatically:

- **Post-edit lint**: Runs your linter after every file edit
- **Post-edit format**: Runs your formatter after every file edit
- **Stop review**: Runs a quick review agent when Claude finishes a task

See [hooks/README.md](hooks/README.md) for setup instructions.

## Building Your Own Skills

Each skill follows a simple pattern:

```
skill-name/
  SKILL.md      # Description, triggers, and overview
  AGENTS.md     # Full instructions for the reviewing agent
  rules/        # Individual rule files (one per check)
    rule-name.md
```

The `rules/` directory makes skills modular. Add, remove, or customize individual rules without touching the core skill. See any existing skill as a template.

## Philosophy

- **Focused over general.** Each skill checks one category of issues well, rather than checking everything poorly.
- **Low noise.** Only flag issues you're confident about. False positives erode trust.
- **Actionable.** Every issue flagged should include a specific fix, not just a warning.
- **Composable.** Skills work alone or together. Mix and match for your workflow.
