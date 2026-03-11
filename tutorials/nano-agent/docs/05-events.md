# 05 - Events

This is where it gets interesting. The event system is what turns a toy loop into a real tool. And it is the pattern that Claude Code uses for its hooks system.

## The Problem

Without events, the loop has print statements everywhere:

```python
# This gets messy fast
print(f"Calling {tool_name}...")
result = execute(tool_name, input)
print(f"Result: {result}")
```

Now you want to add an approval gate. And a spinner. And logging to a file. Each one needs to run at a different point in the loop, and they all interact. Your clean 50-line loop turns into 200 lines of tangled logic.

## The Solution

Instead of embedding behavior in the loop, the loop emits typed events. Listeners subscribe to those events and do whatever they want.

### Event Types

Each observable action is a dataclass:

```python
@dataclass
class ToolCall:
    name: str
    input: dict
    tool_use_id: str

@dataclass
class ToolResult:
    name: str
    output: str
    tool_use_id: str

@dataclass
class ThinkingDelta:
    text: str

@dataclass
class AgentResponse:
    content: str

@dataclass
class SubAgentStart:
    task: str

@dataclass
class SubAgentEnd:
    task: str
    result: str

@dataclass
class Error:
    message: str
```

### The Emit Factory

```python
def make_emit(*listeners):
    def emit(event):
        for listener in listeners:
            listener(event)  # may raise PermissionError
    return emit
```

That is it. `make_emit` takes listener functions and returns an `emit` callable. When the loop calls `emit(event)`, every listener gets the event. If any listener raises `PermissionError`, the loop treats the tool call as denied.

### Using It

```python
# In main.py
emit = make_emit(ui_listener, approval_listener, my_custom_listener)

# In agent.py (the loop)
emit(ToolCall(block.name, block.input, block.id))
```

## Why This Is Powerful

**Adding behavior never changes the loop.** Want to log every tool call to a file? Write a listener. Want to send a Slack notification when the agent finishes? Write a listener. Want to block dangerous commands? Write a listener. The loop stays the same.

**Listeners compose.** You can stack as many as you want. Each one handles the events it cares about and ignores the rest:

```python
def my_logger(event):
    if isinstance(event, ToolCall):
        log_to_file(f"Tool: {event.name}")

def my_monitor(event):
    if isinstance(event, Error):
        send_alert(event.message)
```

## The Claude Code Connection

This is exactly how Claude Code hooks work:

| nano-agent | Claude Code |
|-----------|------------|
| `ToolCall` event | `PreToolUse` hook |
| `ToolResult` event | `PostToolUse` hook |
| listener function | hook shell command |
| `raise PermissionError` | exit code 2 (deny) |

When you configure a Claude Code hook, you are writing a listener. When your hook exits with code 2, you are raising PermissionError. Same pattern, different packaging.

Next: [Approval Gate](06-approval-gate.md)
