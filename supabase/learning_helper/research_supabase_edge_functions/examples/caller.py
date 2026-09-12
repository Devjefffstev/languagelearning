"""Call the deployed `greet` function — reads from the `words` table."""
import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

result = supabase.functions.invoke("greet", {"body": {"word": "hola"}})
print(result.decode())
# Found:    {"found":true,"word":"hola","translation":"hello","language":"spanish"}
# Not found: {"found":false,"word":"xyz"}