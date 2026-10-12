# Exercise 4 — Design and debug a multi-agent research pipeline

**Difficulty:** Hardest
**Domains reinforced:** Domain 1 (Agentic Architecture & Orchestration), Domain 2 (Tool Design & MCP Integration), Domain 5 (Context Management & Reliability)

## Goal

Design a coordinator/subagent architecture that meets the standard the official Exam Guide sets in §8 Exercise 4: coordinator with `allowedTools` including `Task`, parallel subagent execution, structured error propagation, and synthesis that preserves claim-source provenance across multiple sources.

## Task

Edit `starter.py` in this folder. The starter contains a single-agent loop. You will extend it so that on the topic **"the impact of AI on creative industries"**, the system:

1. Has a **coordinator agent** whose `allowedTools` includes `Task` (the subagent-spawning tool). The coordinator's system prompt specifies the research quality bar, NOT a rigid step-by-step sequence.
2. Spawns at least **three subagents in parallel**: a `web_search` subagent, a `document_analysis` subagent, and a `synthesis` subagent. Each receives its research question directly in the prompt (not via implicit context inheritance).
3. Each subagent returns a structured output: a list of `{claim, evidence_excerpt, source_url, publication_date, confidence}` objects. The synthesis subagent **preserves source attribution** when combining findings.
4. The coordinator **propagates structured errors** when a subagent fails: the error context includes `failure_type`, `attempted_query`, `partial_results`, and `potential_alternatives`. Demonstrably, you can simulate one subagent failure and the coordinator proceeds with the others.
5. The final report has **explicit sections** distinguishing well-established findings (consistent across multiple sources) from contested ones (sources disagree) from coverage gaps (where sources are unavailable).
6. The coordinator's task decomposition is **adaptable** — it analyzes the query and decides which subagents to invoke, rather than always running all three.

## Hints

1. You don't need to call live Claude twice for the parallel effect — you can use `client.messages.create` concurrently with `concurrent.futures.ThreadPoolExecutor` and gather the results, simulating the behavior of multiple Task tool calls in one coordinator turn. That's still the right model for the exam: the coordinator emits parallel work in one response, then collects.
2. For requirement 3, the structure `{claim, evidence_excerpt, source_url, publication_date, confidence}` is what the exam calls "structured claim-source mappings" and is the only way to preserve provenance through multi-source synthesis.
3. For requirement 4, simulate failure by raising a typed exception inside the subagent's section of the code and catching it in the coordinator's orchestration. Return a structured error dict, not a stringified exception.
4. For requirement 5, render different content types appropriately: financial figures as tables, news as prose, technical findings as structured lists. Don't force everything into a uniform format — that's an anti-pattern the exam flags.
5. For requirement 6, the coordinator should pick subagents based on query complexity. A simple query like "summarize this article" needs no subagents. A broad research query needs the full pipeline. The exam rewards "dynamically select which subagents to invoke rather than always routing through the full pipeline."

## Success criteria

Running `python starter.py` should:

- Print which subagents the coordinator decided to invoke, with one-line justifications
- Run the invoked subagents and print each subagent's structured claim list
- Produce a final report (as a `print()` of a structured object or markdown string) with three labeled sections: **Well-established findings**, **Contested findings**, **Coverage gaps**
- When you temporarily make the `web_search` subagent raise a `TimeoutError`, the coordinator's orchestration prints the structured error dict (`failure_type: "transient"`, etc.) and proceeds with the remaining subagents
- The final report shows the `web_search` topic as a coverage gap with the reason "subagent timed out"

If your coordinator crashes when a subagent fails, you've violated the structured-error-propagation rule. Wrap subagent calls in try/except blocks at the coordinator level and convert exceptions to structured error dicts before they propagate.

This is the most architecturally dense exercise on the exam. If you can complete it cleanly, you have the bones of the multi-agent-research scenario down.