"""The core agent loop. Call the LLM, check stop_reason, execute tools, repeat."""

import asyncio
from .events import (
    AgentResponse,
    SubAgentEnd,
    SubAgentStart,
    ThinkingDelta,
    ToolCall,
    ToolResult,
)
from .provider import call_llm
from .tools import execute_tool, get_tool_schemas, register_subagent_tool


async def run(
    task: str,
    config: dict,
    emit=None,
    is_subagent: bool = False,
    messages: list | None = None,
) -> str:
    """Run the agent loop until the task is done or max_turns is reached."""
    if messages is None:
        messages = []
    messages.append({"role": "user", "content": task})
    tools = get_tool_schemas(include_subagents=not is_subagent)

    for turn in range(config.get("max_turns", 20)):
        response = call_llm(messages, tools, config)

        for block in response.content:
            if block.type == "thinking" and emit:
                emit(ThinkingDelta(block.thinking))

        if response.stop_reason == "end_turn":
            messages.append({"role": "assistant", "content": response.content})
            text = next((b.text for b in response.content if b.type == "text"), "")
            if emit:
                emit(AgentResponse(text))
            return text

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
                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": "Tool call denied by user.",
                            }
                        )
                        continue
                result = await execute_tool(block.name, block.input)
                if emit:
                    emit(ToolResult(block.name, result, block.id))
                tool_results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": result}
                )
            messages.append({"role": "user", "content": tool_results})

    return "Max turns reached."


async def _run_subagents(tasks: list[dict], config: dict, emit=None) -> str:
    async def run_one(t: dict) -> str:
        task_text = t["task"]
        if emit:
            emit(SubAgentStart(task_text))
        result = await run(task_text, config, emit=emit, is_subagent=True)
        if emit:
            emit(SubAgentEnd(task_text, result))
        return result

    results = await asyncio.gather(*[run_one(t) for t in tasks], return_exceptions=True)
    parts = []
    for t, r in zip(tasks, results):
        status = f"Error: {r}" if isinstance(r, Exception) else f"Result: {r}"
        parts.append(f"Task: {t['task']}\n{status}")
    return "\n\n---\n\n".join(parts)


def init_subagents(config: dict, emit=None):
    async def handler(tasks: list[dict]) -> str:
        return await _run_subagents(tasks, config, emit)

    register_subagent_tool(handler)
