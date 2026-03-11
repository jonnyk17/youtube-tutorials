# 06 - Approval Gate

The approval gate lets you allow or deny tool calls before they execute. It is a safety mechanism built entirely on top of the event system.

## How It Works

The approval gate is just a listener:

```python
def approval_listener(auto_approve: list[str]):
    def listener(event):
        if not isinstance(event, ToolCall):
            return
        if event.name in auto_approve:
            return
        answer = input(f"Allow {event.name}? [y/n] ").strip().lower()
        if answer != "y":
            raise PermissionError(f"User denied {event.name}")
    return listener
```

When the loop emits a `ToolCall` event, this listener:
1. Ignores non-ToolCall events
2. Auto-approves safe tools (read_file, list_directory, grep)
3. Prompts the user for everything else
4. Raises `PermissionError` to veto

The loop catches the `PermissionError` and sends "Tool call denied by user." back to Claude as the tool result. Claude sees the denial and adapts.

## Configuration

In `config.yaml`:

```yaml
approval:
  enabled: false
  auto_approve:
    - read_file
    - list_directory
    - grep
```

Or from the command line:

```bash
uv run nano-agent --approve "Refactor the auth module"
```

## What Happens When a Tool Is Denied

The agent doesn't crash. It sees the denial message and adjusts:

```
> bash `rm -rf /tmp/test`
  Allow bash? [y/n] n
  > (agent sees "Tool call denied by user.")
  > (agent tries a different approach or asks for guidance)
```

This works because the denial is just another tool result. The message list records what happened, and Claude reasons about it on the next turn.

## Auto-Approve vs Prompt

Read-only tools are safe to auto-approve. They can't modify anything:
- `read_file` - just reads
- `list_directory` - just lists
- `grep` - just searches

Write operations should prompt:
- `bash` - could run anything
- `write_file` - modifies the filesystem
- `run_subagents` - spawns new agents

This mirrors how Claude Code handles permissions. Some tools are always allowed, others require explicit consent.

Next: [Sub-Agents](07-sub-agents.md)
