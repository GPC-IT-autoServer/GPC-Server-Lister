from supabase import create_client, Client
import os
from dotenv import load_dotenv
from typing import List, Dict, Any


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Credenciais não configuradas")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def getServers() -> List[Dict[str, Any]]:
    response = supabase.table("server_models").select("*").execute()
    return response.data


def getServerByID(server_id: int) -> Dict[str, Any]:
    response = supabase.table("server_models").select("*").eq("id", server_id).execute()
    if response.data:
        return response.data[0]
    return None


def getServerWithFilter(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    query = supabase.table("server_models").select("*")
    
    for key, value in filters.items():
        if value is not None:
            query = query.eq(key, value)
    
    response = query.execute()
    return response.data


def createServer(dados: Dict[str, Any]) -> bool:
    try:
        supabase.table("server_models").insert(dados).execute()
        return True
    except Exception as e:
        print(f"Erro ao adicionar servidor: {e}")
        return False


def postServer(server_id: int, dados: Dict[str, Any]) -> bool:
    try:
        dados_formatados = {}
        for col, new_value in dados.items():
            if isinstance(new_value, bool):
                dados_formatados[col] = int(new_value)
            else:
                dados_formatados[col] = new_value
        
        supabase.table("server_models").update(dados_formatados).eq("id", server_id).execute()
        return True
    except Exception as e:
        print(f"Erro ao atualizar servidor: {e}")
        return False


def deleteServer(server_id: int) -> bool:
    try:
        supabase.table("server_models").delete().eq("id", server_id).execute()
        return True
    except Exception as e:
        print(f"Erro ao deletar servidor: {e}")
        return False


def getMaxId() -> int:
    try:
        response = supabase.table("server_models").select("id").order("id", desc=True).limit(1).execute()
        if response.data:
            return response.data[0]["id"]
        return 0
    except Exception as e:
        print(f"Erro ao buscar o maior ID: {e}")
        return 0
