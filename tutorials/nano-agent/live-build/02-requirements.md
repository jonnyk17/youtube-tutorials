# Requirements: What We're Building

## The Product

A coding agent called **nano-agent**. It runs in the terminal, uses Claude as its brain, and can complete real coding tasks autonomously.

## Must Have (In Scope)

- Call Claude in a loop until the task is done
- Execute tools on Claude's behalf: read files, write files, run bash, grep, list directories
- Event-driven architecture - every observable action is a typed event
- Approval gate - user can allow or deny tool calls before they execute
- Parallel sub-agents - independent tasks run concurrently
- Extended thinking - see Claude's reasoning as it works
- Rich terminal UI - color-coded output, thinking panels
- YAML configuration
- Conversation mode - REPL with shared message history

## Deliberately Out of Scope

These are important but they hide the core pattern. Each could be a follow-up.

- **Streaming** - adds complexity, hides the message structure
- **Context compaction** - messages grow without bound, we just set max_turns
- **Session persistence** - no saving/resuming, each run starts fresh
- **MCP integration** - tool discovery protocol, separate concern
- **Retry logic** - fails fast, keeps code clear
- **Cost tracking** - no token counting

## Architecture

Six files, one concern each:

| File | Responsibility |
|------|---------------|
| main.py | CLI entry point, config loading, listener wiring |
| agent.py | The core loop + sub-agent runner |
| provider.py | Anthropic API wrapper |
| tools.py | Tool registry + built-in tools |
| events.py | Event types + emit system |
| ui.py | Rich terminal rendering |

## Design Principles

1. **The message list is the memory.** No database, no vector store.
2. **stop_reason drives the loop.** end_turn = done, tool_use = keep going.
3. **Events decouple behavior from the loop.** Adding features never changes the loop.
4. **Tool descriptions matter more than code.** The LLM only sees the schema.
5. **Sub-agents are recursive calls.** No orchestration framework.
6. **No framework.** Raw Anthropic SDK. See every moving part.
