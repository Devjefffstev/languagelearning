"""
Exercise 3 — Build a structured data extraction pipeline.

SKELETON. Extend it so that:
  1. You define an `extract_invoice` tool with a JSON schema covering at
     least 3 required fields, 2 optional fields, one enum, and one nullable.
  2. You set tool_choice={"type": "tool", "name": "extract_invoice"}.
  3. You implement a validation-retry loop (Pydantic) capped at 2 retries.
  4. You include at least 2 few-shot examples in the system prompt for
     documents with different structures.
  5. You add `field_confidence: dict[str, float]` to the schema and a
     `route_for_review(extraction)` function that flags low-confidence
     fields or payment_terms >= "net 90".
  6. You write a COMMENTED skeleton for `process_batch()` that references
     the Message Batches API and the 24-hour SLA / 50% cost savings.

The skeleton below contains a working basic call so you can iterate.
"""
import json
import os
from typing import Optional

from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


# ----------------------------------------------------------------------------
# Sample documents (two invoice shapes — vary the structure between them).
# ----------------------------------------------------------------------------
SAMPLE_INVOICE_FRONT_LOADED = """
INVOICE INV-2026-0042
Date: 2026-09-14
Vendor: Apex Logistics, LLC
Total: $3,247.50
"""

SAMPLE_INVOICE_LINE_ITEM_HEAVY = (
    "Apex Logistics billed us for the following in September 2026: "
    "$2,100 for line-haul transport between Sept 1 and Sept 14, "
    "$847.50 in fuel surcharges, and $300 in accessorial fees. "
    "Net 90. Invoice number INV-2026-0099."
)


# ----------------------------------------------------------------------------
# TODO(step 1): Define the extraction tool schema.
# Required fields: invoice_number, vendor_name, total (number)
# Optional fields: subtotal, tax, payment_terms
# One enum: status in {"paid", "unpaid", "overdue", "unclear"}
# One nullable: notes (string | null)
# Plus field_confidence: dict[str, float] for requirement 5.
# ----------------------------------------------------------------------------
EXTRACT_INVOICE_SCHEMA: dict = {
    # TODO: fill in properties, required[], etc.
}


# TODO(step 2): Build the TOOLS list — a single entry with name "extract_invoice"
# and input_schema=EXTRACT_INVOICE_SCHEMA.


# TODO(step 4): A system prompt with at least 2 few-shot examples covering the
# two SAMPLE_INVOICE shapes above. Keep examples under ~200 tokens combined.
SYSTEM_PROMPT = "You extract structured data from invoices."


# TODO(step 5): Define `route_for_review(extraction: dict) -> tuple[bool, str]`
# It returns (True, "<reason>") if any field_confidence value < 0.7 OR
# if payment_terms is in {"net 90", "net 120"} (or longer), else (False, "").


# ----------------------------------------------------------------------------
# Agent loop with validation-retry
# ----------------------------------------------------------------------------
def extract_invoice(document: str, max_retries: int = 2) -> dict:
    """Run the extraction, retrying on schema failures up to max_retries.

    TODO(step 3): implement validation-retry. When the model returns an
    extraction that fails Pydantic validation, send a follow-up message:
      - the original document
      - the failed extraction
      - the specific validation error string
    Then re-call /v1/messages with tool_choice forced to "extract_invoice".
    Cap retries at max_retries.
    """
    # Skeleton: a single call, no retries, no validation.
    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        # TODO(step 2 cont.): tools=[{...}],
        # TODO(step 2 cont.): tool_choice={"type": "tool", "name": "extract_invoice"},
        messages=[{"role": "user", "content": document}],
    )

    # TODO(step 3): Parse the tool_use response into a dict, validate against
    # a Pydantic model. On ValidationError, append a user message containing
    # the error and recurse. After max_retries retries, raise.

    return {"raw": response.content}  # placeholder — replace


def process_batch(documents: list[str]) -> list[dict]:
    """Skeleton for the batching portion of the exercise.

    TODO(step 6): Implement (or comment) the Message Batches API path.
    - Submit via client.messages.batches.create(requests=[...]).
    - Each request has a `custom_id` you choose for correlation.
    - Poll until status="ended" (up to 24 hours; NO latency SLA).
    - Identify failures by custom_id and resubmit only the failed docs,
      possibly with a chunking transformation if they exceeded context.
    - Note: the Message Batches API does NOT support multi-turn tool calls
      within a single request. It is appropriate ONLY for non-blocking,
      latency-tolerant workloads (overnight reports). It is NOT appropriate
      for pre-merge checks.
    """
    raise NotImplementedError("process_batch — see TODO(step 6) comment")


# ----------------------------------------------------------------------------
# Demo driver
# ----------------------------------------------------------------------------
def main() -> None:
    for label, doc in [
        ("front-loaded", SAMPLE_INVOICE_FRONT_LOADED),
        ("line-item-heavy", SAMPLE_INVOICE_LINE_ITEM_HEAVY),
    ]:
        extraction = extract_invoice(doc)
        # TODO(step 5): call route_for_review(extraction) and print either
        # "Auto-approved" or "Routed to human review: <reason>"
        print(f"[{label}] extraction={extraction!r}")


if __name__ == "__main__":
    main()