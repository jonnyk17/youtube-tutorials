# Research: How Existing Coding Agents Work

Before writing any code, I looked at how existing coding agents are built.

## What I Looked At

- **Claude Code** (Anthropic's official docs on how it works)
- **Sid Bharath's "Baby Claude Code"** (~400 lines of Python, blog post)
- **Geoffrey Huntley's workshop** (GitHub, builds from chatbot to agent)
- **FreeCodeCamp's agent tutorial** (Gemini-based, ~2 hour video)

## Key Findings

**From Anthropic's docs:** Claude Code uses a "single-threaded master loop" with a simple while(tool_call) pattern. No classifiers, no RAG, no DAG orchestrator. The model decides everything.

**From Sid Bharath:** Four pillars - brain (the LLM), instructions (system prompt), tools (file ops, shell), memory (the message list). His version is ~400 lines with streaming.

**Common patterns across all of them:**
1. A while loop that checks stop_reason
2. A message list that grows with every turn
3. Tool definitions as JSON schemas
4. Tool results fed back as user messages

## What Nobody Covers

- **The event/hooks pattern.** No tutorial explains how Claude Code's PreToolUse/PostToolUse hooks work, or the observer pattern that makes them possible. This is the most interesting architectural pattern and it's completely absent from every tutorial I found.
- **The system prompt engineering** that makes agents good
- **Terminal UX** - nobody talks about building a real terminal interface

## Our Angle

We're going to build the core loop AND the event system. The event system is what turns a toy into a real tool, and it's the pattern that Claude Code actually uses.
