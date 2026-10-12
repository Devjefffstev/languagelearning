"""
Exercise 4 — Design and debug a multi-agent research pipeline.

SKELETON. Extend it so that:
  1. A coordinator function decides which subagents to invoke based on
     query complexity (not always the full pipeline).
  2. The invoked subagents run in PARALLEL (concurrent.futures).
  3. Each subagent returns structured claims:
        {"claims": [{"claim": ..., "evidence_excerpt": ...,
                     "source_url": ..., "publication_date": ...,
                     "confidence": float}]}
  4. The coordinator handles subagent failures with structured error dicts
     ({failure_type, attempted_query, partial_results, potential_alternatives}).
  5. The final report has three labeled sections: well-established findings,
     contested findings, coverage gaps.

The skeleton below contains a sequential single-agent loop. Replace it.
"""
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


# ----------------------------------------------------------------------------
# Topic + per-subagent prompts
# ----------------------------------------------------------------------------
TOPIC = "The impact of AI on creative industries"

SUBAGENT_PROMPTS = {
    "web_search": (
        "Search the web for {topic}. Return AT LEAST 6 distinct claims, each "
        "with evidence_excerpt, source_url, publication_date, and confidence "
        "(0.0-1.0). Output JSON only."
    ),
    "document_analysis": (
        "Analyze 3-5 research papers on {topic}. Return AT LEAST 6 claims, each "
        "with evidence_excerpt, source_url (paper PDF or DOI), "
        "publication_date, and confidence. Output JSON only."
    ),
    "synthesis": (
        "Given these findings {findings}, return AT LEAST 6 claims that "
        "aggregate them. Preserve source_url and publication_date. Output JSON only."
    ),
}


# ----------------------------------------------------------------------------
# TODO(step 1): Implement a coordinator function that picks subagents based on
# the query. For a simple query ("summarize this article") it should run
# NO subagents (the existing snippet can handle it). For a broad research
# query like TOPIC, it should run all three. Return a list of subagent names.
# ----------------------------------------------------------------------------
def decide_subagents(query: str, complexity: str) -> list[str]:
    if complexity == "simple":
        return []
    if complexity == "broad":
        return ["web_search", "document_analysis", "synthesis"]
    return ["web_search"]


# ----------------------------------------------------------------------------
# TODO(step 2): Implement a subagent function that calls the API and returns
# structured JSON. The output must be a list of claims with metadata.
# ----------------------------------------------------------------------------
def run_subagent(name: str, prompt: str) -> dict:
    """Call Claude with the subagent prompt. Return structured claims.

    On any API error, raise a typed error. The coordinator will convert
    that error to a structured error dict, not a stringified exception.
    """
    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    # TODO: parse response.content into {"claims": [...]}
    return {"claims": []}  # placeholder


# ----------------------------------------------------------------------------
# TODO(step 4): Implement structured error propagation. When a subagent raises,
# catch it at the coordinator level and return a dict:
#   {
#     "failure_type": "transient" | "validation" | "permission" | "business",
#     "attempted_query": <the prompt>,
#     "partial_results": <whatever was returned before failure>,
#     "potential_alternatives": [...],
#     "isRetryable": bool
#   }
# The final report must include the failed topic as a coverage gap.
# ----------------------------------------------------------------------------
def to_structured_error(name: str, attempted_query: str, exc: Exception) -> dict:
    """Skeleton: returns a dict but does NOT yet include the full fields."""
    return {"subagent": name, "error": str(exc)}


# ----------------------------------------------------------------------------
# TODO(step 3): Run chosen subagents IN PARALLEL.
# ----------------------------------------------------------------------------
def run_subagents_parallel(subagent_names: list[str]) -> dict[str, dict | dict]:
    """Run subagents concurrently. Each entry in the result is either
    {"claims": [...]} for success or a structured error dict for failure."""
    # Skeleton: sequential, no error handling.
    results = {}
    for name in subagent_names:
        prompt = SUBAGENT_PROMPTS[name].format(topic=TOPIC, findings="(none)")
        try:
            results[name] = run_subagent(name, prompt)
        except Exception as exc:
            # TODO(step 4): replace with to_structured_error(...)
            results[name] = {"subagent": name, "error": str(exc)}
    return results


# ----------------------------------------------------------------------------
# TODO(step 5): Render the final report with three labeled sections.
# Distinguish findings that appear in multiple sources (well-established)
# from findings that appear once (single-source) and from topics where
# a subagent failed (coverage gaps).
# ----------------------------------------------------------------------------
def render_report(all_results: dict[str, dict]) -> str:
    """Skeleton: prints everything flat. Replace with structured sections."""
    out = ["Multi-agent research report (skeleton):"]
    for name, payload in all_results.items():
        out.append(f"  {name}: {payload}")
    return "\n".join(out)


# ----------------------------------------------------------------------------
# Demo driver
# ----------------------------------------------------------------------------
def main() -> None:
    query = TOPIC
    complexity = "broad"  # try "simple" too
    chosen = decide_subagents(query, complexity)
    print(f"Coordinator invoked: {chosen}")
    if not chosen:
        print("(simple query — running single agent)")
        # TODO: trivial path
        return
    results = run_subagents_parallel(chosen)
    report = render_report(results)
    print(report)


if __name__ == "__main__":
    main()