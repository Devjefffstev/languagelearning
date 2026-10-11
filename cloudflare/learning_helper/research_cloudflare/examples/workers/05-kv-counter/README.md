# 05 - Cloudflare KV

KV is Cloudflare's key/value store. Reads are super fast and globally cached, writes are eventually consistent (~60s to propagate everywhere). Good for counters, config, sessions, feature flags.

## One-time setup

```bash
# Production namespace
npx wrangler kv namespace create COUNTERS
# Preview namespace (used by `wrangler dev`)
npx wrangler kv namespace create COUNTERS --preview
```

Wrangler prints something like:

```
{ binding = "COUNTERS", id = "abcd1234..." }
```

Paste the IDs into `wrangler.jsonc` where it currently says `REPLACE_WITH_REAL_ID`.

## Run it

```bash
npm install
npm run dev
```

```bash
curl http://localhost:8787/        # visits: 1
curl -X POST http://localhost:8787/ # {"count":2}
curl -X DELETE http://localhost:8787/  # {"count":0,"reset":true}
```

## What's happening

- `env.COUNTERS` is a `KVNamespace`. `get(key)` returns `string | null`.
- `put(key, value)` is fire-and-forget but `await`able.
- `ctx.waitUntil(promise)` lets you do work *after* you've already returned a response — useful for logging or background writes.
- KV isn't transactional and isn't strongly consistent. For "true" counters you'd want Durable Objects.
