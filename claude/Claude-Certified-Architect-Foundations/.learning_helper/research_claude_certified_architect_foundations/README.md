# Claude Certified Architect — Foundations (CCAR-F)

## Description

The **Claude Certified Architect – Foundations** (exam code **CCAR-F**) is an Anthropic Partner Academy certification that validates you can make informed tradeoff decisions when building production solutions with Claude. It is not a trivia quiz about Claude's features — every question is grounded in a realistic production scenario, and on exam day you receive **4 scenarios picked at random from a bank of 6**. The exam is 60 multiple-choice and multiple-response items over 120 minutes, scored on a 100–1,000 scale with a passing threshold of **720**. The exam fee is $125 USD, validity is 12 months (renewable via a free non-proctored assessment), and retakes carry escalating waiting periods (14, 30, 90 days).

The blueprint weights five content domains: **Agentic Architecture & Orchestration (27%)**, **Claude Code Configuration & Workflows (20%)**, **Prompt Engineering & Structured Output (20%)**, **Tool Design & MCP Integration (18%)**, and **Context Management & Reliability (15%)**. The six scenarios you may face — a customer support resolution agent, a multi-agent research system, developer productivity tooling, Claude Code in CI/CD, structured data extraction, and a team Claude Code configuration — cut across these domains. Underneath the scenarios sit the core primitives you must internalize: the agentic loop and `stop_reason` handling, subagent orchestration with isolated context, MCP tool descriptions and resource interfaces, CLAUDE.md hierarchies with path-scoped rules, JSON-schema-enforced structured output via `tool_use`, and a long list of reliability patterns (escalation criteria, error propagation, context preservation, confidence-based human review).

The exam assumes 6+ months of hands-on experience with the Claude API, the Claude Agent SDK, Claude Code, and MCP. If you already have some baseline knowledge — which you indicated — the most efficient path to passing is not to re-read every Anthropic blog post, but to work through the four **Preparation Exercises** in the official Exam Guide end-to-end so the tradeoffs become instinct rather than something you have to reason out from scratch under time pressure. The bundled official Exam Guide (`./sources/claude-certified-architect-foundations-exam-guide.pdf`, v1.0, July 2026) is the authoritative reference — every task statement listed there is fair game.

> **Last verified:** October 11, 2026. Exam guide v1.0 is current; check the Skilljar exam page (linked below) before your exam date for any updated versions.

## Analogy

Think of an Anthropic agent application like a **busy restaurant kitchen** — every concept on the exam has a physical-world counterpart that makes the underlying tradeoff obvious.

| Real kitchen | Claude system | Why it maps |
|---|---|---|
| **Head chef (expediter)** | **Coordinator agent** | Decides which station handles each ticket, owns the system prompt, sees every ticket exactly once |
| **Sous chefs at separate stations** | **Subagents (Task tool)** | Each has an isolated station (isolated context), specializes in one cuisine, does NOT inherit the head chef's tasting notes (no automatic context inheritance) |
| **Recipes pinned above each station** | **System prompt per subagent + `.claude/skills/` `SKILL.md`** | Each station follows its own instructions, not the kitchen-wide playbook |
| **The kitchen-wide playbook (`CLAUDE.md`)** | **`./CLAUDE.md` at the project root** | Everyone reads it; universal conventions applied to every dish |
| **Specialty equipment: pasta roller, wok station, pastry bench** | **MCP servers (`/mcp.json`)** | Each provides a specific capability surface (tools/resources) only available when configured; multiple servers active simultaneously |
| **Tickets coming in from the host stand** | **User messages** | The raw input; the head chef (coordinator) decides whether the ticket needs the sushi station, the grill, or just goes straight out |
| **`stop_reason: "tool_use"`** | **"Plating not done, send back to station"** | The model decided it needs a tool before it can finish — keep the loop going |
| **`stop_reason: "end_turn"`** | **"Ticket is plated; runner takes it to the table"** | Final answer; loop exits, response goes to the user |
| **Structured tickets in triplicate** | **JSON schema tool inputs (`tool_use`)** | Forces a consistent shape; you can't hand the kitchen a recipe scribbled on a napkin |
| **Plan mode: chef preps the menu before service starts** | **`claude -p` with explicit planning prompt** | For complex multi-station dishes, you sketch the entire flow before lighting the burners — prevents late-morning disasters |
| **The walk-in fridge stuffed with 200 jars** | **Long context with 40+ fields per tool result** | Stuff you don't see first, you forget — context window is finite, position-aware placement matters ("lost in the middle") |
| **Customer asks to speak to a manager** | **Explicit escalation trigger** | Some tickets must bypass the line cooks entirely; agent must honor immediately, not retry autonomously |
| **A spice rack with 18 mystery jars** | **An agent with 18 tools** | Selection accuracy collapses; trim to the 4–5 each cook actually needs |
| **`PostToolUse` hook** | **Health-inspector spot-check after every dish leaves a station** | Programmatic normalization/validation: a timestamp in any format gets converted to ISO-8601 before it goes further down the line |

The mental model that pulls everything together: **Claude is the head chef, tools are stations, MCP servers are specialty rooms, subagents are sous chefs, the loop is service running continuously, planning is the prep before the dinner rush, and context budget is fridge space.** Once that frame sticks, every domain-specific question on the exam reduces to "which kitchen practice applies here?"

## Examples

### Example #1 — Minimal agentic loop with `stop_reason` handling

#### Quick setup

This is the **smallest possible** Python implementation of the agentic loop. It demonstrates the single most-tested concept on the exam: inspect `response.stop_reason`, run the tool Claude asked for, append the result, and iterate until Claude is done.

