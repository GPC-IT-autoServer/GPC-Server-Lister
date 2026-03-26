from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL e SUPABASE_KEY não estão configurados no .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def listServers():
    """Retorna todos os servidores da tabela server_model"""
    response = supabase.table("server_models").select("*").execute()
    print(response.data)
    return response.data
