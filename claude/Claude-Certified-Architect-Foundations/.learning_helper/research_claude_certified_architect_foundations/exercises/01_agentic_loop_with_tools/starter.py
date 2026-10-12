"""
Exercise 1 — Build a multi-tool agentic loop.

This is a SKELETON. Your job is to extend it so that:
  1. Three tools exist: get_customer, lookup_order, process_refund.
  2. The loop branches on response.stop_reason ("tool_use" vs "end_turn").
  3. process_refund returns structured errors with isError / errorCategory /
     isRetryable when amount_usd > 500.
  4. process_refund is blocked until get_customer has been called in this
     conversation (a programmatic prerequisite gate).

The skeleton below already works for the trivial "what is today's date?"
case so you can run it and see the loop move. Replace the TODOs.
"""
import json
import os
from datetime import date

from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


# -------- Tool implementations --------------------------------------------

def get_todays_date() -> str:
    """Trivial tool so the basic loop has something to call. Replace with the
    three Exam-Guide tools: get_customer, lookup_order, process_refund."""
    return date.today().isoformat()


# TODO(step 1): Implement get_customer, lookup_order, and process_refund.
#   - get_customer returns a dict with at least {"customer_id", "verified": True}
#   - lookup_order returns a dict with at least {"order_id", "status"}
#   - process_refund returns either {"status": "ok", ...} OR a structured error:
#       {"isError": True, "errorCategory": "business",
#        "isRetryable": False, "message": "Refund of $X exceeds $500 policy."}


# -------- Hook (already implemented so the structure is visible) ----------

def normalize_tool_result(tool_name: str, content) -> dict:
    """PostToolUse hook — convert Unix timestamps to ISO 8601 if present."""
    if isinstance(content, dict) and tool_name == "lookup_order" and "created_at" in content:
        from datetime import datetime, timezone
        try:
            content["created_at"] = datetime.fromtimestamp(
                int(content["created_at"]), tz=timezone.utc
            ).isoformat()
        except (ValueError, TypeError):
            pass
    return content


# -------- TOOLS list — only one trivial tool today ------------------------

TOOLS = [
    {
        "name": "get_todays_date",
        "description": "Return today's calendar date in ISO 8601 (YYYY-MM-DD).",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
]

TOOL_HANDLERS = {
    "get_todays_date": lambda args: get_todays_date(),
    # TODO(step 1 cont.): Register get_customer, lookup_order, process_refund
    # here as well. Each handler should be a callable that accepts the tool's
    # `input` dict and returns the dict you want echoed back to the model.
}


# TODO(step 2): Add a programmatic prerequisite gate. The simplest version is
# a module-level dict `called = {}` that tracks which tools have executed in
# this conversation. Decide where to enforce the gate — inside the loop, before
# the handler runs, or inside each handler. The exam note: hooks/prompts have
# non-zero failure rates for financial actions; deterministic gates do not.


# -------- Agent loop ------------------------------------------------------

# TODO(step 3): Make this system prompt reflect the customer-support scenario
# the Exam Guide uses (Scenario 1). The skeleton version is harmless but boring.
SYSTEM_PROMPT = "You are a helpful assistant."

# TODO(step 3): Replace this user message with the canonical Exam Guide
# scenario input: "Customer CUST-1042 says order ORD-2203 was damaged.
# First confirm the customer, check the order, then process a $50 refund."
MESSAGES = [{"role": "user", "content": "What is today's date?"}]


def main() -> None:
    while True:
        response = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=MESSAGES,
        )

        # TODO(step 4): Branch on response.stop_reason. The two valid
        # continuations are "end_turn" (print final assistant text and break)
        # and "tool_use" (execute tools, append results, loop). Anything else
        # should raise — the loop must never use string-sniffing on assistant
        # text content as a stop signal.

        # The skeleton below handles only the trivial "today's date" tool.
        # You will replace this block when you implement multi-tool support.
        if response.stop_reason == "end_turn":
            print(response.content[0].text)
            return

        if response.stop_reason != "tool_use":
            raise RuntimeError(f"Unexpected stop_reason: {response.stop_reason!r}")

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            handler = TOOL_HANDLERS.get(block.name)
            result = handler(block.input) if handler else {"isError": True, "message": "unknown tool"}

            # ---- PostToolUse hook (apply normalization before returning to
            # the model). Already wired up — extend normalize_tool_result() if
            # you need more shapes normalized.
            if isinstance(result, dict) and not result.get("isError"):
                result = normalize_tool_result(block.name, result)

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(result),
                **({"is_error": True} if isinstance(result, dict) and result.get("isError") else {}),
            })

        MESSAGES.append({"role": "assistant", "content": response.content})
        MESSAGES.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    main()