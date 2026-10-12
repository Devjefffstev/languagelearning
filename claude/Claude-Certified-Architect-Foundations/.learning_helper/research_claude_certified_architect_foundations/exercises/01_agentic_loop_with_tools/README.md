# Exercise 1 — Build a multi-tool agentic loop

**Difficulty:** Easy
**Domains reinforced:** Domain 1 (Agentic Architecture & Orchestration), Domain 2 (Tool Design & MCP Integration)

## Goal

Build a Python agentic loop that meets the bar the official Exam Guide sets in §8 Exercise 1: three or four MCP-style tools with deliberately distinct descriptions, a `stop_reason`-driven loop, structured error responses, and a programmatic escalation gate.

## Task

You will edit `starter.py` in this folder. The starter contains a single tool (`get_todays_date`) and a working `agentic_loop.py`-style skeleton. You must extend it so that, when run, your agent handles the request:

> "Customer CUST-1042 says order ORD-2203 was damaged. First confirm the customer, check the order, then process a $50 refund."

…and rejects (with escalation, not crash) a $600 refund request.

Concrete requirements:

1. Add **three tools** with **distinct** descriptions: `get_customer`, `lookup_order`, `process_refund`. Their names and shapes must match the canonical names from the Exam Guide's Scenario 1.
2. The loop must read `response.stop_reason` and branch on `"tool_use"` vs `"end_turn"`. Use **no** string-sniffing, **no** arbitrary iteration cap as the primary stop signal.
3. Every tool result must be appended to the messages list before the next Claude call. Specifically, you must append the assistant turn **and** the user-role tool_result turn.
4. `process_refund` must return a structured error (use `isError`, `errorCategory="business"`, `isRetryable=False`) when the amount exceeds $500, with a customer-friendly message. The agent must surface that message in plain English and stop — no crash, no retry.
5. Implement at least **one** programmatic gate that blocks one tool (e.g., `process_refund`) until a prerequisite tool (`get_customer`) has been called in the same conversation.

## Hints

1. Look at how `agentic_loop.py` in `examples/` is structured. The starter is a stripped-down copy of it. Mirror that structure rather than starting from scratch.
2. For requirement 5, track which tools have been called by mutating a small dict in the loop (`called = {"get_customer": False}`) and short-circuiting tool execution when the gate condition fails. Return a structured error explaining why.
3. For requirement 4, the order doesn't matter: return the structured error JSON when amount > 500. The agent will surface the message.
4. Tool descriptions are the single largest contributor to tool-selection reliability. After you write your first draft, ask yourself: would Claude know not to call `get_customer` for an order number?

## Success criteria

You know you're done when running `python starter.py` produces this conversation shape (use the $50 amount first to verify the happy path, then change to $600 to verify the escalation path):

- Claude calls `get_customer` (gate-satisfied → tool runs)
- Claude calls `lookup_order`
- Claude calls `process_refund(50, ...)` and you see a success confirmation
- Final assistant message includes a friendly summary
- When the amount is `$600` instead: `process_refund` returns `isError: true` with `errorCategory=business`, and Claude's final message acknowledges the $500 limit without crashing

If your output ends with a Python traceback, you've broken the loop. Inspect `response.stop_reason` and the messages you append after each turn.