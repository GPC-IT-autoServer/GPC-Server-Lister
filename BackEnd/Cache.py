import pandas as pd
import sheets 

class Cache:

    def __init__(self):
        self.dados = None

    def updateCache(self):
        self.dados = pd.DataFrame(sheets.listServers())
        dados_raw = self.dados
        dados_raw['qtd'] = pd.to_numeric(dados_raw['qtd'], errors='raise').fillna(0).astype(int)
        dados_raw['bays'] = pd.to_numeric(dados_raw['bays'], errors='raise').fillna(0).astype(int)
        dados_raw['bay_size'] = pd.to_numeric(dados_raw['bay_size'], errors='raise').fillna(0.0).astype(float)

        self.dados = dados_raw.astype(str).apply(lambda x: x.str.lower())

    def getCache(self):
        if self.dados is None: self.updateCache()
        return self.dados