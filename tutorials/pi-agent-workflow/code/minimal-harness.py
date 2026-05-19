#!/usr/bin/env python3
# /// script
# dependencies = ["anthropic>=0.40.0"]
# ///
"""
Minimal coding agent harness.

A coding agent is a model plus a harness. The model decides what should
happen next. The harness actually does it — reads files, runs commands,
and feeds results back to the model.

This file is the smallest meaningful version: two tools, one loop, no
guardrails. Every production coding agent (Claude Code, Codex, Cursor,
Pi) is a more sophisticated version of what's below.

Usage:
    export ANTHROPIC_API_KEY=...
    uv run minimal-harness.py
"""
import subprocess
from pathlib import Path
from anthropic import Anthropic

client = Anthropic()
MODEL = "claude-sonnet-4-6"


# Tools are JSON schemas the model can call.
# The model never executes them. The harness does.
TOOLS = [
    {
        "name": "read_file",
        "description": "Read the contents of a file at the given path.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
    {
        "name": "run_shell",
        "description": "Run a shell command and return stdout and stderr.",
        "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"],
        },
    },
]


def run_tool(name: str, args: dict) -> str:
    """Tool execution lives in the harness, not the model."""
    if name == "read_file":
        return Path(args["path"]).read_text()
    if name == "run_shell":
        result = subprocess.run(
            args["command"],
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return (result.stdout + result.stderr).strip() or "(no output)"
    return f"Unknown tool: {name}"


def agent(goal: str) -> str:
    """The agent loop. Call model, execute tools, feed results back, repeat."""
    messages = [{"role": "user", "content": goal}]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            tools=TOOLS,
            messages=messages,
        )

        # The model is done. Return its final text.
        if response.stop_reason == "end_turn":
            return "".join(b.text for b in response.content if b.type == "text")

        # The model asked to call one or more tools. Execute them.
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                output = run_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })

        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    print(agent("Look at the files in this folder and tell me what's in it."))
