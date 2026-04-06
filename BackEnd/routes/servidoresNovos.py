from fastapi import APIRouter
import services.ServidoresNovos as serv

router = APIRouter()




                  # ROTAS #      
        #============================#


#--POST--

#Adiciona novo servidor
router.add_api_route("/servidor",serv.addServer, methods=["POST"])


#--GET--

#Retorna a lista de servidores
router.add_api_route("/servidores", serv.listServers, methods=["GET"])


#--DELETE--

#Deleta um servidor por ID
router.add_api_route("/servidor/{serverID}", serv.deleteServer, methods=["DELETE"])


#--PUT--


#Atualiza um servidor com base no ID fornecido
router.add_api_route("/servidor/{serverID}",serv.updateServer, methods=["PUT"])