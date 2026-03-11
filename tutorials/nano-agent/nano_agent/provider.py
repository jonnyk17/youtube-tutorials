"""LLM provider. Wraps the Anthropic API so the agent loop never imports anthropic directly."""

import anthropic

client = anthropic.Anthropic()


def call_llm(messages: list[dict], tools: list[dict], config: dict) -> anthropic.types.Message:
    kwargs = dict(
        model=config["model"],
        max_tokens=config.get("max_tokens", 16384),
        system=config.get("system_prompt", ""),
        messages=messages,
        tools=tools,
    )
    thinking = config.get("thinking", {})
    if thinking.get("enabled"):
        kwargs["thinking"] = {
            "type": "enabled",
            "budget_tokens": thinking.get("budget_tokens", 10000),
        }
    return client.messages.create(**kwargs)
