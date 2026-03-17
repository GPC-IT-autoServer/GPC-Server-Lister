import pandas as pd
import sheets 

class Cache(object):

    def __init__(self):
        self.dados 
        self.MinutesToLive = 5
        self.ttl = self.SecondsToLive * 60

    def updateCache(self):
        self.dados = pd.DataFrame(sheets.ListarServidores())

    def getCache(self):
        if not self.dados: self.updateSheet()
        return self.dados