from fastapi import APIRouter
import services.ServidoresNovos as serv

router = APIRouter()




                  # ROTAS #      
        #============================#


#--POST--

#Webhook - atualização na planilha
#Atualiza o cache do servidor
router.add_api_route("/webhook/atualizar-cache", serv.updateCacheSheets, methods=["POST"])

#Adiciona novo servidor
router.add_api_route("/novo",serv.addServer, methods=["POST"])


#--GET--

#Retorna a lista de servidores
router.add_api_route("/lista", serv.listServers, methods=["GET"])


#--DELETE--

#router.add_api_route("/remove",?, methods=["DELETE"])


#--PUT--


#Atualiza um servidor com base no ID fornecido
router.add_api_route("/atualizar/{serverID}",serv.updateServer, methods=["PUT"])