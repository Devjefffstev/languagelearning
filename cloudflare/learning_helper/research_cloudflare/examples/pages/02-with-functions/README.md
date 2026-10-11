# 02 - With Functions

A Pages site with multiple Function endpoints and a tiny front-end that calls them. Posts live in an in-memory list shared across Functions via ESM imports — useful for demos, not for production (use KV, see 03).

## Try it

```bash
npm install
npm run dev
# -> http://localhost:8788
```

```bash
curl http://localhost:8788/api/posts
curl -X POST http://localhost:8788/api/posts \
  -H 'content-type: application/json' \
  -d '{"title":"Third post","body":"From curl"}'
curl http://localhost:8788/api/posts/1
curl -X DELETE http://localhost:8788/api/posts/1
```

## Layout

```
public/
├── index.html
└── style.css

functions/api/posts/
├── _store.ts        # shared in-memory list (ESM import works)
├── index.ts         # /api/posts        (GET, POST)
└── [id].ts          # /api/posts/:id    (GET, DELETE)
```

## How routing works

The path to a Function file **is** its URL. Bracketed names become params:

- `functions/api/posts/index.ts` -> `/api/posts`
- `functions/api/posts/[id].ts` -> `/api/posts/:id` with `params.id`

Pages Functions are full Workers — they support imports, modules, and bindings like KV (see 03-blog-kv).
