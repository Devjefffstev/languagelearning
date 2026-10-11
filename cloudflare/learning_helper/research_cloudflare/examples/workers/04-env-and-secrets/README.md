# 04 - Env vars & secrets

Workers read configuration from `env`, the second argument to `fetch`. There are three flavors:

| Source | Where | Visibility |
|---|---|---|
| `vars` block in `wrangler.jsonc` | file, committed | non-sensitive |
| `.dev.vars` | local file, gitignored | local dev only |
| `wrangler secret put NAME` | encrypted in Cloudflare dashboard | production secrets |

## Try it

```bash
npm install
npm run dev
```

```bash
curl 'http://localhost:8787/?name=Ada'
# => {"message":"Hello, Ada!","environment":"development","apiKey":"de***90 (len=20)"}
```

## Deploying secrets

```bash
npx wrangler login
npx wrangler secret put API_KEY   # prompts you to type the value
npx wrangler deploy
```

`wrangler secret put` encrypts the value and stores it on Cloudflare. It never appears in `wrangler.jsonc` or in git.

## Why mask the secret?

Logging the raw `API_KEY` would leak it. The example returns only the first/last 2 chars and length, enough to prove the secret is loaded without exposing it.
