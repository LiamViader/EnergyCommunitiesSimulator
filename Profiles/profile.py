import pandas as pd
import numpy as np
from typing import List
from Profiles.profileConfiguration import ProfileConfig
from Profiles.LoadFactors.loadFactor import LoadFactor
from Profiles.LoadFactors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.LoadFactors.SolarPanel.solarPV import SolarPV
from utils.enums import LoadType

class Profile:
    def __init__(self, 
                 solarIrradiation:SolarIrradiation,
                 loadFactors: List[LoadFactor]=[]):
        
        self.loadFactors=loadFactors
        self.solarIrradiation=solarIrradiation

    def generate_loads(self,profileConfig: ProfileConfig, iters:int=100):
        df=pd.DataFrame()
        timeSeries=profileConfig.get_time_series()
        df["TimeStamp"] = timeSeries.index
        for factor in self.loadFactors:
            name=factor.get_name()
            if isinstance(factor,SolarPV):
                df[name]=factor.generate_load(profileConfig=profileConfig,solarIrradiation=self.solarIrradiation)
            else:
                df[name]=factor.generate_load(profileConfig=profileConfig)
        df.to_excel("DataOutputs/PROVA.xlsx")

