# Exercise 01 — Insert and Select

## Goal

Insert your first rows into the `words` table and read them back from Python — a complete write → read round trip through the Supabase REST API.

## Task

Open `starter.py` and complete the three `TODO`s:

1. Build a list of at least 5 dicts, each with the keys `word`, `translation`, and `language`.
2. Insert the whole list into `words` in one call, and print how many rows were inserted.
3. Select every row from `words` and print each one in the format `word — translation [language]`.

Before you start: run `examples/setup_quick.sql` in the Supabase SQL Editor, and finish the one-time setup from the guide README — `python3 -m venv .venv`, `source .venv/bin/activate`, `pip install supabase python-dotenv`, and `cp .env.example .env` filled in with your publishable key (or legacy `anon` key). In every new terminal, re-run `source .venv/bin/activate`.

## Hints

1. The client is already created for you at the top of the file. To see the pattern again, look at `examples/quick_setup.py`.
2. `insert(...)` accepts a list of dicts, and the dict keys must exactly match the table's column names.
3. Every query ends with `.execute()`; the resulting rows live in the response's `.data`.
4. If you see an error about the table not existing (404 or "relation ... does not exist"), you haven't run `setup_quick.sql` yet — or you misspelled `words`.

## Success criteria

- Running `python3 starter.py` prints the number of rows inserted (at least 5).
- It then lists every row in the table in the `word — translation [language]` format, including your new words.
- No exceptions. Note: `word` is a unique column, so running the script twice with identical words raises a duplicate-key error — that's Postgres protecting you. Use different words between runs.
