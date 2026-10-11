# 04 - Calling a Worker from Pages

The headline example. Shows **two ways** to call a Cloudflare Worker from a Pages project, side by side:

1. **Direct (browser → Worker)** — easy, but the Worker needs a public URL and any secret it relies on is reachable from the client.
2. **Via service binding (browser → Pages Function → Worker)** — secure, server-to-server, lower latency, no public URL needed for the Worker.

## Layout

```
04-calling-worker/
├── worker/                 <- the standalone Worker
│   ├── package.json
│   ├── wrangler.jsonc
│   ├── tsconfig.json
│   └── src/index.ts
└── site/                   <- the Pages site that calls it
    ├── package.json
    ├── wrangler.jsonc
    ├── public/
    │   ├── index.html
    │   ├── app.js
    │   └── style.css
    └── functions/
        └── api/
            └── via-binding.ts
```

## Run it (local dev, two terminals)

```bash
# Terminal 1 — the Worker
cd worker
npm install
npm run dev       # -> http://localhost:8789
```

```bash
# Terminal 2 — the Pages site
cd site
npm install
printf 'INTERNAL_TOKEN="dev-secret"\n' > .dev.vars
npm run dev       # -> http://localhost:8790
```

Then open `http://localhost:8790`:

- Click **Call /api/via-binding** — works out of the box. `wrangler pages dev` auto-wires the local Worker to the `API` binding by name.
- For the direct browser→Worker call, open `site/public/app.js` and set `WORKER_URL = "http://localhost:8789"`, then reload the page.

## How the service binding works

In `site/wrangler.jsonc`:

```jsonc
{
  "services": [
    { "binding": "API", "service": "calling-worker-api" }
  ]
}
```

This makes `env.API` available to every Function in the Pages project. `env.API` is a `Fetcher`, so you call it like a regular fetch handler:

```ts
const res = await env.API.fetch(new Request("https://internal/echo", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify(payload),
}));
```

The URL passed to `env.API.fetch` is parsed but not actually contacted over the network — Cloudflare routes it to the bound Worker in-process. That's why the binding is faster, more secure, and works even when the bound Worker has no public URL.

## Why two ways?

| | Direct (browser→Worker) | Service binding (browser→Function→Worker) |
|---|---|---|
| Public Worker URL required | yes | no |
| Latency | extra DNS / TLS hop | one in-process call |
| Can keep server-side secrets | no (browser sees them) | yes |
| Browser can be a client of the API | yes | no (Function is the only client) |

For most production setups you'll use the **service binding** path. The direct path is useful for demos and when the Worker really is meant to be a public API.

## Deploying

```bash
# Worker first — the Pages binding needs the Worker to exist
cd worker
npx wrangler deploy

# Then the Pages site
cd ../site
npx wrangler pages deploy public
```

For the direct browser call once deployed, update `site/public/app.js` with your `*.workers.dev` URL and redeploy the site.
