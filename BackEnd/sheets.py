import gspread
from pathlib import Path
from google.oauth2.service_account import Credentials

DIRETORIO_ATUAL = Path(__file__).resolve().parent


AUTH_PATH = DIRETORIO_ATUAL / 'AUTH' / 'AUTH.json'

scopes = ['https://www.googleapis.com/auth/drive']

creds = Credentials.from_service_account_file(str(AUTH_PATH), scopes = scopes)

client = gspread.authorize(creds)

sheetID = "1m-QxfHDEthX1-wS7l15ilTp2Ah1m2Sn4UyOXp4AI3u8"

sheet = client.open_by_key(sheetID)

def ListarServidores():
    return sheet.sheet1.get_all_records()