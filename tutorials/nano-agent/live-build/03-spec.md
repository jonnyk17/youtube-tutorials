# Spec: nano-agent

This is the spec we hand to Claude Code to implement.

## Overview

Build a minimal coding agent in Python. Uses the Anthropic API (Claude) as the LLM. Runs in the terminal. Completes coding tasks autonomously.

## Architecture

```
User Task (string)
    |
    v
main.py         CLI entry, config loading, listener setup
    |
    v
agent.py        The loop: call LLM -> process response -> execute tools -> repeat
    |           |
    v           v
provider.py   tools.py    LLM abstraction / Tool registry + handlers
    |
    v
events.py       Typed events, emit system, listener composition
    |
    v
ui.py           Rich terminal output (colors, panels)
```

## Core Loop (agent.py)

```python
async def run(task, config, emit=None, is_subagent=False, messages=None):
    if messages is None:
        messages = []
    messages.append({"role": "user", "content": task})
    tools = get_tool_schemas(include_subagents=not is_subagent)

    for turn in range(config["max_turns"]):
        response = call_llm(messages, tools, config)

        # Handle thinking blocks
        for block in response.content:
            if block.type == "thinking" and emit:
                emit(ThinkingDelta(block.thinking))

        if response.stop_reason == "end_turn":
            messages.append({"role": "assistant", "content": response.content})
            text = next((b.text for b in response.content if b.type == "text"), "")
            if emit: emit(AgentResponse(text))
            return text

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type != "tool_use": continue
                if emit:
                    try:
                        emit(ToolCall(block.name, block.input, block.id))
                    except PermissionError:
                        tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": "Tool call denied by user."})
                        continue
                result = await execute_tool(block.name, block.input)
                if emit: emit(ToolResult(block.name, result, block.id))
                tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
            messages.append({"role": "user", "content": tool_results})

    return "Max turns reached."
```

## Provider (provider.py)

Wrap the Anthropic API. Accept messages, tools, config. Return the response. Support extended thinking via config flag. The agent loop should never import anthropic directly.

## Tools (tools.py)

Registry pattern with a decorator:

```python
@tool(name, description, parameters)
def my_tool(...) -> str:
    ...
```

Built-in tools:
- **bash** - Run shell commands (timeout: 120s)
- **read_file** - Read file contents
- **write_file** - Write content to a file (create parent dirs)
- **grep** - Search for patterns (required: pattern only, path and include optional)
- **list_directory** - List directory contents (path optional, defaults to ".")
- **run_subagents** - Run parallel sub-agents (only available to top-level agent)

## Events (events.py)

Typed dataclasses:
- ToolCall(name, input, tool_use_id)
- ToolResult(name, output, tool_use_id)
- ThinkingDelta(text)
- AgentResponse(content)
- SubAgentStart(task)
- SubAgentEnd(task, result)
- Error(message)

Emit factory:
```python
def make_emit(*listeners):
    def emit(event):
        for listener in listeners:
            listener(event)  # raise PermissionError to veto
    return emit
```

## UI (ui.py)

Use the rich library. The UI is an event listener:
- Tool calls: color-coded by type (yellow=bash, green=file ops, cyan=search, magenta=sub-agents)
- Tool results: dimmed preview (first line, truncated)
- Thinking: blue panel with full text
- Agent response: green panel
- Splash screen on startup

## Main (main.py)

- Load config from config.yaml
- Parse CLI: positional task (optional), --approve, --thinking, --config flags
- If task provided: single-shot mode
- If no task: conversation mode (REPL with shared message history)
- Wire up listeners: UI listener always on, approval listener if enabled
- Approval listener: auto-approve read-only tools, prompt for writes

## Config (config.yaml)

```yaml
model: claude-sonnet-4-20250514
max_tokens: 16384
max_turns: 20
system_prompt: |
  You are a coding agent. You help developers by reading, writing, and modifying code.
  Use tools to interact with the filesystem. Be concise and direct.
  When a task is complete, respond with a summary of what you did.
thinking:
  enabled: false
  budget_tokens: 10000
approval:
  enabled: false
  auto_approve:
    - read_file
    - list_directory
    - grep
```

## Dependencies

- anthropic
- rich
- pyyaml
