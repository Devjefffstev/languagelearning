"""
Exercise 03 — Call a Postgres function from Python with .rpc().

Prereqs: run stats_function.sql (same folder) in the Supabase SQL Editor,
activate .venv at the guide root, and have your .env there (copy
.env.example and fill it in).
"""

import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()  # reads SUPABASE_URL / SUPABASE_KEY from the .env file
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# ---- TODO 1: Call the word_stats function via .rpc() ------------------------
# Print a line per language, formatted as:
#   <language>: <total> words, <learned_count> learned
# TODO: your code here

# ---- TODO 2: Get the exact total row count with a select --------------------
# Use .select("*", count="exact") and read the .count attribute.
# TODO: your code here

# ---- TODO 3: Verify -----------------------------------------------------------
# Add the totals from TODO 1 and compare with the count from TODO 2.
# Print "MATCH" or "MISMATCH".
# TODO: your code here
