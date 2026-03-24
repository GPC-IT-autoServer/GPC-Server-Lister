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

def listServers():
    return sheet.sheet1.get_all_records()

def updateServer(row,dados,page):
    page = sheet.sheet1
    headers = page.row_values(1)
    for col, new_value in dados.items():
        if isinstance(new_value,bool):
            new_value = int(new_value)

        target_col_idx = headers.index(col) + 1

        page.update_cell(row, target_col_idx, new_value)
            
    return {"status": 200}

def listarServidor(ID,page):
    page = sheet.sheet1
    headers = page.row_values(1)
    col_id = headers.index('id') + 1

    found = page.find(str(ID), in_column=col_id)
    return found.row

def addServer(ID,dados,page):
    page = sheet.sheet1
    headers = page.row_values(1)
    new_row = [""] * len(headers)
    idx_id = headers.index("id")

    new_row[idx_id] = ID

    for col, val in dados.items():
        if col in headers:
            idx_coluna = headers.index(col)
            new_row[idx_coluna] = val

    page.append_row(new_row)
    return{"status":201}
