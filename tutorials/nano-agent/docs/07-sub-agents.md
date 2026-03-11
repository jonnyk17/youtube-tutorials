# 07 - Sub-Agents

Sub-agents let the agent run independent tasks in parallel. They are not a new concept. They are just recursive calls to the same agent loop.

## The Idea

Sometimes a task has parts that don't depend on each other. "Add type annotations to auth.py AND write tests for auth.py." The annotations don't need the tests, and the tests don't need the annotations. Running them sequentially wastes time.

Sub-agents solve this. The main agent recognizes independent work and delegates it to parallel sub-agents, each with their own message list and tool access.

## Implementation

`run_subagents` is just another tool. The LLM decides when to use it based on the schema:

```python
@tool(
    name="run_subagents",
    description="Run multiple independent tasks in parallel using sub-agents.",
    parameters={
        "tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "task": {"type": "string"}
                },
                "required": ["task"],
            },
        }
    },
)
async def run_subagents(tasks):
    return await run_fn(tasks)
```

The handler spawns parallel agent instances:

```python
async def _run_subagents(tasks, config, emit=None):
    async def run_one(t):
        if emit: emit(SubAgentStart(t["task"]))
        result = await run(t["task"], config, emit=emit, is_subagent=True)
        if emit: emit(SubAgentEnd(t["task"], result))
        return result

    results = await asyncio.gather(
        *[run_one(t) for t in tasks], return_exceptions=True
    )
    # Format results...
```

## The Recursion Guard

Sub-agents must not spawn their own sub-agents. That would be infinite recursion. The guard is one line:

```python
tools = get_tool_schemas(include_subagents=not is_subagent)
```

When `is_subagent=True`, the `run_subagents` tool is excluded from the schema. The sub-agent doesn't even know it exists.

## How It Looks

```
Task: "Add type hints to auth.py and utils.py, and write tests for both"

Main agent:
  > run_subagents [2 parallel tasks]
    >> sub-agent: Add type hints to auth.py and write tests
    >> sub-agent: Add type hints to utils.py and write tests

    [both running simultaneously]

    << sub-agent done
    << sub-agent done

  Agent: Done. Added type hints and tests for both files.
```

## Why asyncio.gather?

The main agent loop is `async` specifically for this. `asyncio.gather` runs multiple coroutines concurrently. Each sub-agent gets its own message list and runs independently.

The alternative would be threading, but `asyncio` is cleaner for this use case because the sub-agents share the same event system. Events from all sub-agents flow through the same `emit` function and appear in the same terminal.

Next: [Thinking and UI](08-thinking-and-ui.md)
