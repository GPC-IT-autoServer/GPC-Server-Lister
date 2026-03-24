import pandas as pd
import Cache as cache
import sheets
from fastapi import Depends, HTTPException
from schemas import DadosServerListar, DadosServerCriar, DadosServerAtualizar

#Cache obj
Cache = cache.Cache()

#--GET--
#Retorna a planilha inteira, aplicando filtros fornecidos pelo usuário
async def listServers(server: DadosServerListar = Depends()):
    cachedSheet = pd.DataFrame(Cache.getCache())
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
            cachedSheet = cachedSheet[cachedSheet[coluna].astype(str).str.contains(valor, case=False, na=False)]
        else:
            cachedSheet = cachedSheet[cachedSheet[coluna] == valor]

    if server.qtd is not None: cachedSheet = cachedSheet[cachedSheet['qtd'] == server.qtd]
    else:
        if server.qtd_min is not None: cachedSheet = cachedSheet[cachedSheet['qtd'] >= server.qtd_min]
        if server.qtd_max is not None: cachedSheet = cachedSheet[cachedSheet['qtd'] <= server.qtd_max]

    if server.bays is not None: cachedSheet = cachedSheet[cachedSheet['bays'] == server.bays]
    else:
        if server.bays_min is not None: cachedSheet = cachedSheet[cachedSheet['bays'] >= server.bays_min]
        if server.bays_max is not None: cachedSheet = cachedSheet[cachedSheet['bays'] <= server.bays_max]

    return {
        "status": 200,
        "total_encontrado": len(cachedSheet), 
        "servidores": cachedSheet.to_dict(orient="records"),
    }

#--PUT--
#Atualiza uma linha
async def updateServer(serverID : int,server: DadosServerAtualizar):
    page = None #placeholder

    cachedSheet = pd.DataFrame(Cache.getCache())
    if not serverID or not cachedSheet['id'].isin([serverID]).any():
        raise HTTPException(status_code=404, detail="Servidor não encontrado")
    
    dados = server.model_dump(exclude_unset=True)
    row = sheets.listarServidor(serverID,page)
    dados['qtd'] += row['qtd']
    if dados['qtd'] <= 0:
        print("PLACEHOLDER: APAGAR SERVER")
    else:
        sheets.updateServer(row,dados,page)

    
    return{"status": 200}
     
#--POST--
#atualiza o cache do server com a planilha atualizada
async def updateCacheSheets():
    Cache.updateCache()
    return {"status": 200}

#Adiciona uma nova linha
async def addServer(server: DadosServerCriar):
    page=None #placeholder
    cachedSheet = pd.DataFrame(Cache.getCache())
    newID = int(cachedSheet['id'].max()) +1

    cacheComparation = cachedSheet.drop(columns = ['id'])
    cacheComparation = cacheComparation.drop(columns = ['qtd'])

    targetData = server.model_dump()

    targetValues = pd.Series(targetData).reindex(cacheComparation.columns)

    targetComparation = targetValues.drop(columns = ['qtd']).astype(str).str.lower().str.strip()

    print(targetComparation)
    print(cacheComparation)

    rowMatch = (cacheComparation.fillna('') == targetComparation.fillna('')).all(axis=1)
    print(rowMatch)

    if not rowMatch.any():
        dados = server.model_dump(exclude_unset=True)
        if not sheets.addServer(newID,dados,page):
            raise HTTPException(status_code=400, detail="Erro indefinido,confira se todos os paramêtros estão corretos")
        return{"status":201, "message": "servidor registrado com sucesso!"}
    
    matchRow = cachedSheet[rowMatch]
    matchID = matchRow['id'].iloc[0]

    updateServer(matchID,{'qtd':server['qtd']})

    
    

#--DELETE--
#async def DeletarServidores():


