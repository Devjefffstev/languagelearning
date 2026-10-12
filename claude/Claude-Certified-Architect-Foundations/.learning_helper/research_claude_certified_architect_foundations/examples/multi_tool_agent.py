"""
Production-flavored multi-tool agent.

Demonstrates Domain 1 + Domain 2 patterns:
  - stop_reason-driven loop (no string sniffing)
  - tools with deliberately differentiated descriptions
  - structured error responses (errorCategory, isRetryable, message)
  - PostToolUse hook for data normalization
  - tool_choice: "any" so the model MUST call a tool before answering
"""
import json
import os
from datetime import datetime, timezone

from anthropic import Anthropic
from anthropic.types import Message

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


# -------- Tools -----------------------------------------------------------

def get_customer(customer_id: str) -> dict:
    """Look up a customer by their verified account ID."""
    return {"customer_id": customer_id, "name": "Ada Lovelace", "verified": True}


def lookup_order(order_id: str) -> dict:
    """Look up an order by its order number (format 'ORD-####')."""
    # Real systems would return 40+ fields — we trim for brevity.
    return {
        "order_id": order_id,
        "items": ["Widget"],
        "status": "shipped",
        "created_at": "1715952000",  # Unix timestamp — will be normalized by hook
    }


def process_refund(amount_usd: float, reason: str) -> dict:
    """Issue a refund up to $500. Use escalate_to_human for larger refunds."""
    if amount_usd > 500:
        return {
            "isError": True,
            "errorCategory": "business",
            "isRetryable": False,
            "message": f"Refund of ${amount_usd} exceeds $500 policy — escalate to a human agent.",
        }
    return {"status": "ok", "amount_usd": amount_usd, "reason": reason}


# -------- Hook (PostToolUse) ---------------------------------------------

def normalize_tool_result(tool_name: str, content: dict) -> dict:
    """Run after every tool call. The exam calls this 'data normalization'."""
    # Convert Unix timestamps to ISO 8601 — different tools return different formats.
    if tool_name == "lookup_order" and "created_at" in content:
        ts = content["created_at"]
        try:
            content["created_at"] = datetime.fromtimestamp(
                int(ts), tz=timezone.utc
            ).isoformat()
        except (ValueError, TypeError):
            pass  # leave it; don't fabricate
    return content


# -------- Tool specs (descriptions are deliberately distinct) -------------

TOOLS = [
    {
        "name": "get_customer",
        "description": (
            "Look up a customer record by their verified account ID "
            "(format 'CUST-####'). Use this BEFORE any order or refund action "
            "to confirm identity. Do NOT call this for raw order lookups."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"customer_id": {"type": "string"}},
            "required": ["customer_id"],
        },
    },
    {
        "name": "lookup_order",
        "description": (
            "Look up an order by order number (format 'ORD-####'). "
            "Use when the customer references an order by number. "
            "Do NOT use for customer-identity questions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"],
        },
    },
    {
        "name": "process_refund",
        "description": (
            "Issue a refund for a verified order. Refunds above $500 must "
            "be escalated — the call will return isError=true with category "
            "'business'. NEVER call before get_customer has confirmed identity."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "amount_usd": {"type": "number"},
                "reason": {"type": "string"},
            },
            "required": ["amount_usd", "reason"],
        },
    },
]

TOOL_HANDLERS = {
    "get_customer": lambda args: get_customer(args["customer_id"]),
    "lookup_order": lambda args: lookup_order(args["order_id"]),
    "process_refund": lambda args: process_refund(args["amount_usd"], args["reason"]),
}


# -------- Agent loop ------------------------------------------------------

SYSTEM_PROMPT = (
    "You are a customer-support escalation specialist. Always call "
    "get_customer before any order or refund action."
)

MESSAGES = [{
    "role": "user",
    "content": "Customer CUST-1042 says order ORD-2203 was damaged. Refund $50.",
}]


def main() -> None:
    while True:
        response: Message = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            # "any" forces the model to call a tool rather than chat — guarantees
            # structured action every turn.
            tool_choice={"type": "any"},
            messages=MESSAGES,
        )

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
            result = (
                handler(block.input) if handler else {"isError": True, "message": "unknown"}
            )
            # ---- PostToolUse hook ----
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