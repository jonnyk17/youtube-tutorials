# AI Git Workflow

> Codify your git conventions in a config file. Let AI enforce them on every commit.

---

## The Idea

Most developers use AI coding agents to write code. But AI agents are just as good — honestly, more consistent — at managing your entire git workflow.

The key is a config file. You write your conventions once — commit format, branch naming, PR template, safety rules — and the agent follows them on every operation. You get consistency you couldn't achieve when humans were doing it from memory.

This works with any coding agent that supports a markdown config: Claude Code (`CLAUDE.md`), Codex (`AGENTS.md`), Cursor (`.cursorrules`), or similar.

---

## Setup

1. Copy the `CLAUDE.md` from this folder into the root of your project
2. Adjust the conventions to match your team's style
3. Open your AI coding agent — the config is loaded automatically

---

## The Config

The `CLAUDE.md` in this repo covers:

- **Branch naming** — `feature/`, `fix/`, `chore/` with kebab-case
- **Commit messages** — conventional commits, body explains WHY not WHAT
- **Atomic commits** — one logical change per commit
- **Safety checks** — no secrets, no debug statements, no commented-out code
- **PR template** — What / Why / How to test
- **Hard rules** — never commit to main, never force push, squash and merge

It's ~30 lines. You're not teaching the agent how git works — you're telling it which conventions to follow.

---

## Example Workflows

### Create a branch

```
create a feature branch for password validation
```

The agent creates `feature/password-validation` following the naming convention from the config.

### Commit changes

```
commit the auth changes
```

The agent reads the diff, stages the relevant files, and writes a conventional commit with a descriptive body. If you made unrelated changes (e.g. a feature + a typo fix), it separates them into multiple commits automatically.

### Open a pull request

```
push this branch and open a PR against main
```

The agent pushes the branch, then uses the GitHub CLI to create a PR with a title and description following the template from the config (What / Why / How to test).

### Check CI and merge

```
what's the CI status on this PR?
```

```
squash and merge the PR
```

The agent checks the status, squashes the commits, merges, and cleans up the branch.

### Resolve a merge conflict

```
merge feature-branch into main and resolve any conflicts
```

The agent handles the merge. If there's a conflict, it reads both versions, understands the intent of each change, and combines them — rather than just picking one side.

### Rebase onto main

```
rebase this branch onto the latest main
```

The agent pulls the latest main and rebases your branch, resolving any minor conflicts along the way.

### Squash commits

```
squash my last 4 commits into one clean commit
```

The agent combines the commits and writes a coherent summary message — not just the first commit pasted in.

### Cherry-pick a specific change

```
cherry-pick just the auth fix from feature-branch and apply it to main
```

The agent finds the right commit by reading the messages and applies it cleanly. No hunting for commit hashes.

### Undo a mistake

```
undo my last commit but keep the changes
```

```
I accidentally committed to main — move those changes to a new branch
```

### Check history

```
what changed in the last 3 commits?
```

```
who last changed this function and why?
```

---

## What AI Does Better

The point isn't just convenience. AI raises the quality bar:

| Operation | Without AI | With AI |
|-----------|-----------|---------|
| Commit messages | "fix stuff", "updates", "WIP" | Descriptive conventional commits with context |
| Staging | `git add .` — everything in one commit | Separates unrelated changes into atomic commits |
| Secrets | Accidentally committed `.env` at least once | Catches secrets before they hit the repo |
| PR descriptions | Empty, or copy-pasted commit messages | Synthesized summary from the full diff |
| Merge conflicts | Pick one side and hope | Understands intent of both branches |
| Consistency | Varies by engineer, time of day, mood | Same standard on every commit |

---

## Sharing With Your Team

Check the config file into your repo. Every engineer's AI agent reads the same file and follows the same conventions automatically.

This replaces the wiki page nobody reads. The conventions are codified and enforced on every commit, by every engineer, without anyone having to remember the rules.

---

## Files

```
ai-git-workflow/
├── CLAUDE.md    # Git conventions config (copy this into your project)
└── README.md    # This guide
```

---

## License

MIT
