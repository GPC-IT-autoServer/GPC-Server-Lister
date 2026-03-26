from pydantic import BaseModel, Field, model_validator
from datetime import datetime

class DadosServerBase(BaseModel):
    modelo: str
    marca: str
    gen: str | None = None        
    variante: str | None = None
    qtd: int
    bays: int
    bay_size: float 
    extra_bays: str | None = None
    rails : bool = False
    bezel: bool = False
    notas: str | None = None


class DadosServerListar(DadosServerBase):
    modelo: str    | None = None
    marca: str     | None = None
    gen: str       | None = None
    variante: str  | None = None
    qtd: int       | None = None
    qtd_min: int          = 0
    qtd_max: int          = 999
    bays: int      | None = None
    bays_min: int         = 0
    bays_max: int         = 999
    bay_size: float| None = None
    extra_bays: str| None = None
    rails : bool   | None = None
    bezel: bool    | None = None
    notas: str     | None = None


class DadosServerCriar(DadosServerBase):
    qtd: int        = Field(1, gt=0)
    bays: int       = Field(4, gt=3)
    bay_size: float = Field(2.5, gt=2.4)


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
                    
        dif = ['qtd','bays','bay_size'] - dados.keys()
        if dif:
            for v in dif:
                fail.append(v)

        for campo in ['gen', 'variante', 'extra_bays', 'notas']:
            valor = dados.get(campo)
            if isinstance(valor, str) and valor == "string":
                dados[campo] = ""

        for campo in ['bezel','rails']:
            valor = dados.get(campo)
            if not isinstance(valor,bool):
                dados[campo] = False

        if fail:        
            raise ValueError(f"por favor, preencha o(s) campo(s) '{fail}'")
        
        return dados

class DadosServerAtualizar(DadosServerBase):
    modelo: str    | None = None
    marca: str     | None = None
    gen: str       | None = None
    variante: str  | None = None
    qtd: int       | None = None
    bays: int      | None = None
    bay_size: float| None = None
    extra_bays: str| None = None
    rails : bool   | None = None
    bezel: bool    | None = None
    notas: str     | None = None


# Schema para respostas do banco de dados (inclui ID e timestamps)
class DadosServerDB(DadosServerBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True  # Permite construir a partir de objetos do SQLAlchemy/ORM