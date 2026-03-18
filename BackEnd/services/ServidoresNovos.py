import pandas as pd
import Cache as cache
import sheets
from fastapi import Depends, HTTPException
from schemas import DadosServerListar, DadosServerCriar, DadosServerAtualizar

#Cache class
Cache = cache.Cache()

#GET
async def listarServidores(server: DadosServerListar = Depends()):
    cacheClone = pd.DataFrame(Cache.getCache())
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
            cacheClone = cacheClone[cacheClone[coluna].astype(str).str.contains(valor, case=False, na=False)]
        else:
            cacheClone = cacheClone[cacheClone[coluna] == valor]


    if server.qtd is not None: cacheClone = cacheClone[cacheClone['qtd'] == server.qtd]
    else:
        if server.qtd_min is not None: cacheClone = cacheClone[cacheClone['qtd'] >= server.qtd_min]
        if server.qtd_max is not None: cacheClone = cacheClone[cacheClone['qtd'] <= server.qtd_max]

    if server.bays is not None: cacheClone = cacheClone[cacheClone['bays'] == server.bays]
    else:
        if server.bays_min is not None: cacheClone = cacheClone[cacheClone['bays'] >= server.bays_min]
        if server.bays_max is not None: cacheClone = cacheClone[cacheClone['bays'] <= server.bays_max]

    return {
        "status": 200,
        "total_encontrado": len(cacheClone), 
        "servidores": cacheClone.to_dict(orient="records"),
    }

#PUT
async def AtualizarServidor(serverID : int,server: DadosServerAtualizar):
    aba = None #placeholder

    cacheClone = pd.DataFrame(Cache.getCache())
    if not serverID or not cacheClone['id'].isin([serverID]).any():
        raise HTTPException(status_code=404, detail="Servidor não encontrado")
    
    dados = server.model_dump(exclude_unset=True)
    row = sheets.listarServidor(serverID,aba)
    sheets.atualizarServidor(row,dados,aba)

    
    return{
        "status": 200
    }
    
    

#POST
#async def AdicionarServidor():

#DELETE
#async def DeletarServidores():

#POST
async def updateCacheSheets():
    Cache.updateCache()
    return {"status": 200}