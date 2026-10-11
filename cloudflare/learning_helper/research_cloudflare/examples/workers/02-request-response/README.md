# 02 - Request / Response

Workers receive a [Web Fetch API `Request`](https://developer.mozilla.org/en-US/docs/Web/API/Request) and return a `Response` — same shape you'd use in the browser.

## Try it

```bash
npm install
npm run dev
```

```bash
curl http://localhost:8787/
curl http://localhost:8787/echo?foo=bar
curl -H 'x-custom: hi' http://localhost:8787/echo
curl http://localhost:8787/headers
curl 'http://localhost:8787/upper?text=hello'
curl -X POST -d 'hello' http://localhost:8787/upper
```

## What's happening

- `new URL(request.url)` lets you read `pathname`, `searchParams`, etc.
- `request.cf` exposes request metadata (country, colo, ...) — handy for geo-routing.
- `await request.text()` / `request.json()` / `request.formData()` reads the body. Workers don't buffer the body for you; you opt in.
- Returning `new Response(body, { status, headers })` is the whole response surface. Set `content-type` so clients know what they got.
