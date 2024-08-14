import pandas as pd
import numpy as np
from typing import List, Tuple, Optional
from Profiles.profileConfiguration import ProfileConfig
from Profiles.Factors.baseFactor import BaseFactor
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.Factors.SolarPanel.solarPV import SolarPV
from Profiles.Battery.batteriesManager import BatteriesManager
from utils.enums import Granularity
from utils.enums import FactorType
from EnergyPrice.EnergyPlans.baseEnergyPlan import BaseEnergyPlan

class Profile:
    def __init__(self, 
                name:str,
                exteriorContactArea:float=50,
                insideVolume:float=150,
                energyPlan: Optional[BaseEnergyPlan]=None,
                loadFactors: List[BaseFactor]=[],
                batteries: BatteriesManager=None):

        self.name=name
        self.energyPlan=energyPlan
        self.exteriorContactArea=exteriorContactArea
        self.insideVolume=insideVolume
        self.loadFactors=loadFactors
        self.batteries=batteries
        self.detailedLoad={}
        self.configLastSimulation=None

    def simulate(self,profileConfig: ProfileConfig): #simula la energia consumida al llarg del temps en intervals de la granularitat seleccionada. en kwh
        self.detailedLoad={}
        self.configLastSimulation=profileConfig

        profileConfig.set_properties(
            exteriorContactArea=self.exteriorContactArea,
            insideVolume=self.insideVolume
        )

        for factor in self.loadFactors:
            name=factor.get_name()
            load=factor.simulate(profileConfig=profileConfig)
            
            if name in self.detailedLoad:
                self.detailedLoad[name].append((load, factor.get_factor_type()))
            else:
                self.detailedLoad[name] = [(load, factor.get_factor_type())]

        
        if self.batteries is not None:
            batteriesLoad=self.batteries.use_on(self.get_combined_load(),profileConfig)
            name="Batteries"
            if name in self.detailedLoad:
                self.detailedLoad[name].append((batteriesLoad, FactorType.Battery))
            else:
                self.detailedLoad[name] = [(batteriesLoad, FactorType.Battery)]


    def get_detailed_load(self):
        return self.detailedLoad
    
    def get_detailed_load_df(self)->pd.DataFrame:
        df_detailed=pd.DataFrame()
        timeSeries=self.configLastSimulation.get_time_series()
        df_detailed["TimeStamp"] = timeSeries.index
        for name, loads in self.detailedLoad.items():
            for index, (load, factor_type) in enumerate(loads):
                serie = pd.Series(load)
                df_detailed[f"{name}_{index}"] = serie


        return df_detailed

    def get_combined_load(self)->np.ndarray:
        if self.configLastSimulation is not None:
            combinedLoad=np.zeros(self.configLastSimulation.num_indices())
            for name, loads in self.detailedLoad.items():
                for load, factor_type in loads:
                    if factor_type==FactorType.Consumer or factor_type==FactorType.Prosumer or factor_type==FactorType.Battery:
                        combinedLoad+=load
                    elif factor_type==FactorType.Producer:
                        combinedLoad-=load
            return combinedLoad
        else: raise ValueError("theres no simulated load")

    def get_name(self)->str:
        return self.name

    def get_load_pv(self)->Tuple[np.ndarray,np.ndarray]:
        if self.configLastSimulation is not None:
            finalLoad=np.zeros(self.configLastSimulation.num_indices())
            finalPv=np.zeros(self.configLastSimulation.num_indices())
            for name, loads in self.detailedLoad.items():
                for load, factor_type in loads:
                    if factor_type==FactorType.Consumer:
                        finalLoad+=load
                    elif factor_type==FactorType.Producer:
                        finalPv+=load
                    elif factor_type==FactorType.Prosumer:
                        for i in range(self.configLastSimulation.num_indices()):
                            if load[i]>0:
                                finalLoad[i]+=load[i]
                            else:
                                finalPv[i]+=abs(load[i])
                    elif factor_type==FactorType.Battery:
                        for i in range(self.configLastSimulation.num_indices()):
                            if load[i]<0:
                                finalLoad[i]+=load[i]
                            else:
                                finalPv[i]-=load[i]

            return finalLoad,finalPv
        else: raise ValueError("theres no simulated load")
    
    def get_combined_load_pv(self)->Tuple[np.ndarray,np.ndarray]:
        if self.configLastSimulation is not None:
            combinedLoad=np.zeros(self.configLastSimulation.num_indices())
            combinedPv=np.zeros(self.configLastSimulation.num_indices())
            for name, loads in self.detailedLoad.items():
                for load, factor_type in loads:
                    if factor_type==FactorType.Consumer or factor_type==FactorType.Prosumer or factor_type==FactorType.Battery:
                        combinedLoad+=load
                    elif factor_type==FactorType.Producer:
                        combinedLoad-=load
            for i in range(self.configLastSimulation.num_indices()):
                if combinedLoad[i]<0:
                    combinedPv[i]=abs(combinedLoad[i])
                    combinedLoad[i]=0
            return combinedLoad, combinedPv
        else: raise ValueError("theres no simulated load")

    def get_energy_plan(self)->BaseEnergyPlan:
        return self.energyPlan