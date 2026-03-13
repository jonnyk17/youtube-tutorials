# Claude Code Hooks for Automated Quality

These hook configurations make quality checks automatic. Copy the relevant sections into your `.claude/settings.json` or `.claude/settings.local.json`.

## Available Hooks

### 1. Auto-lint after every edit

Runs your linter automatically every time Claude edits or creates a file.

**JavaScript/TypeScript:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx eslint --fix 2>/dev/null || true",
            "statusMessage": "Linting..."
          }
        ]
      }
    ]
  }
}
```

**Python:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs ruff check --fix 2>/dev/null || true",
            "statusMessage": "Linting..."
          }
        ]
      }
    ]
  }
}
```

### 2. Auto-format after every edit

**JavaScript/TypeScript:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null || true",
            "statusMessage": "Formatting..."
          }
        ]
      }
    ]
  }
}
```

**Python:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs ruff format 2>/dev/null || true",
            "statusMessage": "Formatting..."
          }
        ]
      }
    ]
  }
}
```

### 3. AI review when Claude finishes a task

Runs a lightweight review agent every time Claude completes a response. The review agent checks for obvious issues and sends Claude back to fix them if found.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Review the changes made in this session. Check for: 1) Security issues (hardcoded secrets, injection, missing auth) 2) Obvious bugs (null handling, off-by-one, logic errors) 3) CLAUDE.md violations. Only flag issues you are 90%+ confident about. If no issues found, respond with {\"ok\": true}. If issues found, respond with {\"ok\": false, \"reason\": \"Brief description of each issue\"}.",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

### 4. Block commits with secrets

Prevents committing files that contain potential secrets.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "input=$(cat); cmd=$(echo \"$input\" | jq -r '.tool_input.command // empty'); if echo \"$cmd\" | grep -qE '^git commit'; then changed=$(git diff --cached --name-only); for f in $changed; do if grep -qEi '(sk_live|sk-[a-zA-Z0-9]{20,}|AKIA[A-Z0-9]{16}|password\\s*=\\s*[\"'\\'']((?!process\\.env|os\\.environ).){3,})' \"$f\" 2>/dev/null; then echo \"Potential secret found in $f\" >&2; exit 2; fi; done; fi"
          }
        ]
      }
    ]
  }
}
```

## Combining Hooks

You can combine multiple hooks in one settings file. Here's a complete example:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null || true",
            "statusMessage": "Formatting..."
          },
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx eslint --fix 2>/dev/null || true",
            "statusMessage": "Linting..."
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Review the changes made in this session for security issues, obvious bugs, and CLAUDE.md violations. Only flag issues you are 90%+ confident about. Respond with {\"ok\": true} if clean or {\"ok\": false, \"reason\": \"issues\"} if not.",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

## Installation

Copy the hook config into your project:

```bash
# Project-level settings (gitignored, local only)
# Merge into .claude/settings.local.json

# Project-level settings (shared with team)
# Merge into .claude/settings.json
```

Or apply globally:
```bash
# Merge into ~/.claude/settings.json
```
