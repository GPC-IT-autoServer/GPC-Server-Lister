from fastapi import APIRouter
from typing import Optional
import services.ServidoresNovos as serv

router = APIRouter()




                  # ROTAS #      
        #============================#


router.add_api_route("/lista", serv.listarServidores, methods=["GET"])

#@router.post("/add")

#@router.delete("/remove/{id}")

#@router.put("/update")