# Exercise 3 — Build a structured data extraction pipeline

**Difficulty:** Hard
**Domains reinforced:** Domain 4 (Prompt Engineering & Structured Output), Domain 5 (Context Management & Reliability)

## Goal

Build a Python extraction pipeline that meets the standard the official Exam Guide sets in §8 Exercise 3: `tool_use` with a JSON schema, validation-retry on schema errors, few-shot examples handling varied document formats, batch processing with the Message Batches API, and a confidence-based human-review routing strategy.

## Task

Edit `starter.py` in this folder. The starter contains a basic synchronous `/v1/messages` call. You will extend it so that:

1. You define an **extraction tool** with a JSON schema containing **at least 3 required fields, at least 2 optional fields, one enum, and one nullable field** for an invoice schema (`invoice_number`, `vendor_name`, `invoice_date`, `subtotal`, `tax`, `total`, `line_items[]`, `payment_terms`).
2. You use `tool_choice={"type": "tool", "name": "extract_invoice"}` so the extraction is **always** the first turn and is never skipped for chat-style responses.
3. You implement a **validation-retry loop**: when Pydantic rejects the response (parse error, missing required, semantic error like `line_items.sum() != total`), you send a follow-up `messages.create` call that includes the original document, the failed extraction, and the specific validation error string. Cap retries at 2.
4. You include **at least two few-shot examples** in your system prompt showing extraction from documents with different structures (e.g., one with `total` stated near the top, one with line items inline in a narrative).
5. You add a `field_confidence` field to your schema — an object `{ invoice_number: 0.97, total: 0.82, ... }` — and write a `route_for_review(extraction)` function that flags the extraction for human review if any field's confidence is below 0.7, OR if the document contained `payment_terms` reading "net 90" or longer (a business rule).
6. You **do not** implement the actual batching in this exercise. Instead, write a commented `process_batch(documents: list[str])` function that submits to `client.messages.batches.create(...)`, polls, and identifies failures by `custom_id`. The comment skeleton must reference the 50% cost savings and the 24-hour SLA from the Exam Guide.

## Hints

1. For requirement 1, model your schema on a `TypedDict` or `pydantic.BaseModel`. If you don't have pydantic installed, `pip install pydantic` — the exam assumes you do.
2. For requirement 3, the **second** `messages.create` call has a slightly different shape: the new `user` turn contains **text** (the validation error) plus an **inner** reference to the original tool result. The exact format is in the [Tool Use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).
3. For requirement 4, keep examples short — one input/output pair each, no more than ~200 tokens combined.
4. For requirement 5, the model emits `field_confidence` as a free-form dict; you validate ranges with Pydantic and route accordingly.
5. For requirement 6, the `custom_id` field is your correlation key. Anthropic returns results keyed by it, so you can resubmit only failures.

## Success criteria

Running `python starter.py` on the two sample invoices in the starter docstrings should:

- Extract all required fields correctly
- Return a Pydantic-validated object (no schema syntax errors)
- Populate `field_confidence` for at least the required fields
- Call `route_for_review(...)` and print either `"Auto-approved"` or `"Routed to human review: <reason>"` for each invoice
- One of the two test invoices should be **routed to review** (e.g., because the total is missing or a confidence score is below 0.7), the other auto-approved
- The validation-retry loop should be visible: if you temporarily corrupt the model output (e.g., by overriding response parsing), the loop should attempt a retry exactly once before giving up

If your output ends with a Pydantic `ValidationError` that hasn't been caught, you've broken the retry loop. Wrap each extraction attempt in `try/except` and append the message that triggered failure before retrying.