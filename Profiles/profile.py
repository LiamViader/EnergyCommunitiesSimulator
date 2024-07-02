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
                 loadFactors: List[BaseFactor]=[]):
        
        self.loadFactors=loadFactors
        self.solarIrradiation=solarIrradiation
        self.overflow= pd.Series([])#guarda l'overflow de les darreres simulacions (carregues que passaven al seguents dies del que s'estava simulant)

    def simulate(self,profileConfig: ProfileConfig): #simula la energia consumida al llarg del temps en intervals de la granularitat seleccionada. en kwh
        df=pd.DataFrame()
        timeSeries=profileConfig.get_time_series()
        df["TimeStamp"] = timeSeries.index
        for factor in self.loadFactors:
            name=factor.get_name()
            if isinstance(factor,SolarPV):
                load, overflow=factor.simulate(profileConfig=profileConfig,solarIrradiation=self.solarIrradiation)
            else:
                load, overflow=factor.simulate(profileConfig=profileConfig)
            df[name]=load
            if overflow is not None:
                self.overflow=self.overflow.add(overflow,fill_value=0)
        df.to_excel("DataOutputs/PROVA.xlsx")
        self.overflow.to_excel("DataOutputs/PROVA2.xlsx")

