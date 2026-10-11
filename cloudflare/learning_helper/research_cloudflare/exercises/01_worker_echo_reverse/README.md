# Exercise 01 — Worker Echo Reverse

Practice adding a new route to an existing Worker. You'll extend the
`02-request-response` Worker with a `/reverse` endpoint that flips a string.

## Goal

Given a request to `/reverse?text=hello`, the Worker should respond with
`olleh`. The endpoint should also accept `POST` with the text in the body
(mirroring how `/upper` works in the example).

## Task

Open `starter/src/index.ts`. It contains a copy of the `02-request-response`
Worker. Find the `TODO` comment and implement the `/reverse` route.

Requirements:
- On `GET /reverse?text=...`, return the reversed string as plain text.
- On `POST /reverse` with the text in the body, do the same.
- If no text was provided (neither query nor body), return a `400` with a
  short message.

## Hints

1. Look at how `/upper` handles both `text` from the query string and the
   body — copy that pattern for reading the input.
2. To reverse a string in JavaScript: `"abc".split("").reverse().join("")`.
3. Return `new Response(reversed, { headers: { "content-type": "text/plain; charset=utf-8" } })`.
4. For the missing-text case, return `new Response("text required", { status: 400 })`.

## Success criteria

```bash
cd starter
npm install
npm run dev
```

```bash
curl 'http://localhost:8787/reverse?text=cloudflare'    # => "eralfduolc"
curl -X POST -d 'hello' http://localhost:8787/reverse   # => "olleh"
curl http://localhost:8787/reverse                      # 400 text required
```

Once all three commands behave as expected, you've got it.
