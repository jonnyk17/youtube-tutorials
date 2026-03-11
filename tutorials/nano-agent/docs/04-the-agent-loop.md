# 04 - The Agent Loop

This is the core of the agent. Everything else is built around this loop. It is about 50 lines of actual logic.

## The Full Loop

```python
async def run(task, config, emit=None, is_subagent=False):
    messages = [{"role": "user", "content": task}]
    tools = get_tool_schemas(include_subagents=not is_subagent)

    for turn in range(config.get("max_turns", 20)):
        response = call_llm(messages, tools, config)

        # Handle thinking blocks
        for block in response.content:
            if block.type == "thinking":
                if emit: emit(ThinkingDelta(block.thinking))

        # end_turn means the agent is done
        if response.stop_reason == "end_turn":
            text = next(
                (b.text for b in response.content if b.type == "text"), ""
            )
            if emit: emit(AgentResponse(text))
            return text

        # tool_use means we need to execute tools
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []

            for block in response.content:
                if block.type != "tool_use":
                    continue

                if emit:
                    try:
                        emit(ToolCall(block.name, block.input, block.id))
                    except PermissionError:
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": "Tool call denied by user.",
                        })
                        continue

                result = await execute_tool(block.name, block.input)

                if emit: emit(ToolResult(block.name, result, block.id))

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

            messages.append({"role": "user", "content": tool_results})

    return "Max turns reached."
```

## Walking Through It

**Line by line:**

1. `messages = [{"role": "user", "content": task}]` - Start with just the user's task. This list will grow.

2. `tools = get_tool_schemas(include_subagents=not is_subagent)` - Get the tool schemas. Sub-agents don't get the `run_subagents` tool (prevents infinite recursion).

3. `for turn in range(max_turns)` - Safety limit. Without this, a confused agent could loop forever.

4. `response = call_llm(messages, tools, config)` - Send everything to Claude and get a response.

5. Check `response.stop_reason`:
   - `"end_turn"` - Claude is done. Extract the text and return.
   - `"tool_use"` - Claude wants to use tools. Execute them and loop.

6. For each tool call, emit a `ToolCall` event (which the approval gate can veto), execute the tool, emit a `ToolResult` event, and collect the result.

7. Append all tool results as a user message and go back to step 4.

## The Two Exit Conditions

The loop ends when either:
- Claude returns `stop_reason == "end_turn"` (task complete)
- We hit `max_turns` (safety valve)

There is no "planning" step. No "reflection" step. No multi-phase pipeline. Claude decides what to do, does it, sees the result, and decides what to do next. The loop is the agent.

## Why async?

The loop itself is `async` because tool execution might be async (sub-agents use `asyncio.gather`). But the LLM call is synchronous. We don't stream. This keeps the message structure visible and easy to debug.

## The Provider Abstraction

The loop never imports `anthropic` directly. It calls `call_llm()` from `provider.py`:

```python
client = anthropic.Anthropic()

def call_llm(messages, tools, config):
    kwargs = dict(
        model=config["model"],
        max_tokens=config.get("max_tokens", 16384),
        system=config.get("system_prompt", ""),
        messages=messages,
        tools=tools,
    )
    thinking = config.get("thinking", {})
    if thinking.get("enabled"):
        kwargs["thinking"] = {
            "type": "enabled",
            "budget_tokens": thinking.get("budget_tokens", 10000),
        }
    return client.messages.create(**kwargs)
```

This separation means you could swap Claude for a different LLM by changing one file. The loop doesn't care which model is behind `call_llm`.

Next: [Events](05-events.md)
