"""Call the deployed `lookup_by_id` function — reads a `words` row by its id."""
import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# Pass any id from your `words` table (check with the Table Editor).
result = supabase.functions.invoke("lookup_by_id", {"body": {"id": 1}})
print(result.decode())
# Found:     {"found":true,"id":1,"word":"hola","translation":"hello","language":"spanish","learned":false}
# Not found: {"found":false,"id":999}