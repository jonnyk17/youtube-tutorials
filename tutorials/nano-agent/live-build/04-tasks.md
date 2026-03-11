# Tasks: Step-by-Step Build

Break the work into small, testable tasks. Implement one at a time. Test at each stage.

## Task 1: Project Setup
- [ ] Initialize the project with uv
- [ ] Add dependencies: anthropic, rich, pyyaml
- [ ] Create config.yaml with defaults
- [ ] Create the package structure (nano_agent/ with __init__.py)

**Test:** `uv sync` succeeds, `uv run python -c "import anthropic; print('ok')"` works.

## Task 2: Provider
- [ ] Create provider.py
- [ ] Implement call_llm(messages, tools, config) wrapping the Anthropic API
- [ ] Support extended thinking via config flag

**Test:** Call the provider with a simple message and no tools. Get a response.

## Task 3: Tool Registry + First Two Tools
- [ ] Create tools.py with the TOOL_REGISTRY dict
- [ ] Implement the @tool decorator
- [ ] Implement get_tool_schemas() and execute_tool()
- [ ] Add bash tool
- [ ] Add read_file tool

**Test:** Register both tools, verify schemas are correct, execute each manually.

## Task 4: The Core Loop (Minimal)
- [ ] Create agent.py with the run() function
- [ ] Implement the basic loop: call LLM, check stop_reason, execute tools, repeat
- [ ] No events yet. Just print statements for now.

**Test:** Run the agent with "list the files in this directory". It should call list_directory (once we add it) or bash ls, and return a response.

## Task 5: Remaining Tools
- [ ] Add write_file tool
- [ ] Add grep tool (pattern required, path and include optional)
- [ ] Add list_directory tool (path optional)

**Test:** Ask the agent to create a file and then read it back. Ask it to grep for a pattern.

## Task 6: Events
- [ ] Create events.py with all 7 event dataclasses
- [ ] Implement make_emit(*listeners)
- [ ] Refactor agent.py to emit events instead of printing
- [ ] Remove all print statements from the loop

**Test:** Create a simple listener that logs events. Run the agent and verify events fire.

## Task 7: UI
- [ ] Create ui.py with the ui_listener
- [ ] Add color-coded tool calls
- [ ] Add thinking panel (blue, full text)
- [ ] Add agent response panel (green)
- [ ] Add splash screen

**Test:** Run the agent. Output should be color-coded and formatted.

## Task 8: Approval Gate
- [ ] Implement approval_listener in main.py
- [ ] Auto-approve read-only tools
- [ ] Prompt for write operations
- [ ] Handle PermissionError in the loop (send "denied" as tool result)

**Test:** Run with --approve. Deny a bash command. Agent should recover.

## Task 9: Sub-agents
- [ ] Add _run_subagents() to agent.py
- [ ] Add register_subagent_tool() to tools.py
- [ ] Wire up in main.py via init_subagents()
- [ ] Recursion guard: is_subagent=True strips run_subagents from schema

**Test:** Ask the agent to do two independent tasks. Watch them run in parallel.

## Task 10: Main + Conversation Mode
- [ ] Create main.py with CLI argument parsing
- [ ] Single-shot mode (task as argument)
- [ ] Conversation mode (REPL when no task given)
- [ ] Shared message history across conversation turns
- [ ] Wire everything together: config, listeners, emit, sub-agents

**Test:** Run in both modes. Conversation mode should remember previous turns.
