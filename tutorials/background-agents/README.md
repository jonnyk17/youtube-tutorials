# Background Agents

A background agent system in a single Python file. Assign tasks from a task manager, an AI agent does the work, you review the results.

This repo uses Todoist as the control plane and Claude Code as the agent, but the pattern works with any task manager and any agent.

## Quick Start

```bash
git clone https://github.com/owainlewis/background-agents.git
cd background-agents
cp .env.example .env
# Add your TODOIST_API_TOKEN to .env

uv run agent_worker.py --project "Agent" --watch --verbose
```

Add a task to your Todoist project. The worker picks it up, dispatches to Claude Code, and comments back when it's done.

## Tutorial

**[Read the full tutorial →](docs/tutorial.md)** — The three levels of AI delegation, why task managers beat chat interfaces, the three-component architecture pattern, and how to adapt it to your own stack.
