# 03 - Routing

A Worker is one entry point. To stay organized you split logic into routes and dispatch with a tiny router.

## Try it

```bash
npm install
npm run dev
```

```bash
curl http://localhost:8787/
curl http://localhost:8787/about
curl http://localhost:8787/api/time
curl http://localhost:8787/api/users/42
```

## Layout

```
src/
├── index.ts          # entrypoint, declares the route table
├── router.ts         # tiny regex-based router
└── routes/
    ├── home.ts
    ├── about.ts
    ├── time.ts
    └── user.ts       # uses /api/users/:id params
```

## What's happening

- Each route is a file exporting a handler `(params, request) => Response`.
- The entrypoint builds a `[{ method, pattern, handler }]` table.
- `:id` style placeholders become regex groups and are passed in `params`.

## Real-world routers

The tiny router here is fine for demos. For real projects pick a battle-tested one:

- [itty-router](https://github.com/kwhitley/itty-router) — minimal, Workers-native.
- [Hono](https://hono.dev/) — fast, ergonomic, runs anywhere.

```bash
npm i hono
```
