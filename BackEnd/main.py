from typing import Optional

from fastapi import FastAPI
import uvicorn
import sheets 
from fastapi.responses import FileResponse
from pathlib import Path
import pandas as pd

app = FastAPI()

PATH = Path(__file__).resolve().parent

HTML_RESPONSE = PATH / 'Response' / 'index.html'




            #================#
            #     ROTAS      #
            #================#
@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse(path=HTML_RESPONSE)


@app.get("/lista")
async def listar_servidores(
    modelo: Optional[str] = None,
    marca: Optional[str] = None,
    gen: Optional[str] = None,   #String, pois temos alguns casos como V1 ou V2
    variante: Optional[str] = None,
    qtd: Optional[int] = None,
    qtd_min: Optional[int] = 0,
    qtd_max: Optional[int] = 999,
    bays: Optional[int] = None,
    bays_min: Optional[int] = 0,
    bays_max: Optional[int] = 999,
    bay_size: Optional[float] = None,
    extra_bays: Optional[str] = None,
    rails : Optional[bool] = None,
    bezel: Optional[bool] = None,
    notas: Optional[str] = None,
):
    dadosRaw = pd.DataFrame(sheets.ListarServidores())

    dadosCache = dadosRaw
    filtros = {
        "modelo": modelo,
        "marca": marca,
        "gen": gen,
        "variante": variante, 
        "qtd": qtd,
        "bays": bays,
        "bay_size": bay_size,
        "extra_bays": extra_bays,
        "rails": rails,
        "bezel": bezel,
        "notas": notas
    }

    filtros_ativos = {coluna: valor for coluna, valor in filtros.items() if valor is not None}

    for coluna, valor in filtros_ativos.items():
        if isinstance(valor, str):
            dadosCache = dadosCache[dadosCache[coluna].astype(str).str.contains(valor, case=False, na=False)]
        else:
            dadosCache = dadosCache[dadosCache[coluna] == valor]


    if qtd is not None: dadosCache = dadosCache[dadosCache['qtd'] == qtd]
    else:
        if qtd_min is not None: dadosCache = dadosCache[dadosCache['qtd'] >= qtd_min]
        if qtd_max is not None: dadosCache = dadosCache[dadosCache['qtd'] <= qtd_max]

    if bays is not None: dadosCache = dadosCache[dadosCache['bays'] == bays]
    else:
        if bays_min is not None: dadosCache = dadosCache[dadosCache['bays'] >= bays_min]
        if bays_max is not None: dadosCache = dadosCache[dadosCache['bays'] <= bays_max]

    return {
        "total_encontrado": len(dadosCache), 
        "servidores": dadosCache.to_dict(orient="records")
    }


if __name__ == "__main__":
    uvicorn.run(app,port=8000)