from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

def get_client():
    """Return Supabase client."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)
