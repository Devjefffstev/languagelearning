"""
Minimal agentic loop.

Demonstrates the four mechanical steps the exam considers non-negotiable:
  1. Send messages to Claude.
  2. Inspect stop_reason: "tool_use" => execute the tool.
  3. Append the tool_result to the conversation history.
  4. Repeat until stop_reason == "end_turn" (or you decide to stop).
"""
import json
import os

from anthropic import Anthropic

# A deliberately trivial tool so the loop actually runs to completion.
def get_todays_date() -> str:
    """Return today's date in ISO 8601 format."""
    from datetime import date
    return date.today().isoformat()

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
messages = [{"role": "user", "content": "What is today's date? Use the tool."}]

# The loop. Pure stop_reason control flow — no string sniffing, no iteration caps
# treated as the primary stopping mechanism (those are anti-patterns the exam calls out).
while True:
    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=1024,
        tools=[{
            "name": "get_todays_date",
            "description": "Return today's calendar date in ISO 8601 (YYYY-MM-DD).",
            "input_schema": {"type": "object", "properties": {}, "required": []},
        }],
        messages=messages,
    )

    if response.stop_reason == "end_turn":
        # Final assistant message — surface it and we're done.
        print(response.content[0].text)
        break

    if response.stop_reason != "tool_use":
        raise RuntimeError(f"Unexpected stop_reason: {response.stop_reason!r}")

    # Execute every tool_use block Claude emitted this turn, in order.
    tool_results = []
    for block in response.content:
        if block.type != "tool_use":
            continue
        if block.name == "get_todays_date":
            result_text = get_todays_date()
        else:
            result_text = f"Unknown tool: {block.name}"
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": result_text,
        })

    # Append the assistant turn AND the user-role tool_result turn —
    # skipping the assistant append breaks conversational coherence.
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})