# Supabase Edge Functions

Custom TypeScript code on Supabase's edge network — your first step beyond REST.

## Description

An Edge Function is your own server code (TypeScript + Deno) running on Supabase's global edge network, called like an API endpoint from anywhere. The killer pattern: the function runs server-side with the **service_role key**, so it can read and write any table bypassing RLS — while your browser and Python clients keep using the safe publishable key. Use it for server-only logic like database reads, external API calls, or anything that needs a secret you don't want exposed in clients.

## Analogy

Back to the restaurant: the database is the kitchen, the REST API is the wait staff reading a fixed menu and following house rules (RLS). An Edge Function is the chef stepping into the kitchen with the master key — they can grab any ingredient (row) directly, including ones regular customers aren't allowed to order.

## Examples

### Quick setup

One-time CLI setup, from this guide's folder:

```bash
brew install supabase/tap/supabase
cd learning_helper/research_supabase_edge_functions
supabase login                          # browser auth
supabase init                           # creates supabase/config.toml
supabase link --project-ref <your-ref>  # same ref as your basics .env
```

Create + edit + deploy the function (the `secrets set` step is one-time per project):

```bash
# one-time: paste your service_role key (dashboard → Project Settings → API Keys → Secret key)
supabase secrets set SUPABASE_SERVICE_ROLE_KEY=<paste-your-secret-key>

supabase functions new greet            # scaffolds supabase/functions/greet/index.ts
cp examples/greet.ts supabase/functions/greet/index.ts
supabase functions deploy greet
```

Create a venv (reuse your basics guide's, or make a new one):

```bash
python3 -m venv .venv && .venv/bin/python3 -m pip install supabase python-dotenv
```

Run the caller (same `.env` as the basics guide):

```bash
.venv/bin/python3 examples/caller.py
```

**The function** (`examples/greet.ts`, deployed as `greet`):

```typescript
import { createClient } from 'npm:@supabase/supabase-js@2'

Deno.serve(async (req) => {
  const { word } = await req.json()
  const admin = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
  )
  const { data } = await admin
    .from('words')
    .select('word, translation, language')
    .eq('word', word)
    .maybeSingle()
  return Response.json({ found: !!data, word, ...(data ?? {}) })
})
```

**The Python caller** (`examples/caller.py`):

```python
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

result = supabase.functions.invoke("greet", {"body": {"word": "hola"}})
print(result.data)
# Found:    {'found': True, 'word': 'hola', 'translation': 'hello', 'language': 'spanish'}
# Not found: {'found': False, 'word': 'xyz'}
```

## Exercises

- `exercises/edge_greet/` — write the function (query the `words` table) and call it from Python (medium)

## Research

- https://supabase.com/docs/guides/functions/quickstart — CLI quickstart: scaffold, deploy, invoke.
- https://supabase.com/docs/guides/functions/secrets — how `supabase secrets set` works.
- https://github.com/supabase/supabase-py — `.functions.invoke` lives here.

All verified September 12, 2026.

## Next steps

After this: try mutating data inside the function (insert/update/delete via service_role), then swap the service_role client for a publishable-key client to write a function that respects RLS for an authenticated user.