Save as `examples/agentic_loop.py`. Requires `pip install anthropic` and the `ANTHROPIC_API_KEY` environment variable.

```python
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
```

**Run it:** `python examples/agentic_loop.py` — Claude will call `get_todays_date`, you'll see the ISO date printed. That's the loop end-to-end.

#### Complete setup

A **production-flavored** version that demonstrates the rest of Domain 1: multiple tools, structured errors with `isError`, MCP-style tool descriptions, an explicit handler for each error category, a `tool_choice: "any"` enforcement, and a hook-style PostToolUse transformation.

Save as `examples/multi_tool_agent.py`. Each tool has a deliberately distinct description (the exam hammers on description quality). Errors carry `errorCategory` and `isRetryable`. The hook runs after every tool execution and normalizes timestamps.

```python
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
```

**Run it:** `python examples/multi_tool_agent.py`. You will observe Claude call `get_customer` first, then `lookup_order`, then `process_refund`. The hook normalizes the Unix timestamp on `lookup_order`'s result into ISO 8601 before Claude sees it. Try `$50` (passes), then try modifying the user request to refund `$600` — observe the structured `business`-category error propagate back without crashing the loop.

## Exercises

These four hands-on exercises mirror the **Preparation Exercises** in the official Exam Guide (§8), ordered easiest → hardest. Each reinforces one or more of the five exam domains, and each ships with a starter file that has `TODO` markers and hints — no finished solution.

- `exercises/01_agentic_loop_with_tools/` — **Easy.** Build a minimal agentic loop with distinct tool descriptions and a stop_reason switch. **(Domain 1: Agentic Architecture & Orchestration; Domain 2: Tool Design & MCP Integration)**
- `exercises/02_claude_code_team_config/` — **Medium.** Configure a multi-file Claude Code workspace: project `CLAUDE.md`, path-scoped rules in `.claude/rules/`, a project-scoped skill with `context: fork`, and an MCP server entry. **(Domain 3: Claude Code Configuration & Workflows; Domain 2: Tool Design & MCP Integration)**
- `exercises/03_structured_extraction_pipeline/` — **Hard.** Build a Python extraction pipeline using `tool_use` with a JSON schema, validation-retry on schema errors, and confidence-scored field-level output suitable for human-review routing. **(Domain 4: Prompt Engineering & Structured Output; Domain 5: Context Management & Reliability)**
- `exercises/04_multi_agent_research_pipeline/` — **Hardest.** Design a coordinator that spawns subagents in parallel via `Task`, propagates structured error context, preserves claim-source provenance, and structures the final report to distinguish well-established findings from contested ones. **(Domain 1: Agentic Architecture & Orchestration; Domain 2; Domain 5)**

Work through them in order. Each one prepares you for ~20–30% of the exam items.

## Research

### Reference URLs

All URLs were fetched and validated on October 11, 2026 (HTTP 2xx response, content read).

- [Claude Certified Architect – Foundations Certification (Skilljar exam page)](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification) — Official exam landing page; lists the three reference PDFs (Exam Guide, Terms, Exam Policy), exam code CCAR-F, and the $125 fee.
- [Claude Architect Learning Path (Skilljar)](https://anthropic-partners.skilljar.com/path/claude-architect) — Free Skillsjar learning path covering Agent Skills, MCP, subagents, Claude Code, and Delivery Readiness.
- [Claude Code Overview (official docs)](https://docs.claude.com/en/docs/claude-code/overview) — The canonical Claude Code docs entry point: what Claude Code is, where it runs (Terminal / VS Code / JetBrains / Web / Desktop), and what it can do.
- [Claude Agent SDK Overview (official docs)](https://docs.claude.com/en/api/agent-sdk/overview) — How the Agent SDK lets you embed Claude Code's loop, tools, hooks, sessions, and subagents in your own Python or TypeScript application.
- [Tool Use with Claude (official API docs)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — The conceptual model behind `tool_use`, `tool_result`, `tool_choice`, `stop_reason`, and the round-trip pattern every Domain 1 question assumes you know.
- [Agent Skills Overview (official API docs)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — How Skills (the `SKILL.md` + frontmatter pattern in Claude Code) load progressively, what counts as YAML frontmatter, and where they fit in Domain 3.

Local source (downloaded from Skilljar to `./sources/`):
- `sources/claude-certified-architect-foundations-exam-guide.pdf` — Official v1.0 Exam Guide (July 2026), 8 pages, the authoritative task-statement reference. Read this in full before sitting the exam.
- `sources/certification-terms-and-conditions.pdf` — Anthropic's certification terms.
- `sources/anthropic-certification-exam-policy.pdf` — Exam-day rules, Pearson VUE procedures, retake schedule.

## Next steps

You have three concrete paths from here. **Path A** (recommended for your timeline): start with `exercises/01_agentic_loop_with_tools/` and work through the four exercises in order — they cover 100% of the tested task statements and force you to internalize the tradeoffs. **Path B** (refresh-on-the-way): read the bundled `sources/claude-certified-architect-foundations-exam-guide.pdf` cover to cover; for every task statement you cannot immediately articulate, jump to the matching domain reference URL above. **Path C** (build a real thing): pick one of the six exam scenarios (customer support is the easiest to scope) and build a small end-to-end version in your own repo — the exam questions become obvious when you have a working system to point your judgment at.

Within 24 hours of registering, you can cancel or reschedule for free; after that the fee is forfeit. Plan to register for an exam date at least 2 weeks out so you have buffer to finish the exercises and re-read the official Exam Guide.