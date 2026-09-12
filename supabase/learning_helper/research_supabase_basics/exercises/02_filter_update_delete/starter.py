"""
Exercise 02 — Filter, update, delete.

Prereqs: run examples/setup_complete.sql first (it adds the `learned`
column and the update/delete permissions), activate .venv at the guide
root, and have your .env there (copy .env.example and fill it in).
"""

import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()  # reads SUPABASE_URL / SUPABASE_KEY from the .env file
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# ---- TODO 1: Fetch only unlearned Spanish words, ordered alphabetically ---
# Filter with .eq(...) on language and learned, order by "word".
# Print each row as: word (translation)
# TODO: your code here

# ---- TODO 2: Mark one word as learned --------------------------------------
# Pick any word from the list above and update it with {"learned": True}.
# Target it with .eq("word", "<the word>"). Print a confirmation.
# TODO: your code here

# ---- TODO 3: Delete one row by its id ---------------------------------------
# First select a row to get its id, then delete with .eq("id", <id>).
# Print the id you removed. NEVER call delete() without a filter.
# TODO: your code here

# ---- TODO 4: Sanity check ----------------------------------------------------
# Re-fetch all rows and print the total count so you can see the result.
# TODO: your code here
