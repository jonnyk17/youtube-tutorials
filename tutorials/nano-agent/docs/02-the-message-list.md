# 02 - The Message List

The message list is the agent's memory. Every interaction is recorded here, and the LLM sees the full history on every call. Understanding the message format is critical because it's the contract between your code and the API.

## The Shape of Messages

A conversation with tool use looks like this:

```python
messages = [
    # 1. The user's task
    {"role": "user", "content": "Create a hello.py file"},

    # 2. The assistant responds with a tool call
    {"role": "assistant", "content": [
        {"type": "text", "text": "I'll create that file for you."},
        {
            "type": "tool_use",
            "id": "toolu_01ABC",
            "name": "write_file",
            "input": {"file_path": "hello.py", "content": "print('hello')"}
        }
    ]},

    # 3. We send back the tool result
    {"role": "user", "content": [
        {
            "type": "tool_result",
            "tool_use_id": "toolu_01ABC",
            "content": "Wrote 15 bytes to hello.py"
        }
    ]},

    # 4. The assistant sees the result and responds
    {"role": "assistant", "content": [
        {"type": "text", "text": "Done. Created hello.py with a print statement."}
    ]}
]
```

## Key Rules

**Tool results must reference the tool_use_id.** Every `tool_use` block has an `id`. The matching `tool_result` must include `tool_use_id` with that same value. This is how the API pairs calls with results.

**The assistant's response can contain multiple blocks.** A single response might include text blocks, tool_use blocks, and (with extended thinking) thinking blocks. Your code needs to handle all of them.

**Tool results go in the user role.** This might feel odd, but it makes sense. From the LLM's perspective, tool results are new information coming from the outside world, just like user messages.

## In Our Code

The agent loop in `agent.py` manages this list:

```python
messages = [{"role": "user", "content": task}]
```

After each LLM call, if there are tool calls:

```python
# Append the assistant's response (contains tool_use blocks)
messages.append({"role": "assistant", "content": response.content})

# Execute tools and collect results
tool_results = []
for block in response.content:
    if block.type == "tool_use":
        result = await execute_tool(block.name, block.input)
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": result
        })

# Append tool results as a user message
messages.append({"role": "user", "content": tool_results})
```

The list grows with every turn. The LLM sees everything that happened before, which is how it maintains context across multiple tool calls.

## Why Not a Database?

For a teaching agent, the list is sufficient. The conversation lasts for one session and stays in memory. A production agent might need to persist conversations, compact long histories, or store tool outputs separately. But the underlying format stays the same.

Next: [Building Tools](03-building-tools.md)
