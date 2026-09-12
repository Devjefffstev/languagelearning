"""
Exercise 01 — Insert and select.

Prereqs (one-time, at the guide root — see the README Quick setup):
  - python3 -m venv .venv
  - source .venv/bin/activate        # re-run in every new terminal
  - pip install supabase python-dotenv
  - cp .env.example .env             # fill in your URL + publishable key
  - Run examples/setup_quick.sql in the Supabase SQL Editor

Goal: insert at least 5 words, then read and print everything.
Fill in every TODO. Do not modify the imports.
"""

import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()  # reads SUPABASE_URL / SUPABASE_KEY from the .env file
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# ---- TODO 1: Build a list of at least 5 dicts, one per word ---------------
# Each dict must have the keys: word, translation, language
# Example style (pick your own words): {"word": "perro", "translation": "dog", "language": "spanish"}
words_to_add = [
    # TODO: add your dicts here
    # Each dict is one row; its keys (word, translation, language) must match the
    # column names defined in setup_quick.sql — that's the contract .insert()
    # uses to map Python values into SQL columns.
    {"word": "perro", "translation": "dog", "language": "spanish"},
    {"word": "gato", "translation": "cat", "language": "spanish"},
    {"word": "libro", "translation": "book", "language": "spanish"},
    {"word": "casa", "translation": "house", "language": "spanish"},
    {"word": "agua", "translation": "water", "language": "spanish"},
]

# ---- TODO 2: Insert the list into the "words" table -----------------------
# Print how many rows were inserted (the length of the result's .data).
# TODO: your code here
# result = supabase.table("words").insert(words_to_add).execute()
# print(f"Inserted {len(result.data)} rows")
# ---- TODO 3: Select every row from "words" and print it -------------------
# Format each line exactly as: word — translation [language]
# TODO: your code here
# .select("*") asks PostgREST for every column; the response payload lives on
# .data and is a list of dicts keyed by column name, so we can pull fields by key.
rows = supabase.table("words").select("*").execute()
for row in rows.data:
    print(f'{row["word"]} — {row["translation"]} [{row["language"]}]')
