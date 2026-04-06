from fastapi import Depends, HTTPException
from schemas import DadosServerListar, DadosServerCriar, DadosServerAtualizar
import database


#--GET--
#Retorna todos os servidores que se encaixam nos filtros fornecidos
async def listServers(server: DadosServerListar = Depends()):

    filtros = server.model_dump(exclude_none=True)

    resultados = database.getServerWithFilter(filtros)

    return {
        "status": 200,  
        "total_encontrado": len(resultados), 
        "servidores": resultados,
    }

#--PUT--
#Atualiza uma linha
async def updateServer(serverID : int,server: DadosServerAtualizar):
    dados = server.model_dump(exclude_none=True)
    sucesso = database.postServer(serverID, dados)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Erro ao atualizar servidor")
    
    return{"status": 200}
     


#--POST--

#Adiciona uma nova linha
async def addServer(server: DadosServerCriar):

    dados = server.model_dump(exclude_none=True)

    sucesso = database.createServer(dados)

    if not sucesso:
        raise HTTPException(status_code=500, detail="Erro ao adicionar servidor")
    
    return{"status": 200,
    "message": "Servidor adicionado com sucesso"}
    

    
    

#--DELETE--
async def deleteServer(server_id: int):
    sucesso = database.deleteServer(server_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Servidor não encontrado")
    return {"status": 200, 
            "message": "Servidor deletado com sucesso"}
