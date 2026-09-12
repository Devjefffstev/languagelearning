# Exercise 04 (Capstone) — Vocabulary Tracker CLI

## Goal

Combine everything into a small command-line app: a loop where you can add, list, update, delete, and get stats — full CRUD against your Supabase database.

## Task

`starter.py` already has the menu loop and empty action functions. Implement all five `TODO`s:

1. `add_word()` — upsert, so re-adding an existing word updates it instead of failing.
2. `list_words()` — all rows ordered by `language,word`, with a `[x]`/`[ ]` checkbox showing `learned`.
3. `mark_learned()` — set `learned = True` for a word the user types.
4. `delete_word()` — delete a row by its `word`.
5. `show_stats()` — call `word_stats()` with `.rpc()`, like Exercise 03.

Before you start: make sure `examples/setup_complete.sql` has been run (it creates the schema, permissions, and the `word_stats()` function). Activate your `.venv` and have your `.env` at the guide root (see the README Quick setup) — re-run `source .venv/bin/activate` in every new terminal.

## Hints

1. Implement and test one function at a time, from the menu. Don't write all five and then start debugging.
2. `upsert({...}, on_conflict="word")` is the insert that never duplicates — `examples/complete_setup.py` shows the exact syntax.
3. For the checkbox: `"[x]" if row["learned"] else "[ ]"`.
4. `.order()` accepts a comma-joined column list, e.g. `.order("language,word")`.

## Success criteria

- You can add a word, see it in the list, mark it learned, delete it, and see stats — all without restarting the script.
- Invalid menu choices print a friendly message instead of crashing.
- Re-adding an existing word updates it: no duplicate rows, no errors.
