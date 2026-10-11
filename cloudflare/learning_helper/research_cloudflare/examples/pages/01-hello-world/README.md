# 01 - Hello World (Pages)

A Pages project is two things:

1. **Static assets** in `public/` (HTML, CSS, images, anything).
2. **Functions** in `functions/` (Workers, file-routed).

This example has a static home page plus two tiny JSON endpoints.

## Run it

```bash
npm install
npm run dev
# -> http://localhost:8788
```

```bash
curl http://localhost:8788/
curl http://localhost:8788/api/hello
curl http://localhost:8788/api/time
```

## Layout

```
public/                 <- served verbatim
├── index.html
└── style.css

functions/              <- file-routed Workers (Pages Functions)
├── api/
│   ├── hello.ts        -> /api/hello
│   └── time.ts         -> /api/time
```

## How the routing works

The path to a Function file **is** its URL:

| File | URL |
|---|---|
| `functions/api/hello.ts` | `/api/hello` |
| `functions/api/users/[id].ts` | `/api/users/:id` |
| `functions/[[path]].ts` | catch-all |

Each file exports one of:

- `onRequestGet`, `onRequestPost`, ... (per-method)
- `onRequest(context)` for any method
- `onRequest` + a default export works too
