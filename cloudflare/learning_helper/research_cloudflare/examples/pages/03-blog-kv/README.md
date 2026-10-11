# 03 - Blog with KV

Same UI as 02-with-functions, but posts live in **Cloudflare KV** instead of an in-memory list. State survives reloads and deploys.

## One-time setup

```bash
npx wrangler kv namespace create POSTS
npx wrangler kv namespace create POSTS --preview
```

Paste the printed IDs into `wrangler.jsonc` where it says `REPLACE_WITH_REAL_ID`.

## Try it

```bash
npm install
npm run dev
# -> http://localhost:8788
```

Then click around the page, or:

```bash
curl http://localhost:8788/api/posts
curl -X POST http://localhost:8788/api/posts \
  -H 'content-type: application/json' \
  -d '{"title":"Persisted","body":"Stored in KV."}'
```

## What's happening

- `env.POSTS` is a `KVNamespace` (the binding is declared in `wrangler.jsonc`).
- Each post is stored under its id as a JSON string.
- Listing does a `posts.list()` then a `get` per key — fine for tens of items; switch to a list-of-ids pattern for thousands.
- KV writes are eventually consistent (≈60s globally). Reads are fast and consistent at the edge.
