# Exercise 03 — Pages Calls Worker (Service Binding)

Build the same pattern as `examples/pages/04-calling-worker` from scratch.
This cements the service-binding flow: a standalone Worker, a Pages Function
that calls it, and a static front-end that drives the call.

## Goal

- A Worker (`worker/`) accepts `POST /ping` with a JSON body and returns
  `{ pong: true, receivedAt, payload }`.
- A Pages Function (`site/functions/api/proxy.ts`) calls the Worker via a
  service binding, forwards an `x-internal-token` header, and wraps the
  response with `{ via: "service-binding", worker: <worker-json> }`.
- The static page (`site/public/index.html`) shows a button that calls
  `/api/proxy` and displays the result.

## Task

Three files have TODOs:
- `starter/worker/src/index.ts` — implement `POST /ping`.
- `starter/site/functions/api/proxy.ts` — call the bound Worker.
- `starter/site/public/index.html` (the inline `<script>`) — call
  `/api/proxy` on click.

The rest of the scaffold (config, package.json, etc.) is already wired.

## Hints

1. In the Worker: `await request.json()` reads the body, then return
   `Response.json({ ... })`.
2. In the Function: `env.API` is a `Fetcher` (because of the `services` block
   in `wrangler.jsonc`). Call it with `await env.API.fetch(new Request(...))`.
3. Pass `env.INTERNAL_TOKEN` as a header so the Worker can verify the
   caller. Reading it as a header doesn't expose it to the browser.
4. The URL passed to `env.API.fetch` doesn't need to be real — it's parsed
   but not fetched from the network. Use `https://internal/ping` or similar.

## Success criteria

Run in two terminals:

```bash
cd starter/worker
npm install
npm run dev       # -> http://localhost:8789

cd ../site
npm install
printf 'INTERNAL_TOKEN="dev-secret"\n' > .dev.vars
npm run dev       # -> http://localhost:8790
```

Then:

```bash
curl -X POST http://localhost:8790/api/proxy \
  -H 'content-type: application/json' \
  -d '{"hello":"binding"}'
```

Expected response shape:

```json
{
  "via": "service-binding",
  "worker": {
    "pong": true,
    "receivedAt": "...",
    "payload": { "hello": "binding" }
  }
}
```

Open the page at `http://localhost:8790` — clicking the button should print
the same JSON.
