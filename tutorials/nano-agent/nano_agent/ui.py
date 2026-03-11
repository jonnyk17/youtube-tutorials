"""Rich terminal UI. Renders agent events as color-coded output."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from .events import AgentResponse, Error, SubAgentEnd, SubAgentStart, ThinkingDelta, ToolCall, ToolResult

console = Console()

TOOL_COLORS = {
    "bash": "yellow", "read_file": "green", "write_file": "green",
    "grep": "cyan", "list_directory": "cyan", "run_subagents": "magenta",
}


def splash():
    text = Text("nano-agent", style="bold white")
    text.append("\n  a minimal coding agent", style="dim")
    console.print(Panel(text, border_style="blue", padding=(1, 2)))


def _summarize(name: str, inp: dict) -> str:
    if name == "bash": return f'`{inp.get("command", "")[:80]}`'
    if name in ("read_file", "write_file"): return inp.get("file_path", "")
    if name == "grep": return f'{inp.get("pattern", "")} in {inp.get("path", ".")}'
    if name == "list_directory": return inp.get("path", ".")
    if name == "run_subagents": return f'{len(inp.get("tasks", []))} parallel tasks'
    return str(inp)[:60]


def ui_listener(event):
    match event:
        case ToolCall(name=name, input=inp):
            color = TOOL_COLORS.get(name, "white")
            console.print(f"  [{color}]> {name}[/{color}] {_summarize(name, inp)}")
        case ToolResult(output=output):
            lines = output.strip().split("\n")
            preview = lines[0][:120] + (f" ... ({len(lines)} lines)" if len(lines) > 1 else "")
            console.print(f"    [dim]{preview}[/dim]")
        case ThinkingDelta(text=text):
            console.print(Panel(
                Text(text, style="italic"),
                title="[bold]Thinking[/bold]",
                border_style="blue",
                padding=(1, 2),
            ))
        case AgentResponse(content=content):
            console.print()
            console.print(Panel(content, title="Agent", border_style="green"))
        case SubAgentStart(task=task):
            console.print(f"  [magenta]>> sub-agent:[/magenta] {task[:80]}")
        case SubAgentEnd():
            console.print(f"  [magenta]<< sub-agent done[/magenta]")
        case Error(message=msg):
            console.print(f"  [red bold]Error: {msg}[/red bold]")
