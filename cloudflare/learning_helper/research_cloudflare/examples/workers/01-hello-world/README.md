# 01 - Hello World

The smallest Worker that does anything useful. Every Worker exports an object with a `fetch` handler that receives a `Request` and returns a `Response`.

## Run it

```bash
npm install
npm run dev          # local server on http://localhost:8787
```

## Try it

```bash
curl http://localhost:8787/
# => Hello from a Cloudflare Worker!
```

## What's happening

- `export default { async fetch(request) { ... } }` is the worker shape Cloudflare calls.
- `_request` is the incoming `Request`. We ignore it for now.
- We return a plain text `Response`. Workers also accept JSON, HTML, streams, etc.
