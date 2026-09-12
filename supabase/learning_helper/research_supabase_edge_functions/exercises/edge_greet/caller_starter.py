"""
Exercise 05 — Call the `greet` Edge Function from Python.

Prereqs: `supabase functions deploy greet` succeeded; the
SUPABASE_SERVICE_ROLE_KEY secret is set on the project.
"""

import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# TODO 1: Invoke the `greet` function with {"word": "hola"} and print the dict.
# Hint: supabase.functions.invoke("greet", {"body": {...}}).data