import pandas as pd
import numpy as np
from typing import List
from Profiles.loadConfiguration import LoadConfig
from Profiles.LoadFactors.loadFactor import LoadFactor
from Profiles.LoadFactors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.LoadFactors.SolarPanel.solarPanel import SolarPanel
from utils.enums import LoadType

class Profile:
    def __init__(self, 
                 solarIrradiation:SolarIrradiation,
                 loadFactors: List[LoadFactor]=[]):
        
        self.loadFactors=loadFactors
        self.solarIrradiation=solarIrradiation

    def generate_loads(self,loadConfig: LoadConfig, iters:int=100):
        df=pd.DataFrame()
        timeSeries=loadConfig.get_time_series()
        df["TimeStamp"] = timeSeries.index
        for factor in self.loadFactors:
            name=factor.get_name()
            if isinstance(factor,SolarPanel):
                df[name]=factor.generate_load(loadConfig=loadConfig,solarIrradiation=self.solarIrradiation)
            else:
                df[name]=factor.generate_load(loadConfig=loadConfig,iters=iters)
        df.to_excel("DataOutputs/PROVA.xlsx")

