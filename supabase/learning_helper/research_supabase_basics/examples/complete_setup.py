"""
Complete setup — a realistic tour of what you can do with supabase-py.

Before running:
  1. Run examples/setup_complete.sql in the Supabase dashboard SQL Editor.
  2. Same .env and .venv as quick_setup.py (at the guide root):
       cp .env.example .env        # paste your Project URL + publishable key
       source .venv/bin/activate   # if not already active

Run (from the guide root, .venv active):
  python3 examples/complete_setup.py

Thanks to upsert, this whole script is safe to re-run: no duplicate rows.

Note: in one insert/upsert call, give EVERY dict the same keys — PostgREST
fills missing keys with null, and null skips column defaults.
"""

import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()  # reads SUPABASE_URL / SUPABASE_KEY from the .env file
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# ---- 1. Seed vocabulary with upsert (insert-or-update) --------------------
# "word" is a unique column, so if a row with the same word already exists,
# upsert updates it instead of raising a duplicate-key error.
supabase.table("words").upsert(
    [
        {"word": "hola", "translation": "hello", "language": "spanish",
         "example_sentence": "Hola, ¿cómo estás?"},
        {"word": "gracias", "translation": "thank you", "language": "spanish",
         "example_sentence": "Gracias por todo."},
        {"word": "gato", "translation": "cat", "language": "spanish",
         "example_sentence": "El gato duerme."},
        {"word": "bonjour", "translation": "hello", "language": "french",
         "example_sentence": "Bonjour, ça va ?"},
        {"word": "chien", "translation": "dog", "language": "french",
         "example_sentence": "Le chien court."},
    ],
    on_conflict="word",
).execute()
print("1) Seeded vocabulary with upsert (re-runnable, no duplicates).")

# ---- 2. Upsert a single row ------------------------------------------------
supabase.table("words").upsert(
    {"word": "hola", "translation": "hello", "language": "spanish",
     "example_sentence": "¡Hola! Me llamo Ana."},
    on_conflict="word",
).execute()
print("2) Updated 'hola' with a better example sentence.")

# ---- 3. Select with filter + order + limit ---------------------------------
# Equivalent SQL: select word, translation, learned from words
#                 where language = 'spanish' and learned = false
#                 order by word limit 5;
todo = (
    supabase.table("words")
    .select("word, translation, learned")
    .eq("language", "spanish")
    .eq("learned", False)
    .order("word")
    .limit(5)
    .execute()
    .data
)
print(f"3) Spanish words still to learn ({len(todo)}):")
for row in todo:
    print(f"   {row['word']} = {row['translation']}")

# ---- 4. Exact row count without downloading every row ----------------------
res = supabase.table("words").select("*", count="exact").execute()
print(f"4) Total rows in the table: {res.count}")

# ---- 5. Update the rows that match a filter --------------------------------
# Golden rule: always pair update() with a filter, or you update every row.
supabase.table("words").update({"learned": True}).eq("word", "gracias").execute()
print("5) Marked 'gracias' as learned.")

# ---- 6. Delete the rows that match a filter --------------------------------
# Same rule: never call delete() without a filter.
supabase.table("words").delete().eq("word", "gato").execute()
print("6) Deleted 'gato'.")

# ---- 7. Call a Postgres function defined in your database ------------------
# word_stats() was created by setup_complete.sql. Postgres does the
# aggregation; Python just receives the finished result.
stats = supabase.rpc("word_stats").execute().data
print("7) Stats per language (computed inside Postgres):")
for s in stats:
    print(f"   {s['language']}: {s['total']} words, {s['learned_count']} learned")

print("\nDone! Re-run me any time — the upsert seeding keeps things clean.")
