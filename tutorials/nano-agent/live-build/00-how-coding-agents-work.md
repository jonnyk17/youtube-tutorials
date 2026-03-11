# How AI Coding Agents Work

Before building anything, let's understand what we're building.

## The Core Insight

AI coding agents like Claude Code are simpler than you think. Anthropic's own docs say it: "No classifiers, no RAG pipeline, no DAG orchestrator. The model itself decides everything."

A coding agent is three things:

1. **A loop** - Call the LLM, check the response, act on it, repeat
2. **A message list** - Every interaction is recorded and sent back on every call. This IS the memory.
3. **Tools** - Functions the LLM can call (read files, write files, run commands)

## The Loop

```
User gives a task
  -> Call Claude with the task + tool definitions
    -> Claude responds
      -> stop_reason == "tool_use"?  -> Execute tools, add results, loop back
      -> stop_reason == "end_turn"?  -> Done. Return the response.
```

That's it. Two possible outcomes per loop iteration. tool_use means keep going. end_turn means done.

## The Message List

The message list is a Python list. It grows with every turn:

```python
messages = [
    {"role": "user", "content": "Create a hello.py file"},
    {"role": "assistant", "content": [tool_use block]},
    {"role": "user", "content": [tool_result block]},
    {"role": "assistant", "content": [text response]},
]
```

The entire list is sent to Claude on every API call. That's how Claude remembers what happened. No database. No vector store. Just a list.

## Tools

Tools have two parts:
- **A JSON schema** - what Claude sees (name, description, parameters)
- **A Python function** - what actually runs

Claude never sees your code. It only sees the schema. The quality of your tool descriptions directly affects how well the agent works.

## The Event Pattern

This is the most interesting part. And it's exactly how Claude Code hooks work.

Instead of putting print statements and approval logic inside the loop, the loop emits typed events. Listeners subscribe to those events and handle them however they want.

- ToolCall event = Claude Code's PreToolUse hook
- ToolResult event = Claude Code's PostToolUse hook
- A listener raising PermissionError = a hook returning exit code 2 (deny)

Adding logging, approval gates, or UI never requires changing the loop. You just add listeners.
