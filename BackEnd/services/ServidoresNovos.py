import pandas as pd
import Cache as cache
from fastapi import Depends
from schemas import DadosServerListar, DadosServerCriar, DadosServerAtualizar

#Cache class
Cache = cache.Cache()

#GET
async def listarServidores(server: DadosServerListar = Depends()):
    dadosCache = pd.DataFrame(Cache.getCache())
    filtros = {
        "modelo": server.modelo,
        "marca": server.marca,
        "gen": server.gen,
        "variante": server.variante, 
        "qtd": server.qtd,
        "bays": server.bays,
        "bay_size": server.bay_size,
        "extra_bays": server.extra_bays,
        "rails": server.rails,
        "bezel": server.bezel,
        "notas": server.notas
    }

    filtros_ativos = {coluna: valor for coluna, valor in filtros.items() if valor is not None}

    for coluna, valor in filtros_ativos.items():
        if isinstance(valor, str):
            dadosCache = dadosCache[dadosCache[coluna].astype(str).str.contains(valor, case=False, na=False)]
        else:
            dadosCache = dadosCache[dadosCache[coluna] == valor]


    if server.qtd is not None: dadosCache = dadosCache[dadosCache['qtd'] == server.qtd]
    else:
        if server.qtd_min is not None: dadosCache = dadosCache[dadosCache['qtd'] >= server.qtd_min]
        if server.qtd_max is not None: dadosCache = dadosCache[dadosCache['qtd'] <= server.qtd_max]

    if server.bays is not None: dadosCache = dadosCache[dadosCache['bays'] == server.bays]
    else:
        if server.bays_min is not None: dadosCache = dadosCache[dadosCache['bays'] >= server.bays_min]
        if server.bays_max is not None: dadosCache = dadosCache[dadosCache['bays'] <= server.bays_max]

    return {
        "status": 200,
        "total_encontrado": len(dadosCache), 
        "servidores": dadosCache.to_dict(orient="records"),
    }

#PUT
#async def AtualizarServidor(ID):

#POST
#async def AdicionarServidor():

#DELETE
#async def DeletarServidores():

#POST
async def updateCacheSheets():
    Cache.updateCache()
    return {"status": 200}