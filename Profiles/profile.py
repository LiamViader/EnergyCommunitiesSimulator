import pandas as pd
import numpy as np
from typing import List
from Profiles.profileConfiguration import ProfileConfig
from Profiles.Factors.baseFactor import BaseFactor
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.Factors.SolarPanel.solarPV import SolarPV
from Profiles.Battery.batteriesManager import BatteriesManager
from utils.enums import FactorType

class Profile:
    def __init__(self, 
                 loadFactors: List[BaseFactor]=[],
                 batteries: BatteriesManager=None):

        self.loadFactors=loadFactors
        self.batteries=batteries
        self.overflow= pd.Series(dtype=float)#guarda l'overflow de les darreres simulacions (carregues que passaven al seguents dies del que s'estava simulant)

    def simulate(self,profileConfig: ProfileConfig, useOverflow:bool=True, saveOverflow:bool=True, outputRoute="DataOutputs/example"): #simula la energia consumida al llarg del temps en intervals de la granularitat seleccionada. en kwh

        df_detailed=pd.DataFrame()
        combinedLoad=pd.Series([])
        timeSeries=profileConfig.get_time_series()
        df_detailed["TimeStamp"] = timeSeries.index

        if useOverflow:
            #afegir el overflow del dia anterior 
            overflowToUse=self.overflow.head(24)
            df_detailed["overflow"]=overflowToUse
            df_detailed["overflow"] = df_detailed['overflow'].fillna(0)
            combinedLoad.add(overflowToUse,fill_value=0)
            #treure overflow usat
            self.overflow = self.overflow[24:]


        for factor in self.loadFactors:
            name=factor.get_name()
            load, overflow=factor.simulate(profileConfig=profileConfig)
            df_detailed[name]=load

            if factor.get_factor_type()==FactorType.Consumer:
                combinedLoad=combinedLoad.add(load,fill_value=0)
            elif factor.get_factor_type()==FactorType.Producer:
                combinedLoad=combinedLoad.subtract(load,fill_value=0)

            if overflow is not None and saveOverflow:
                if factor.get_factor_type()==FactorType.Consumer:
                    self.overflow=self.overflow.add(overflow,fill_value=0)
                elif factor.get_factor_type()==FactorType.Producer:
                    self.overflow=self.overflow.subtract(overflow,fill_value=0)

        
        if self.batteries is not None:
            batteriesLoad=self.batteries.use(combinedLoad,profileConfig)
            combinedLoad=combinedLoad.add(batteriesLoad,fill_value=0)
            df_detailed["Batteries"]=batteriesLoad


        df_detailed.to_excel(outputRoute+"_detailed.xlsx")


        combinedLoad.to_excel(outputRoute+"_combined.xlsx")

