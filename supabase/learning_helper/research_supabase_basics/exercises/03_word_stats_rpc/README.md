# Exercise 03 — Call a Postgres Function with RPC

## Goal

Move work into the database: call a custom SQL function (`word_stats()`) from Python with `.rpc()`, and cross-check it against an exact row count.

## Task

1. Run `stats_function.sql` (this folder) in the SQL Editor. It creates `word_stats()`, which groups words by language and counts totals and learned words — inside Postgres, not in Python.
2. Complete the three `TODO`s in `starter.py`:
   - Call the function via `.rpc("word_stats")` and print one line per language.
   - Get the total row count with `.select("*", count="exact")`.
   - Sum the per-language totals and compare with the count; print `MATCH` or `MISMATCH`.

Before you start: activate your `.venv` and have your `.env` at the guide root (see the README Quick setup) — re-run `source .venv/bin/activate` in every new terminal.

## Hints

1. `.rpc("word_stats")` takes the function name exactly as written in the SQL — lowercase, no parentheses.
2. The response's `.data` is a list of dicts with the keys the function returns: `language`, `total`, `learned_count`.
3. For the exact count: `res = supabase.table("words").select("*", count="exact").execute()`, then read `res.count`.
4. If `.rpc()` returns a permissions error, re-run `stats_function.sql` — it ends with a `grant execute ... to anon` that makes the function callable with the anon key.

## Success criteria

- The script prints a per-language summary like `spanish: 4 words, 1 learned`.
- The last line prints `MATCH`.
