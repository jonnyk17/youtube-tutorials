# 01 - How Agents Work

An agent is a loop. That's the core insight. Strip away the frameworks, the abstractions, the marketing, and you're left with this:

1. Send a task to an LLM
2. The LLM either responds with text (done) or asks to use a tool (keep going)
3. If it wants a tool, execute it and send the result back
4. Go to step 2

```
         ┌──────────────┐
         │  User Task   │
         └──────┬───────┘
                │
         ┌──────▼───────┐
    ┌───►│   Call LLM    │
    │    └──────┬───────┘
    │           │
    │    ┌──────▼───────┐
    │    │ Check stop    │
    │    │ reason        │
    │    └──┬────────┬──┘
    │       │        │
    │  tool_use   end_turn
    │       │        │
    │  ┌────▼────┐   │
    │  │Execute  │   │
    │  │tools    │   │
    │  └────┬────┘   │
    │       │        │
    └───────┘   ┌────▼────┐
                │  Done   │
                └─────────┘
```

## The Three Pieces

**1. The message list.** This is the agent's memory. Every user message, assistant response, tool call, and tool result gets appended to this list. The LLM sees the entire history on every call. No database, no vector store, just a Python list.

**2. The tools.** These are functions the LLM can call. Each tool has a JSON schema (name, description, parameters) that the LLM sees, and a Python function that actually runs. The LLM never sees the implementation. It only sees the schema.

**3. The stop reason.** After every LLM call, the response includes a `stop_reason`. If it's `"end_turn"`, the agent is done. If it's `"tool_use"`, the LLM wants to call one or more tools. This single field drives the entire loop.

## Why This Matters

Most agent frameworks add layers on top of this basic pattern. State machines, graph-based workflows, planners, memory systems. Those have their place. But the core pattern is always the same loop.

By building it from scratch, you understand exactly what's happening at every step. When something goes wrong, you know where to look. When you need to add a feature, you know where it fits.

## What We're Building

Our agent, nano-agent, implements this loop in about 50 lines of Python. It adds:

- Five built-in tools (bash, read_file, write_file, grep, list_directory)
- An event system for observability
- An approval gate for safety
- Parallel sub-agents for independent tasks
- A Rich terminal UI

But at its core, it's still just the loop.

Next: [The Message List](02-the-message-list.md)
