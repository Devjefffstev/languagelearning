# Exercise 05 — Edge Function: Read from the Database

## Goal

Write and deploy an Edge Function that reads a row from your `words` table using the service_role key, then call it from Python.

## What's the pattern?

A function runs server-side with secrets it can read via `Deno.env.get(...)`. You pass it `SUPABASE_SERVICE_ROLE_KEY` once via `supabase secrets set`, the function builds an admin Supabase client, and queries any table bypassing RLS.

## Task

Complete the 4 `TODO`s in `greet_starter.ts` (build the admin client, read the request body, query `words`, return the response), deploy with `supabase functions deploy greet`, then complete `TODO 1` in `caller_starter.py` to invoke it from Python.

## Prereqs

- Supabase CLI: `brew install supabase/tap/supabase`
- From this folder:

```bash
cd learning_helper/research_supabase_edge_functions
supabase login
supabase init
supabase link --project-ref <your-ref>      # same ref as your basics .env
supabase functions new greet                # creates supabase/functions/greet/index.ts
```

  Replace the scaffolded `supabase/functions/greet/index.ts` with this folder's `greet_starter.ts`.
- Set the secret (get it from dashboard → Project Settings → API Keys → Secret key):

  ```bash
  supabase secrets set SUPABASE_SERVICE_ROLE_KEY=<paste-secret-key>
  ```
- Reuse your basics `.venv` (already has supabase + python-dotenv), or create one here: `python3 -m venv .venv && .venv/bin/python3 -m pip install supabase python-dotenv`.

## Hints

1. The admin client is just `createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!)`.
2. `SUPABASE_URL` is auto-injected into Edge Functions; you only need to `supabase secrets set SUPABASE_SERVICE_ROLE_KEY`.
3. The query is `.from('words').select('word, translation, language').eq('word', word).maybeSingle()` — `maybeSingle()` returns null instead of erroring when nothing matches.
4. Spread the row with `...(data ?? {})` so the response shape stays consistent whether or not a row was found.

## Success criteria

- `supabase secrets set SUPABASE_SERVICE_ROLE_KEY=...` and `supabase functions deploy greet` both succeed.
- `caller_starter.py` printing an existing word (e.g. `hola`) returns a dict with `found: True` and the row's columns.
- Calling with a word that doesn't exist returns `{'found': False, 'word': '...'}` (no error).
