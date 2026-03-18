from fastapi import APIRouter
import services.ServidoresNovos as serv

router = APIRouter()




                  # ROTAS #      
        #============================#


#Webhook - atualização na planilha
#Atualiza o cache do servidor
router.add_api_route("/webhook/atualizar-cache", serv.updateCacheSheets, methods=["POST"])

#Retorna a lista de servidores
router.add_api_route("/lista", serv.listarServidores, methods=["GET"])

#router.add_api_route("/add",?, methods=["POST"])

#router.add_api_route("/remove",?, methods=["DELETE"])

#router.add_api_route("/update",?, methods=["PUT"])