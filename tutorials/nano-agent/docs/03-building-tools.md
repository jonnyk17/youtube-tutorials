# 03 - Building Tools

Tools are how the agent interacts with the world. Each tool has two parts: a JSON schema (what the LLM sees) and a Python function (what actually runs). The LLM never sees your implementation. It only sees the schema.

## The Registry Pattern

We use a decorator to register tools. This keeps the schema and implementation together:

```python
TOOL_REGISTRY: dict[str, tuple[dict, Callable]] = {}

def tool(name: str, description: str, parameters: dict):
    def decorator(fn):
        schema = {
            "name": name,
            "description": description,
            "input_schema": {
                "type": "object",
                "properties": parameters,
                "required": list(parameters.keys()),
            },
        }
        TOOL_REGISTRY[name] = (schema, fn)
        return fn
    return decorator
```

Using the decorator:

```python
@tool(
    name="bash",
    description="Run a shell command and return its output.",
    parameters={
        "command": {
            "type": "string",
            "description": "The shell command to execute",
        }
    },
)
def bash(command: str) -> str:
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, timeout=120
    )
    output = result.stdout
    if result.stderr:
        output += f"\nSTDERR:\n{result.stderr}"
    return output.strip() or "(no output)"
```

## The Five Built-In Tools

| Tool | What It Does | Why the Agent Needs It |
|------|-------------|----------------------|
| bash | Runs shell commands | Installing packages, running tests, git operations |
| read_file | Reads a file | Understanding existing code |
| write_file | Writes a file | Creating or modifying code |
| grep | Searches for patterns | Finding relevant code across a project |
| list_directory | Lists a directory | Navigating the filesystem |

These five tools are enough for real coding tasks. Claude Code has more tools, but the pattern is identical for each one.

## Tool Execution

When the LLM calls a tool, we look it up in the registry and run it:

```python
async def execute_tool(name: str, tool_input: dict) -> str:
    if name not in TOOL_REGISTRY:
        return f"Unknown tool: {name}"
    _, handler = TOOL_REGISTRY[name]
    try:
        result = handler(**tool_input)
        if asyncio.iscoroutine(result):
            result = await result
        return str(result)
    except Exception as e:
        return f"Error: {e}"
```

Note: errors are returned as strings, not raised. The LLM needs to see what went wrong so it can try a different approach.

## Why Descriptions Matter

The LLM decides which tool to use based entirely on the description and parameter names. If your description is vague, the LLM will pick the wrong tool or pass wrong parameters.

Compare:

```
Bad:  "Run a command"
Good: "Run a shell command and return its output. Use this for installing
       packages, running tests, or any shell operation."
```

The good description tells the LLM when to use this tool and what to expect back. This is one of the most impactful things you can tune in an agent.

## Adding Your Own Tools

Adding a tool is just defining a function with the decorator:

```python
@tool(
    name="search_web",
    description="Search the web for a query and return results.",
    parameters={
        "query": {
            "type": "string",
            "description": "The search query",
        }
    },
)
def search_web(query: str) -> str:
    # Your implementation here
    ...
```

The loop doesn't change. The event system doesn't change. You just add a function and the agent can use it.

Next: [The Agent Loop](04-the-agent-loop.md)
