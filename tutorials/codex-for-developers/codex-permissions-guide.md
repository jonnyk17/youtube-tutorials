# Codex Permissions TL;DR

Codex permissions make the most sense if you think about **boundaries**.

For any action, Codex is effectively asking:

1. Is this **inside the workspace** or **outside it**?
2. Does this action need the **internet**?
3. If it crosses a boundary, should I **ask first**?

That maps to three controls:

- `sandbox_mode`: where Codex can act
- `network_access`: whether commands can go online
- `approval_policy`: whether Codex asks before crossing a boundary

## The simplest mental model

Think of Codex as working inside a fenced workshop.

- The **sandbox** decides where the fence is.
- **Network access** decides whether commands can leave the workshop to use the internet.
- **Approval policy** decides whether Codex has to stop and ask before crossing the fence.

If you remember one sentence, use this:

> Sandbox defines the boundary. Network controls internet access. Approval controls whether Codex asks before crossing the line.

## The three controls

### 1. Sandbox

This controls where Codex can write and what commands it can run safely.

- `read-only`
  - Good for review, analysis, and planning
  - Codex can inspect files but not make normal edits
- `workspace-write`
  - Best default for day-to-day development
  - Codex can edit files in the workspace and run routine local commands there
- `danger-full-access`
  - No sandbox boundary
  - Only use this when you intentionally want full machine access

### 2. Network

This is the most confusing part because there are **two different internet paths**.

#### Command network access

This affects shell commands and code that need the internet:

- `curl https://example.com`
- `npm install`
- `uv sync`
- API calls from scripts

If command network access is off, those actions fail or need escalation.

#### Built-in web search / fetch

Codex can also use its own built-in web tooling. That is **separate** from shell network access.

So these are different:

- `curl https://example.com` -> depends on command network access
- `Fetch https://example.com` -> may use Codex's built-in web tooling

This is why Codex may be able to fetch a page in chat even when terminal `curl` is blocked.

### 3. Approval policy

This controls whether Codex asks before doing something that crosses a boundary.

- `untrusted`
  - More cautious
- `on-request`
  - Good default for most people
  - Codex asks when it needs extra permission
- `never`
  - Codex does not interrupt for approvals
  - Best only when you already trust the workspace and your settings

Important:

> Approval does not create permission by itself. It only decides whether Codex asks before trying to cross a boundary.

## Common examples

| Action | What matters | Typical result in `workspace-write` |
|---|---|---|
| Edit `./backend/app.py` | Sandbox | Allowed |
| Create `./notes.txt` | Sandbox | Allowed |
| Edit `~/Desktop/notes.txt` | Sandbox + approval | Outside workspace, so usually asks or needs escalation |
| Read `~/Desktop/notes.txt` | Filesystem rules | Often readable unless explicitly denied |
| Edit `.git/config` | Protected paths | Usually blocked even inside workspace |
| Run `pytest` | Sandbox | Usually allowed |
| Run `curl https://example.com` | Network + approval | Needs command network access |
| Run `npm install` | Network + approval | Needs command network access |
| Ask Codex to look up docs | Web search setting | May still work without shell network |

## Important edge cases

### Outside the current folder

If you're in `workspace-write`, Codex can usually edit inside the workspace, but not arbitrary places like:

- `~/Desktop`
- `~/Downloads`
- another repo

That usually triggers an approval flow or needs escalated execution.

### Protected paths inside the workspace

Some paths are still treated as protected even if they are inside the workspace, including:

- `.git`
- `.codex`
- `.agents`

So "inside the repo" does **not** always mean "writable".

### Reads vs writes

The big safety lesson is:

- write access is tightly controlled
- read access can be broader unless you explicitly deny it

If you want to protect sensitive files like `.env` files or `~/.ssh`, add deny rules.

## A practical default for most developers

If you want something that works well for normal coding:

- `sandbox_mode = "workspace-write"`
- `approval_policy = "on-request"`
- enable network only if you regularly install packages or call APIs

That gives you:

- smooth editing inside the project
- prompts when something tries to escape the workspace
- fewer surprises than full autonomy

## UI vs config vs CLI

These are just different ways to set the same behavior:

- **UI permissions picker**
  - quick session-level choice
- **`config.toml`**
  - your default settings
- **CLI flags**
  - one-off overrides for a single launch

Good rule of thumb:

- use the UI when you want to change behavior right now
- use `config.toml` for your normal defaults
- use CLI flags for temporary experiments

## Config precedence

If multiple places define the same setting, the more specific setting wins.

In practice:

1. CLI flags win
2. selected profile wins over base config
3. project config can override user config
4. org-managed policy may block unsafe combinations entirely

## Recommended teaching summary

If you are explaining this to someone else, use this:

1. Codex first checks whether the action is inside the workspace.
2. Then it checks whether the action needs the internet.
3. Then it checks whether it should ask before crossing a boundary.

That is the whole permission system most developers need to understand.

## Good defaults by situation

### Safe everyday coding

- `workspace-write`
- `on-request`
- network on only if needed

### Review only

- `read-only`
- `on-request`

### Full autonomy in a trusted environment

- `workspace-write` or `danger-full-access`
- `never`
- only if you understand the tradeoff

## Final shortcut

When in doubt, remember:

> Inside workspace is easy. Outside workspace is sensitive. Internet is separate. Approval decides whether Codex asks.
