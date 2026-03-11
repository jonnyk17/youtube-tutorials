"""Tool registry and built-in tools."""

import asyncio
import os
import subprocess
from typing import Callable

TOOL_REGISTRY: dict[str, tuple[dict, Callable]] = {}


def tool(
    name: str, description: str, parameters: dict, required: list[str] | None = None
):
    """Decorator that registers a tool with its JSON schema and handler."""

    def decorator(fn: Callable) -> Callable:
        schema = {
            "name": name,
            "description": description,
            "input_schema": {
                "type": "object",
                "properties": parameters,
                "required": required
                if required is not None
                else list(parameters.keys()),
            },
        }
        TOOL_REGISTRY[name] = (schema, fn)
        return fn

    return decorator


def get_tool_schemas(include_subagents: bool = True) -> list[dict]:
    return [
        schema
        for name, (schema, _) in TOOL_REGISTRY.items()
        if include_subagents or name != "run_subagents"
    ]


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


# ── Built-in tools ───────────────────────────────────────────


@tool(
    "bash",
    "Run a shell command and return its output.",
    {
        "command": {"type": "string", "description": "The shell command to execute"},
    },
)
def bash(command: str) -> str:
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, timeout=120
    )
    output = result.stdout
    if result.stderr:
        output += f"\nSTDERR:\n{result.stderr}"
    if result.returncode != 0:
        output += f"\nExit code: {result.returncode}"
    return output.strip() or "(no output)"


@tool(
    "read_file",
    "Read the contents of a file at the given path.",
    {
        "file_path": {
            "type": "string",
            "description": "Absolute or relative path to the file",
        },
    },
)
def read_file(file_path: str) -> str:
    with open(file_path) as f:
        return f.read()


@tool(
    "write_file",
    "Write content to a file. Creates parent dirs if needed.",
    {
        "file_path": {
            "type": "string",
            "description": "Absolute or relative path to the file",
        },
        "content": {"type": "string", "description": "The content to write"},
    },
)
def write_file(file_path: str, content: str) -> str:
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)
    return f"Wrote {len(content)} bytes to {file_path}"


@tool(
    "grep",
    "Search for a regex pattern in files. Returns matching lines with paths and line numbers.",
    {
        "pattern": {"type": "string", "description": "The regex pattern to search for"},
        "path": {"type": "string", "description": "Directory or file to search in"},
        "include": {"type": "string", "description": "File glob pattern, e.g. '*.py'"},
    },
    required=["pattern"],
)
def grep(pattern: str, path: str = ".", include: str = "") -> str:
    cmd = ["grep", "-rn", pattern, path]
    if include:
        cmd.extend(["--include", include])
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return result.stdout.strip() or "No matches found."


@tool(
    "list_directory",
    "List files and directories at the given path. Defaults to current directory.",
    {
        "path": {"type": "string", "description": "Directory path to list"},
    },
    required=[],
)
def list_directory(path: str = ".") -> str:
    return "\n".join(sorted(os.listdir(path))) or "(empty directory)"


# ── Sub-agent tool (registered conditionally) ────────────────


def register_subagent_tool(run_fn):
    @tool(
        "run_subagents",
        "Run independent tasks in parallel using sub-agents. Use when tasks don't depend on each other.",
        {
            "tasks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "Task for the sub-agent",
                        }
                    },
                    "required": ["task"],
                },
                "description": "List of independent tasks to run in parallel",
            },
        },
    )
    async def run_subagents(tasks: list[dict]) -> str:
        return await run_fn(tasks)
