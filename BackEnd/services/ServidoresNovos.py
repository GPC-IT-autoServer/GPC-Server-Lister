from fastapi import Depends, HTTPException
from schemas import DadosServerListar, DadosServerCriar, DadosServerAtualizar
import database


#--GET--
#Retorna todos os servidores que se encaixam nos filtros fornecidos
async def listServers(server: DadosServerListar = Depends()):

    filtros = server.model_dump(exclude_none=True)

    qtd_min = filtros.pop("qtd_min", None)
    qtd_max = filtros.pop("qtd_max", None)
    
    bays_min = filtros.pop("bays_min", None)
    bays_max = filtros.pop("bays_max", None)

    resultados = database.getServerWithFilter(filtros)

    return {
        "status": 200,  
        "total_encontrado": len(resultados), 
        "servidores": resultados,
    }

#--PUT--
#Atualiza uma linha
async def updateServer(serverID : int,server: DadosServerAtualizar):

    
    return{"status": 200}
     


#--POST--

#Adiciona uma nova linha
async def addServer(server: DadosServerCriar):
    return{"status": 200}
    #updateServer(matchID,{'qtd':server['qtd']})

    
    

#--DELETE--
#async def DeletarServidores():


