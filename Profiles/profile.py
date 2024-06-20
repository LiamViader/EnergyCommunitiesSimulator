import pandas as pd
import numpy as np
from typing import List
from Profiles.loadConfiguration import LoadConfig
from Profiles.loadFactor import LoadFactor

class Profile:
    def __init__(self, 
                 loadConsumers: List[LoadFactor]=[],
                 loadProducers: List[LoadFactor]=[]):
        
        self.loadConsumers=loadConsumers
        self.loadProducers=loadProducers

    def generate_loads(self,loadConfig: LoadConfig, iters:int=100):
        df=pd.DataFrame()
        timeSeries=loadConfig.get_time_series()
        df["Time"] = timeSeries.index
        for loadConsumer in self.loadConsumers:
            name=loadConsumer.get_name()
            df[name]=loadConsumer.generate_load(loadConfig=loadConfig,iters=iters)
        df.to_excel("DataOutputs/PROVA.xlsx")

