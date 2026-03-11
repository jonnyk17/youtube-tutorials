"""Event types and emit system."""

from dataclasses import dataclass
from typing import Callable


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


def make_emit(*listeners: Callable) -> Callable:
    """Return an emit(event) callable. PermissionError vetoes tool calls."""

    def emit(event):
        for listener in listeners:
            listener(event)

    return emit
