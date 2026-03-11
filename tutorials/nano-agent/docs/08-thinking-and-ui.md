# 08 - Thinking and UI

The finishing touches. Extended thinking makes Claude's reasoning visible. The Rich UI makes the terminal output clean and readable.

## Extended Thinking

Extended thinking is a Claude feature that lets you see the model's reasoning process before it responds. Enabling it takes one change in the provider:

```python
thinking = config.get("thinking", {})
if thinking.get("enabled"):
    kwargs["thinking"] = {
        "type": "enabled",
        "budget_tokens": thinking.get("budget_tokens", 10000),
    }
```

When thinking is enabled, the response includes `thinking` blocks alongside the usual `text` and `tool_use` blocks:

```json
{
  "content": [
    {"type": "thinking", "thinking": "Let me look at this code first..."},
    {"type": "tool_use", "name": "read_file", "input": {"file_path": "auth.py"}}
  ]
}
```

The loop handles this with two lines:

```python
for block in response.content:
    if block.type == "thinking":
        if emit: emit(ThinkingDelta(block.thinking))
```

One API parameter, one event type, and you can see Claude reasoning about your code.

## The Rich UI

We use the `rich` library for terminal output. The UI is a single event listener:

```python
def ui_listener(event):
    match event:
        case ToolCall(name=name, input=inp):
            color = TOOL_COLORS.get(name, "white")
            summary = _summarize_input(name, inp)
            console.print(f"  [{color}]> {name}[/{color}] {summary}")

        case ToolResult(name=name, output=output):
            preview = output.strip().split("\n")[0][:120]
            console.print(f"    [dim]{preview}[/dim]")

        case ThinkingDelta(text=text):
            console.print(f"  [blue italic]{text[:200]}[/blue italic]")

        case AgentResponse(content=content):
            console.print(Panel(content, title="Agent", border_style="green"))

        # ... sub-agent and error events
```

### Color Coding

Each tool type has a color so you can scan the output quickly:
- Yellow: bash (watch these closely)
- Green: file operations
- Cyan: search operations
- Magenta: sub-agents
- Blue: thinking

### The Splash Screen

A small touch that makes the agent feel like a real tool:

```python
def splash():
    text = Text("nano-agent", style="bold white")
    text.append("\n  a minimal coding agent", style="dim")
    console.print(Panel(text, border_style="blue", padding=(1, 2)))
```

## Putting It All Together

In `main.py`, everything is wired up:

```python
# Build listeners
listeners = [ui_listener]
if approval_enabled:
    listeners.insert(0, approval_listener(auto_approve))

# Compose the emit function
emit = make_emit(*listeners)

# Wire up sub-agents
init_subagents(config, emit)

# Run
splash()
result = asyncio.run(run(task, config, emit=emit))
```

The approval listener goes first so it can veto before the UI renders. The UI listener renders everything that was not vetoed.

## The Final File Structure

```
src/nano_agent/
  main.py      # CLI, config, listener wiring     (~95 lines)
  agent.py     # The loop + sub-agent runner       (~125 lines)
  provider.py  # Anthropic API wrapper             (~33 lines)
  tools.py     # Registry + 5 tools + sub-agents   (~186 lines)
  events.py    # 7 event types + emit factory      (~69 lines)
  ui.py        # Terminal rendering                 (~87 lines)
```

## What is Next

This agent works. You can point it at real code and it will read, write, refactor, and test. But it is missing things a production agent needs:

- **Streaming** so you see responses as they generate
- **Context compaction** so the message list doesn't grow forever
- **Session persistence** so you can resume conversations
- **MCP** so tools can be discovered dynamically
- **Retry logic** so transient API errors don't kill the agent

Each of these would be a great follow-up project. But the core loop stays the same.

Back to: [README](../README.md)
