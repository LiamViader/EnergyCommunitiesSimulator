import pandas as pd
import numpy as np
from typing import List
from Profiles.profileConfiguration import ProfileConfig
from Profiles.Factors.baseFactor import BaseFactor
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.Factors.SolarPanel.solarPV import SolarPV
from utils.enums import FactorType

class Profile:
    def __init__(self, 
                 solarIrradiation:SolarIrradiation,
                 powerFactors: List[BaseFactor]=[]):
        
        self.powerFactors=powerFactors
        self.solarIrradiation=solarIrradiation

    def simulate(self,profileConfig: ProfileConfig, iters:int=100): #simula la potencia consumida/produida al llarg del temps
        df=pd.DataFrame()
        timeSeries=profileConfig.get_time_series()
        df["TimeStamp"] = timeSeries.index
        for factor in self.powerFactors:
            name=factor.get_name()
            if isinstance(factor,SolarPV):
                df[name]=factor.simulate(profileConfig=profileConfig,solarIrradiation=self.solarIrradiation)
            else:
                df[name]=factor.simulate(profileConfig=profileConfig)
        df.to_excel("DataOutputs/PROVA.xlsx")

