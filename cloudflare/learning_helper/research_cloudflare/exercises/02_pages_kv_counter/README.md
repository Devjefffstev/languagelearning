# Exercise 02 — Pages + KV Counter

Build a Pages site that uses a Pages Function and Cloudflare KV to keep a
global counter that survives restarts.

## Goal

- `GET /api/count` returns `{ count: <number> }`.
- `POST /api/count` increments the counter and returns the new value.
- The page at `/` shows the current count and has a button to increment it.

## Task

Fill in `starter/functions/api/count.ts` (the file currently returns 501 with
a `TODO`). You'll also need to:

1. Create a KV namespace and paste its IDs into `starter/wrangler.jsonc`
   (see Setup below).
2. Wire the front-end in `starter/public/index.html` so it calls
   `/api/count` on load and on button click.

## Setup

```bash
npx wrangler kv namespace create COUNTERS
npx wrangler kv namespace create COUNTERS --preview
```

Paste the printed IDs into `wrangler.jsonc` where it says
`REPLACE_WITH_REAL_ID`.

## Hints

1. The binding `env.COUNTERS` is a `KVNamespace`. Read with
   `await env.COUNTERS.get(key)` and write with `await env.COUNTERS.put(key, value)`.
2. `get` returns `string | null`. Wrap in `Number(value ?? "0")` to default to 0.
3. On POST: read, increment, write, return JSON.
4. The HTML page just needs `fetch("/api/count")` on load and on click — no
   external libraries required.

## Success criteria

```bash
cd starter
npm install
npm run dev
```

```bash
curl http://localhost:8788/api/count              # {"count":1} (or higher on reload)
curl -X POST http://localhost:8788/api/count      # {"count":2}
```

Reload the page a few times — the counter must keep going up, never reset.
