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

def listarServidores():
    return sheet.sheet1.get_all_records()


def atualizarServidor(row,dados,aba):
    aba = sheet.sheet1
    headers = aba.row_values(1)
    for nome_coluna, novo_valor in dados.items():

        col_alvo_index = headers.index(nome_coluna) + 1

        aba.update_cell(row, col_alvo_index, novo_valor)
            
    return {"status": 200}

def listarServidor(ID,aba):
    aba = sheet.sheet1
    headers = aba.row_values(1)
    col_id = headers.index('id') + 1
    found = aba.find(str(ID), in_column=col_id)
    return found.row