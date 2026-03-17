# Background Agent Workers: A Pull-Based Architecture

Companion guide for [My Multi-Agent Team (Built From Scratch)](https://youtube.com/@owainlewis).

## The Problem

Most of us use AI coding agents the same way: open a terminal, start a session, paste context, prompt, wait, correct, repeat. It works, but you're the bottleneck. You can only run one task at a time because every task needs you in the loop.

Tools like OpenClaw attempt to solve this by letting agents run in the background. But they're built on a push-based (webhook) architecture that exposes HTTP endpoints on machines with access to your code, credentials, and file system. That's a security surface you don't need.

There's a simpler approach.

## The Solution

**agent-worker** is a polling-based background agent that watches your issue tracker for tasks, picks them up, executes an agent harness to do the work, and reports results back. You stay out of the loop entirely.

```
You create a ticket -> Agent picks it up -> Writes code -> Runs tests -> Opens a PR -> You review
```

The full source code is at [github.com/owainlewis/agent-worker](https://github.com/owainlewis/agent-worker).

## Architecture

The system has three components:

1. **Linear** (or any issue tracker) is the task manager and source of truth. You create tickets here. The agent label marks a ticket as agent-ready.
2. **Worker Service** runs on your machine and polls Linear on a schedule. When it finds a ready ticket, it claims it and starts processing.
3. **Agent Harness** (Claude Code, Codex, or any CLI agent) does the actual coding work. The worker is harness-agnostic. Adding a new agent is a single file implementing the executor interface.

```
Phone / Laptop
      |
      |  create ticket
      v
   Linear
      |
      |  worker polls (outbound only)
      v
Worker Service
      |
      |  1. pre-hooks (git pull, checkout branch)
      |  2. dispatch to agent harness
      |  3. post-hooks (lint, test, commit, push)
      v
  Agent Harness (Claude Code / Codex)
      |
      |  writes code
      v
  Pull Request
      |
      |  you review
      v
    main
```

### The worker loop

The core is an infinite loop:

1. **Poll** Linear for tickets with the agent label in "Todo" status
2. **Claim** the ticket by marking it "In Progress" (no two workers pick up the same ticket)
3. **Pre-hooks** run deterministic setup: git pull, create a branch
4. **Dispatch** the ticket to the agent harness with a structured prompt
5. **Post-hooks** run deterministic verification: lint, test, commit, push
6. **Report** success or failure back to Linear with details

If anything fails at any step, the ticket is marked failed with the error message as a comment.

## Pull-Based vs Push-Based Architecture

This is the core architectural decision and it matters for security.

### Push-based (webhook) architecture

This is how tools like OpenClaw work. An external service sends HTTP requests to your agent when there's work to do.

```
External Service --HTTP POST--> Your Machine (exposed endpoint)
                                     |
                                     v
                                Agent executes
```

**What this requires:**
- An HTTP endpoint exposed to the internet (or at minimum, to the service)
- A machine that accepts inbound connections
- Port forwarding, tunneling, or a public IP
- Authentication and authorization on the endpoint

**The problem:** The machine running your agent has access to your code, your file system, your credentials, your git config. Exposing an HTTP endpoint on that machine creates an attack surface. Anyone who can reach that endpoint can potentially trigger agent execution. You're trusting the external service's security, your network configuration, and every layer in between.

### Pull-based (polling) architecture

This is how agent-worker works. Your machine reaches out to the issue tracker on a schedule. Nothing reaches in.

```
Your Machine --polls--> Linear API (outbound only)
     |
     v
Agent executes
```

**What this requires:**
- Outbound HTTPS requests to the Linear API
- A Linear API key
- Nothing else

**Why this is better for most use cases:**
- **No exposed ports.** Your machine makes outbound requests only. There's nothing to attack from the outside.
- **No inbound connections.** No tunneling, no port forwarding, no public IP required.
- **Simpler infrastructure.** No webhook receivers, no authentication middleware, no retry logic for failed deliveries.
- **Works anywhere.** Behind a NAT, on a home network, on a corporate VPN. If you can make HTTPS requests, you can run the worker.
- **Same security model as your browser.** Your machine already makes outbound requests to hundreds of services. This is the same pattern.

### The tradeoff

Pull-based architectures have higher latency. If you poll every 60 seconds, a new ticket waits up to 60 seconds before pickup. For background coding tasks that take minutes to complete, this latency is irrelevant. If you needed sub-second response times, push-based would be the better choice. For agent work, you don't.

### Summary

| | Push-based (webhooks) | Pull-based (polling) |
|---|---|---|
| **Direction** | External service pushes to your machine | Your machine pulls from external service |
| **Exposed surface** | HTTP endpoint on agent machine | None |
| **Inbound connections** | Required | None |
| **Infrastructure** | Webhook receiver, auth middleware, retry logic | Polling loop, API key |
| **Latency** | Near-instant | Poll interval (e.g. 60s) |
| **Security posture** | Machine with code access accepts inbound traffic | Machine with code access makes outbound requests only |
| **Best for** | Real-time triggers, low-latency requirements | Background tasks, coding agents, async work |

## Hooks: Deterministic Guardrails Around Non-Deterministic Agents

Agents are powerful but non-deterministic. You can't predict exactly what code they'll write or what changes they'll make. Hooks solve this by wrapping agent execution with deterministic, auditable steps.

### Pre-hooks

Run before the agent starts. If any pre-hook fails, the agent never runs.

```yaml
hooks:
  pre:
    - "git checkout main"
    - "git pull origin main"
    - "git checkout -b agent/task-{id}"
```

These guarantee the agent starts from a clean, up-to-date state on a dedicated branch. If `git pull` fails (maybe you're offline, maybe there's a conflict), the agent never touches the codebase.

### Post-hooks

Run after the agent finishes. If any post-hook fails, the task is marked failed.

```yaml
hooks:
  post:
    - "bun run test"
    - "bun run lint"
    - "git add -A"
    - "git commit -m 'feat: {title}'"
    - "git push origin agent/task-{id}"
```

The agent doesn't get to declare itself done. The tests do. If the code doesn't pass lint and tests, it doesn't get committed or pushed. The agent has to meet the same bar any human developer would.

### Why this matters

Without hooks, you're letting an agent loose on your codebase with no guardrails. With hooks, you have a deterministic process wrapped around a non-deterministic agent:

```
[deterministic] pre-hooks  ->  [non-deterministic] agent  ->  [deterministic] post-hooks
```

The agent does the creative work. The hooks enforce the process.

## Configuration

The worker is configured with a single YAML file. All project-specific logic lives here, not in the worker code. This means the worker is project-agnostic: swap the config, point it at a different repo, and it works.

```yaml
linear:
  project_id: "your-project-uuid"
  poll_interval_seconds: 60

  statuses:
    ready: "Todo"
    in_progress: "In Progress"
    done: "Done"
    failed: "Canceled"

repo:
  path: "/path/to/your/repo"

hooks:
  pre:
    - "git checkout main"
    - "git pull origin main"
    - "git checkout -b agent/task-{id}"
  post:
    - "bun run test"
    - "git add -A"
    - "git commit -m 'feat: {title}'"
    - "git push origin agent/task-{id}"

claude:
  timeout_seconds: 300
  retries: 0

log:
  file: "./agent-worker.log"
```

Hook commands support variable interpolation:

| Variable | Value |
|---|---|
| `{id}` | Linear ticket identifier (e.g. `ENG-42`) |
| `{title}` | Slugified ticket title (e.g. `add-login-page`) |
| `{branch}` | Generated branch name (`agent/task-{id}`) |

## Getting Started

### Prerequisites

- [Bun](https://bun.sh) 1.0+
- An agent harness installed and authenticated (Claude Code or Codex)
- A Linear account with a personal API key

### Setup

```bash
git clone https://github.com/owainlewis/agent-worker
cd agent-worker
bun install
```

Copy and edit the config:

```bash
cp agent-worker.example.yaml agent-worker.yaml
```

Set your Linear API key:

```bash
export LINEAR_API_KEY=lin_api_...
```

### Run

```bash
bun run start
```

The worker starts polling. Create a ticket in Linear, add the agent label, and watch it get picked up.

## Scaling

The pattern scales without architectural changes:

- **One worker, one repo:** Run `agent-worker` on your laptop. It processes tickets sequentially.
- **Multiple workers, one repo:** Run multiple instances. Each claims tickets atomically (mark as "In Progress"), so no two workers pick up the same task.
- **Multiple workers, multiple repos:** Each worker gets its own config pointing at a different repo. They all poll the same Linear project or different ones.

The system scales from a single agent on your laptop to hundreds of workers across many repos and projects without any additional infrastructure.

## Links

- [agent-worker source code](https://github.com/owainlewis/agent-worker)
- [Video: My Multi-Agent Team (Built From Scratch)](https://youtube.com/@owainlewis)
