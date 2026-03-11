"""Entry point. Loads config, parses CLI args, runs the agent."""

import argparse
import asyncio
import sys
from pathlib import Path
import yaml
from .agent import init_subagents, run
from .events import ToolCall, make_emit
from .ui import console, splash, ui_listener


def load_config(path: str = "config.yaml") -> dict:
    config_path = Path(path)
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    return {"model": "claude-sonnet-4-20250514", "max_turns": 20}


def approval_listener(auto_approve: list[str]):
    def listener(event):
        if not isinstance(event, ToolCall):
            return
        if event.name in auto_approve:
            return
        console.print(f"  [yellow bold]Allow {event.name}? [y/n][/yellow bold] ", end="")
        answer = input().strip().lower()
        if answer != "y":
            raise PermissionError(f"User denied {event.name}")
    return listener


def main():
    parser = argparse.ArgumentParser(description="nano-agent")
    parser.add_argument("task", nargs="?", default=None, help="Initial task (omit for interactive mode)")
    parser.add_argument("--approve", action="store_true", help="Enable approval gate")
    parser.add_argument("--thinking", action="store_true", help="Enable extended thinking")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.thinking:
        config.setdefault("thinking", {})["enabled"] = True
    if args.approve:
        config.setdefault("approval", {})["enabled"] = True

    listeners = [ui_listener]
    approval_cfg = config.get("approval", {})
    if approval_cfg.get("enabled"):
        listeners.insert(0, approval_listener(approval_cfg.get("auto_approve", [])))

    emit = make_emit(*listeners)
    init_subagents(config, emit)

    splash()

    # Single-shot mode: run one task and exit
    if args.task:
        console.print(f"[dim]Task:[/dim] {args.task}\n")
        result = asyncio.run(run(args.task, config, emit=emit))
        if result == "Max turns reached.":
            console.print("[yellow]Stopped: max turns reached.[/yellow]")
            sys.exit(1)
        return

    # Conversation mode: REPL loop with shared message history
    messages = []
    console.print("[dim]Type a task, or 'quit' to exit.[/dim]\n")
    while True:
        try:
            task = console.input("[bold cyan]> [/bold cyan]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye.[/dim]")
            break
        if not task:
            continue
        if task.lower() in ("quit", "exit", "q"):
            console.print("[dim]Goodbye.[/dim]")
            break
        result = asyncio.run(run(task, config, emit=emit, messages=messages))
        if result == "Max turns reached.":
            console.print("[yellow]Stopped: max turns reached.[/yellow]")
        console.print()


if __name__ == "__main__":
    main()
