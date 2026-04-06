from fastapi.params import Query
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from enum import Enum

class SizeEnum(str, Enum):
    small = "SFF"
    large = "LFF"


class DadosServerBase(BaseModel):
    modelo: str = Field(..., description="Modelo (ex: R640)")
    marca: str = Field(..., description="Marca (ex: Dell)")
    gen: str | None = Field(default=None, description="Geração (ex: Gen10)")
    variante: str = Field(..., description="Variante (ex: xd)")
    qtd: int = Field(..., description="Quantidade de baias")
    baias_sas_sata: int | None = Field(default=None, description="Número de baias SAS/SATA")
    baias_nvme: int | None = Field(default=None, description="Número de baias NVMe")
    tamanho_baias_sas_sata: SizeEnum | None = Field(default=None, description="Tamanho das baias SAS/SATA")
    tamanho_baias_traseiras_sas_sata: SizeEnum | None = Field(default=None, description="Tamanho das baias traseiras SAS/SATA")
    baias_traseiras_sas_sata: int | None = Field(default=None, description="Número de baias traseiras SAS/SATA")
    baias_traseiras_nvme: int | None = Field(default=None, description="Número de baias traseiras NVMe")
    trilhos: bool = False
    bezel: bool = False
    notas: str | None = Field(default=None, description="Notas adicionais, como avarias")


class DadosServerListar(DadosServerBase):
    modelo: str                 | None = None
    marca: str                  | None = None
    gen: str                    | None = None
    variante: str               | None = None
    qtd: int                    | None = None
    qtd_min: int                       = 0
    qtd_max: int                       = 999
    baias_sas_sata: int         | None = None
    baias_nvme : int            | None = None
    baias_sas_sata_min: int            = 0
    baias_sas_sata_max: int            = 999
    baias_nvme_min: int                = 0
    baias_nvme_max: int                = 999
    incluir_traseiras: bool            = True
    tamanho_baias_sas_sata: SizeEnum | None = None
    tamanho_baias_traseiras_sas_sata: SizeEnum | None = None
    baias_traseiras_sas_sata:int| None = None
    baias_traseiras_nvme: int   | None = None
    trilhos : bool              | None = None
    bezel: bool                 | None = None
    notas: str                  | None = None


class DadosServerCriar(DadosServerBase):
    qtd: int = Field(1, gt=0)
    baias: int = Field(4, gt=3)
    tamanho_baias: SizeEnum = Field(default=SizeEnum.small, description="Tamanho das baias, SFF se vazio")

    @model_validator(mode='before')
    @classmethod
    def createFilter(cls, dados: dict):
        fail = []
        if not isinstance(dados, dict):
            return dados
        
        for campo in ['marca', 'modelo']:
            valor = dados.get(campo)
            if isinstance(valor, str):
                if valor.strip() == "string" or valor.strip() == "":
                    fail.append(campo)
                    
        dif = {"qtd", "baias", "tamanho_baias"} - dados.keys()
        if dif:
            for v in dif:
                fail.append(v)

        for campo in ['gen', 'variante', 'baias_traseiras','baias_traseiras_nvme', 'notas']:
            valor = dados.get(campo)
            if isinstance(valor, str) and valor == "string":
                dados[campo] = ""

        for campo in ['bezel','trilhos']:
            valor = dados.get(campo)
            if not isinstance(valor, bool):
                dados[campo] = False

        if fail:        
            raise ValueError(f"por favor, preencha o(s) campo(s) '{fail}'")
        
        return dados


class DadosServerAtualizar(DadosServerBase):
    gen: str | None = None
    variante: str | None = None
    qtd: int | None = None
    tamanho_baias: SizeEnum | None = None
    baias_traseiras: int | None = None
    trilhos: bool | None = None
    bezel: bool | None = None
    notas: str | None = None

    @model_validator(mode='before')
    @classmethod
    def createFilter(cls, dados: dict):
        if not isinstance(dados, dict):
            return dados
        
        for campo in ['gen', 'variante', 'baias_traseiras','baias_traseiras_nvme','notas']:
            valor = dados.get(campo)
            if isinstance(valor, str) and valor == "string":
                dados[campo] = ""

        for campo in ['bezel','trilhos']:
            valor = dados.get(campo)
            if not isinstance(valor, bool):
                dados[campo] = False

        return dados

# Schema para respostas do banco de dados (inclui ID e timestamps)
class DadosServerDB(DadosServerBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True  # Permite construir a partir de objetos do SQLAlchemy/ORM