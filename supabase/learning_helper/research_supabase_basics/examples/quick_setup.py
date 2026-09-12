"""
Quick setup — your first Supabase round trip from Python.

Before running (one-time setup, from the guide root):
  1. Run examples/setup_quick.sql in the Supabase dashboard SQL Editor.
  2. Get your Project URL and publishable key from the Connect button
     (or Project Settings -> API Keys) in the dashboard. The legacy
     "anon" key (a long eyJ... JWT) works too.
  3. Create your .env file at the guide root (the folder containing
     examples/ and exercises/):
       cp .env.example .env
     then open .env and paste your URL and publishable key.
  4. Create a virtual environment and install the dependencies
     (macOS Homebrew Python blocks system-wide pip installs):
       python3 -m venv .venv
       source .venv/bin/activate
       pip install supabase python-dotenv

Run (from the guide root, .venv active):
  python3 examples/quick_setup.py
"""

import os

from dotenv import load_dotenv
from supabase import create_client

# Read SUPABASE_URL / SUPABASE_KEY from the .env file instead of `export`.
# The .env lives at the guide root; load_dotenv() searches upwards from
# this script's folder and finds it.
load_dotenv()

# create_client talks to your project's auto-generated REST API.
# The publishable key identifies "anonymous visitors" (it maps to the
# Postgres "anon" role); the table's grants and Row Level Security
# policies (created by setup_quick.sql) decide what those visitors
# are allowed to do.
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# ---- 1. Write: insert two rows in one call -------------------------------
new_words = [
    {"word": "hola", "translation": "hello", "language": "spanish"},
    {"word": "gracias", "translation": "thank you", "language": "spanish"},
]
result = supabase.table("words").insert(new_words).execute()
print(f"Inserted {len(result.data)} row(s).")

# ---- 2. Read: fetch every column of every row ----------------------------
rows = supabase.table("words").select("*").execute().data
print(f"\nAll words in the table ({len(rows)} total):")
for row in rows:
    print(f"  {row['word']} = {row['translation']} [{row['language']}]")

print("\nDone! Open the dashboard -> Table Editor -> words to see them in the UI.")
