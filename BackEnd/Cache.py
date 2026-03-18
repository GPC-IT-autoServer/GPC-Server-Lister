import pandas as pd
import sheets 

class Cache:

    def __init__(self):
        self.dados = None

    def updateCache(self):
        self.dados = pd.DataFrame(sheets.listarServidores())

    def getCache(self):
        if self.dados is None: self.updateCache()
        return self.dados