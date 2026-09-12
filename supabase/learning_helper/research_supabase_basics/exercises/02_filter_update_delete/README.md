# Exercise 02 — Filter, Update, Delete

## Goal

Practice targeting specific rows: filter your reads with `.eq(...)`, then change rows with `update` and remove rows with `delete` — always through a filter.

## Task

Complete the four `TODO`s in `starter.py`:

1. Fetch only Spanish words with `learned = false`, ordered alphabetically by `word`, and print them.
2. Pick one of those words and mark it as learned using `update` + `.eq(...)`.
3. Select one row, read its `id`, and delete that row by `id`.
4. Re-fetch all rows and print the total count so you can see the result.

Before you start: run `examples/setup_complete.sql` — it adds the `learned` column and the update/delete permissions. It rebuilds the table, so re-run `examples/complete_setup.py` (or insert words manually) if the table ends up empty. Activate your `.venv` and have your `.env` at the guide root (see the README Quick setup) — re-run `source .venv/bin/activate` in every new terminal.

## Hints

1. Filters chain between the column selection and `.execute()`: `.select("*").eq("language", "spanish").eq("learned", False).order("word")`.
2. `update({...})` and `delete()` also need an `.eq(...)` filter before `.execute()` — without one, you would hit every row in the table.
3. `learned` is a real boolean column — pass Python `True`/`False`, not the strings `"true"`/`"false"`.
4. To delete by id: select the row first (for example `.eq("word", ...)`), read `rows[0]["id"]`, then call `.delete().eq("id", that_id)`.

## Success criteria

- Step 1 prints only unlearned Spanish words, sorted A→Z.
- In the dashboard's Table Editor, your chosen word now has `learned` checked, and the deleted id is gone.
- The final printed count matches what the Table Editor shows.
