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
async def updateServer(serverID: int, server: DadosServerAtualizar):
    dados = server.model_dump(exclude_none=True)

    if not dados:
        return {"status": 200, "message": "Pedido vazio"}

    server = database.getServerByID(serverID)
    if not server:
        raise HTTPException(status_code=404, detail="Servidor não encontrado")

    dados_update = {}
    for chave, valor_novo in dados.items():
        valor_limpo = valor_novo.value if hasattr(valor_novo, "value") else valor_novo
        
        if server.get(chave) != valor_limpo:
            dados_update[chave] = valor_limpo

    if not dados_update:
        return {"status": 200, "message": "Pedido vazio e/ou sem alterações."}

    sucesso = database.postServer(serverID, dados_update)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Erro ao atualizar servidor")
    
    return {"status": 200, "message": "Servidor atualizado com sucesso", "atualizados": dados_update}
     


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
