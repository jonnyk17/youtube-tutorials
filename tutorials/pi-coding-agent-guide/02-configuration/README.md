# Configuration

Pi stores configuration at `~/.pi/agent/`. Here's how to set it up properly.

## Custom Providers (models.json)

Add custom model providers in `~/.pi/agent/models.json`. This is how you connect local models, OpenRouter, or any OpenAI-compatible API.

See [models.json](./models.json) for a working example.

```json
{
  "providers": {
    "my-provider": {
      "baseUrl": "https://api.example.com/v1",
      "apiKey": "sk-...",
      "api": "openai-chat-completions",
      "models": [
        {
          "id": "my-model",
          "reasoning": false,
          "contextWindow": 128000,
          "maxTokens": 8192
        }
      ]
    }
  }
}
```

Supported API types:
- `openai-chat-completions` (works with most providers)
- `openai-responses`
- `anthropic`
- `google`

Changes to `models.json` are picked up live. No restart needed.

## System Prompt (SYSTEM.md)

Override or extend the default system prompt:

```bash
# Replace the default system prompt entirely
echo "You are a senior TypeScript engineer." > ~/.pi/agent/SYSTEM.md

# Or append to the default (add this at the top of SYSTEM.md)
# ---
# mode: append
# ---
```

See [SYSTEM.md](./SYSTEM.md) for an example.

## Settings (settings.json)

Key settings you might want to change:

```json
{
  "theme": "dark",
  "extensionPaths": ["~/my-extensions"],
  "defaultModel": "claude-sonnet-4-20250514",
  "compaction": {
    "threshold": 0.8
  }
}
```

## Prompt Templates

Reusable prompts stored at `~/.pi/agent/prompts/`:

```markdown
<!-- ~/.pi/agent/prompts/review.md -->
Review this code for:
1. Security vulnerabilities
2. Performance issues
3. Missing error handling

Focus on: {{focus}}
```

Invoke with `/review` and Pi will interpolate `{{focus}}` from context or ask for it.
