# nano-agent

A fully working coding agent built from scratch using the Anthropic API. No frameworks, no magic.

## Quick Start

```bash
git clone https://github.com/owainlewis/youtube-tutorials.git
cd youtube-tutorials/tutorials/nano-agent

# Install dependencies
uv sync

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Run it
uv run python -m nano_agent "Create a Python function that calculates fibonacci numbers and write it to fib.py"
```

## Flags

```bash
# Enable approval gate (asks before running dangerous tools)
uv run python -m nano_agent --approve "Refactor the utils module"

# Enable extended thinking (see Claude's reasoning)
uv run python -m nano_agent --thinking "Debug why the tests are failing"

# Custom config
uv run python -m nano_agent --config my-config.yaml "Add type hints to main.py"
```

## Demo

<!-- TODO: Add terminal recording / screenshot -->

## How It Works

The agent calls Claude in a loop. Claude responds with either text (done) or tool calls (keep going). The agent executes the tools and feeds results back. That's it.

```
User task
  -> LLM call
    -> stop_reason == "tool_use"?
      -> Execute tools, append results, loop back
    -> stop_reason == "end_turn"?
      -> Done. Print response.
```

## File Structure

```
nano_agent/
  main.py      # CLI entry point, config loading
  agent.py     # The core loop + sub-agent runner
  provider.py  # Anthropic API wrapper
  tools.py     # Tool registry + 5 built-in tools
  events.py    # Typed events + emit system
  ui.py        # Rich terminal output
```

## Tutorial

Step-by-step docs that walk through every concept:

1. [How Agents Work](docs/01-how-agents-work.md) - The mental model
2. [The Message List](docs/02-the-message-list.md) - Messages as memory
3. [Building Tools](docs/03-building-tools.md) - Tool registry and implementations
4. [The Agent Loop](docs/04-the-agent-loop.md) - The core loop
5. [Events](docs/05-events.md) - Event system and listeners
6. [Approval Gate](docs/06-approval-gate.md) - Permission system
7. [Sub-Agents](docs/07-sub-agents.md) - Parallel execution
8. [Thinking and UI](docs/08-thinking-and-ui.md) - Extended thinking and Rich UI

## YouTube Video

<!-- TODO: Add link to video -->

## What's Deliberately Left Out

This is a teaching tool, not a production agent. Things we skipped on purpose:

- **Streaming** - We use synchronous API calls. Streaming adds complexity without teaching new concepts.
- **Context compaction** - When the message list gets too long, a real agent would summarize and trim. We just set max_turns.
- **Session persistence** - No saving/loading conversation state. Each run starts fresh.
- **MCP (Model Context Protocol)** - A real agent might connect to external tool servers. We keep tools local.
- **Retry logic** - No exponential backoff on API errors. One failure and we stop.
- **Cost tracking** - No token counting or budget limits.
- **File change tracking** - No git integration or rollback capability.

Each of these would be a great follow-up project.
