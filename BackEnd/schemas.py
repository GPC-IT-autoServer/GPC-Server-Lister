from pydantic import BaseModel


#Classes
class DadosServerBase(BaseModel):
    modelo: str
    marca: str
    gen: str        #String, pois temos alguns casos como V1 ou V2
    variante: str
    qtd: int
    bays: int
    bay_size: float 
    extra_bays: str
    rails : bool
    bezel: bool
    notas: str

class DadosServerListar(DadosServerBase):
    modelo: str    | None = None
    marca: str     | None = None
    gen: str       | None = None       #String, pois temos alguns casos como V1 ou V2
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
    extra_bays: str| None = None
    rails : bool          = 0
    bezel: bool           = 0
    notas: str     | None = None
    variante: str  | None = None
    gen: str       | None = None

class DadosServerAtualizar(DadosServerBase):
    modelo: str    | None = None
    marca: str     | None = None
    gen: str       | None = None       #String, pois temos alguns casos como V1 ou V2
    variante: str  | None = None
    qtd: int       | None = None
    bays: int      | None = None
    bay_size: float| None = None
    extra_bays: str| None = None
    rails : bool   | None = None
    bezel: bool    | None = None
    notas: str     | None = None

