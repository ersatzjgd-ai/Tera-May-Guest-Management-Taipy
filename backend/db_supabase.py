import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables (Ensure .env is in your .gitignore file)
load_dotenv()

# Retrieve credentials securely from the environment
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials not found. Please ensure your .env file or Secrets Manager is configured.")

# Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------------------------------------------------
# DATABASE OPERATIONS
# ---------------------------------------------------------

def fetch_all_guests():
    """
    Fetches the full guest roster from the 'guests' table.
    Returns a pandas DataFrame for seamless integration with Taipy's table UI.
    """
    try:
        # Querying the exact 'guests' table from the schema
        response = supabase.table("guests").select("*").execute()
        
        # Convert the dictionary response directly to a DataFrame for Taipy
        if response.data:
            return pd.DataFrame(response.data)
        return pd.DataFrame()
        
    except Exception as e:
        print(f"Error fetching guest data: {e}")
        return pd.DataFrame() # Return empty DataFrame to prevent UI crashes

def import_guests_from_csv(file_path):
    """
    Handles bulk ingestion of guests via .CSV format.
    Maps data directly to the 'guests' table schema.
    """
    try:
        # Fast read of the CSV file
        df = pd.read_csv(file_path)
        
        # Clean up NaN values to None (which translates to Null in PostgreSQL)
        # This prevents insertion errors for optional schema columns
        df = df.where(pd.notna(df), None)
        
        # Convert DataFrame to a list of dictionaries for Supabase insertion
        records = df.to_dict(orient="records")
        
        # Insert records into the 'guests' table
        response = supabase.table("guests").insert(records).execute()
        return True, len(response.data)
        
    except Exception as e:
        print(f"CSV Import Error: {e}")
        return False, str(e)

def fetch_all_gres():
    """
    Fetches the list of Guest Relations Executives from the 'gres' table.
    Used to populate dropdowns when assigning a GRE to a guest.
    """
    try:
        response = supabase.table("gres").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error fetching GRE list: {e}")
        return []

def assign_gre_to_guest(guest_id, gre_id, gre_name):
    """
    Assigns a GRE to a specific guest.
    Updates both the integer ID and the text name per the schema requirements.
    """
    try:
        response = supabase.table("guests").update({
            "assigned_gre_id": gre_id,
            "assigned_gre": gre_name
        }).eq("id", guest_id).execute()
        return True
    except Exception as e:
        print(f"Error assigning GRE to guest {guest_id}: {e}")
        return False
