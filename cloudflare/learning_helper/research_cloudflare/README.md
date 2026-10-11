# Cloudflare Workers & Pages — A Beginner's Tour

## Description

Cloudflare runs code in hundreds of data centers around the world. Two products sit on top of that network: **Workers** and **Pages**.

A **Worker** is a small piece of code (a function) that runs on Cloudflare's edge whenever an HTTP request hits it. You write it, deploy it, and from then on every request is served by a server physically close to the user — often under 20ms. Workers are great for APIs, JSON transforms, A/B tests, scheduled jobs, and glue between services.

**Pages** is Cloudflare's static-site host. You drop HTML/CSS/JS in a folder and Pages serves it from the edge too. The trick: Pages also supports **Functions** — full Workers that live inside the `functions/` folder and are auto-routed by file path. So a Pages project can be 100% static, 100% dynamic, or (most commonly) a static front-end with a few API endpoints.

The mental model is the same for both: **request comes in, function returns a response.** The differences are mostly about packaging and routing.

## Analogy

Think of Cloudflare's edge as a chain of hundreds of tiny post offices scattered around the world.

A **Worker** is like hiring one postmaster per office and giving each the same instruction manual ("when a letter arrives with this stamp, forward it; with that stamp, return a form letter"). Same logic everywhere, executed locally.

A **Pages** site is like publishing a magazine that's printed in every post office — same content, available everywhere. And **Pages Functions** are little reply slips tucked into the magazine: when a reader fills one out and mails it back, the postmaster processes it before anything is reprinted.

In both cases the post office (data center) is close to the reader, so round-trip is fast.

## Examples

The `examples/` directory contains runnable projects. Start with the smallest and work up.

### Workers

- `examples/workers/01-hello-world/` — the smallest Worker.
- `examples/workers/02-request-response/` — inspect Request, build Responses (JSON, plain text, headers).
- `examples/workers/03-routing/` — split a Worker into a tiny router + per-route handlers.
- `examples/workers/04-env-and-secrets/` — `vars`, `.dev.vars`, and `wrangler secret put`.
- `examples/workers/05-kv-counter/` — durable state with Cloudflare KV.

### Pages

- `examples/pages/01-hello-world/` — static site + one tiny Pages Function.
- `examples/pages/02-with-functions/` — multi-endpoint Pages Functions with an in-memory store.
- `examples/pages/03-blog-kv/` — same shape, but state lives in KV.
- `examples/pages/04-calling-worker/` — the headline example: a Worker called from a Pages Function via a **service binding**.
- `examples/pages/05-langgraph-ai/` — a Pages site that calls a **Python LangGraph agent** (Anthropic Claude by default) over HTTP. The agent is model-agnostic — the README shows the 1-line swap to OpenAI / Gemini / Groq / Cloudflare Workers AI. Demonstrates the "any LLM API" pattern.

### Example #1 — A standalone Worker (quick)

```bash
cd examples/workers/01-hello-world
npm install
npm run dev          # -> http://localhost:8787
curl http://localhost:8787/
```

The whole Worker is:

```ts
export default {
  async fetch(_request: Request): Promise<Response> {
    return new Response("Hello from a Cloudflare Worker!", {
      headers: { "content-type": "text/plain; charset=utf-8" },
    });
  },
};
```

### Example #2 — Pages calling a Worker (complete)

The most realistic pattern is a Pages site that calls a separate Worker over a **service binding** — server-to-server, no public URL. See `examples/pages/04-calling-worker/`. It contains:

- `worker/` — a tiny Worker with `POST /echo`.
- `site/` — a Pages site with two buttons: one calls the Worker directly from the browser, the other goes through a Pages Function that uses a service binding (`env.API.fetch(...)`) so secrets never leak.

### Example #3 — Pages calling a Python LangGraph agent (off-platform backend)

The first example that leaves the JS-only path. See `examples/pages/05-langgraph-ai/`. A LangGraph agent (Python, FastAPI, Anthropic Claude) is exposed at `POST /chat`. A Pages function at `site/functions/api/chat.ts` forwards browser requests to it. The `ANTHROPIC_API_KEY` lives only in the agent's process.

## Exercises

Hands-on practice, easiest first. Each folder has a `README.md` (the brief) and a `starter/` folder with the scaffold to fill in. Hints are inside each README — no full solutions shipped.

- `exercises/01_worker_echo_reverse/` — extend a Worker to add a `/reverse` endpoint that flips a string. (Beginner)
- `exercises/02_pages_kv_counter/` — build a Pages site + Function that keeps a global counter in KV. (Intermediate)
- `exercises/03_pages_calls_worker/` — wire up a Pages site to call a Worker via a service binding. (Intermediate-advanced)

## Research

### Reference URLs (last verified Sep 2026)

- https://developers.cloudflare.com/workers/ — official Workers docs: runtime, APIs, bindings.
- https://developers.cloudflare.com/pages/ — official Pages docs, including Functions routing conventions.
- https://developers.cloudflare.com/workers/runtime-apis/service-bindings/ — how `env.SERVICE.fetch()` works, with examples.
- https://developers.cloudflare.com/workers/runtime-apis/kv/ — KV namespace API (`get`, `put`, `list`, `delete`).
- https://developers.cloudflare.com/pages/functions/ — Pages Functions reference (routing, middleware, examples).
- https://github.com/cloudflare/workers-sdk — Wrangler + Miniflare source; useful for issue search and recent changes.
- https://langchain-ai.github.io/langgraph/ — LangGraph docs (the framework used in example 05).
- https://docs.anthropic.com/en/api/getting-started — Anthropic Claude API (the default LLM in example 05).

## Next steps

After working through the examples and exercises, the natural next directions are:

- **Bindings beyond KV**: R2 (object storage), D1 (SQLite at the edge), Durable Objects (strongly consistent state). The order to learn them in: KV → D1 → R2 → Durable Objects.
- **Real-world patterns**: caching, rate limiting, auth at the edge, scheduled Workers (cron), and the "smart placement" hint.
- **Routers**: swap the tiny hand-rolled router in `03-routing` for [Hono](https://hono.dev/) or [itty-router](https://github.com/kwhitley/itty-router) — both are tiny and Workers-native.
- **Agent backends**: example 05 shows a Python LangGraph agent. The same shape works with Google ADK, Pydantic AI, raw OpenAI Agents SDK, or anything else that speaks HTTP. Pick the framework that matches your team's taste; the Pages side doesn't care.