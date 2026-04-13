# Pi Coding Agent (Complete Guide)

Companion repo for the video. Everything you need to go from zero to a fully configured Pi setup with custom extensions.

## What is Pi?

Pi is a minimal, open-source terminal coding agent by Mario Zechner (creator of libGDX). It ships with 4 tools (read, write, edit, bash), a system prompt under 1,000 tokens, and an extension system that lets you build everything else yourself.

- GitHub: https://github.com/badlogic/pi-mono
- Website: https://pi.dev

## Why Pi?

Pi gives you control. Claude Code is batteries-included. Pi is a chassis you configure to match your workflow. No bloated system prompt eating your context window. No permission dialogs slowing you down. No vendor lock-in to one model provider.

The tradeoff is real: you do more setup work upfront. This repo gives you a head start.

## What's in This Repo

```
01-getting-started/     Install, first run, basic commands
02-configuration/       Custom providers, system prompts, settings
03-extensions/          Write your own tools and event handlers
04-skills/              On-demand capability packages
05-claude-code-migration/ Coming from Claude Code? Start here.
06-multi-provider/      Switch models mid-session, custom providers
```

## Quick Start

```bash
# Install Pi
npm install -g @mariozechner/pi-coding-agent

# Set up a provider (pick one)
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
export GEMINI_API_KEY=...

# Run it
pi
```

Then clone this repo and copy the extensions you want:

```bash
cp 03-extensions/permission-gate.ts ~/.pi/agent/extensions/
cp 03-extensions/git-checkpoint.ts ~/.pi/agent/extensions/
pi  # Extensions auto-load
```

## Requirements

- Node.js >= 20.6.0
- At least one LLM provider API key (or a subscription to Claude Pro/Max, ChatGPT Plus, GitHub Copilot, or Gemini)
