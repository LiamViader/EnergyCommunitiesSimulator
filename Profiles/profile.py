import pandas as pd
import numpy as np
from typing import List, Tuple, Optional, Dict
from Profiles.Factors.baseFactor import BaseFactor
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.Factors.SolarPanel.solarPV import SolarPV
from Profiles.Battery.batteriesManager import BatteriesManager
from utils.enums import Granularity
from utils.enums import FactorType
from EnergyPrice.EnergyPlans.baseEnergyPlan import BaseEnergyPlan
from Simulation.simulationConfiguration import SimulationConfig

class Profile:
    _idCounter=0

    def __init__(self, 
                name:str,
                energyPlan: BaseEnergyPlan,
                exteriorContactArea:float=50,
                insideVolume:float=150,
                loadFactors: List[BaseFactor]=[],
                batteries: BatteriesManager=None):

        Profile._idCounter+=1
        self.id=Profile._idCounter
        self.name=name
        self.energyPlan=energyPlan
        self.exteriorContactArea=exteriorContactArea
        self.insideVolume=insideVolume
        self.loadFactors=loadFactors
        self.batteries=batteries
        self.detailedLoad:Dict[BaseFactor,np.ndarray]={}
        self.configLastSimulation=None

    def simulate(self,simulationConfig: SimulationConfig): #simula la energia consumida al llarg del temps en intervals de la granularitat seleccionada. en kwh
        self.detailedLoad:Dict[BaseFactor,np.ndarray]={}
        self.configLastSimulation=simulationConfig

        for factor in self.loadFactors:
            load=factor.simulate(simulationConfig=simulationConfig)
            self.detailedLoad[factor]=load
            
        if self.batteries is not None:
            batteriesLoad=self.batteries.use_on(self.get_combined_load(),simulationConfig)
            self.detailedLoad[self.batteries]=batteriesLoad
            


    def get_detailed_load(self)->Dict[BaseFactor,np.ndarray]:
        return self.detailedLoad
    
    def get_detailed_load_df(self)->pd.DataFrame:
        df_detailed=pd.DataFrame()
        timeSeries=self.configLastSimulation.get_time_series()
        df_detailed["TimeStamp"] = timeSeries.index
        for asset, load in self.detailedLoad.items():
            serie = pd.Series(load)
            df_detailed[f"{asset.get_name()}_{asset.get_id()}"] = serie


        return df_detailed

    def get_combined_load(self)->np.ndarray: #combina pv i load restant pv a load
        if self.configLastSimulation is not None:
            combinedLoad=np.zeros(self.configLastSimulation.num_indices())
            for asset, load in self.detailedLoad.items():
                factor_type=asset.get_factor_type()
                if factor_type==FactorType.Consumer or factor_type==FactorType.Prosumer or factor_type==FactorType.Battery:
                    combinedLoad+=load
                elif factor_type==FactorType.Producer:
                    combinedLoad-=load
            return combinedLoad
        else: raise ValueError("theres no simulated load")

    def get_name(self)->str:
        return self.name
    
    def get_id(self)->int:
        return self.id

    def get_load_pv(self)->Tuple[np.ndarray,np.ndarray]: #retorna pv i load per separat
        if self.configLastSimulation is not None:
            finalLoad=np.zeros(self.configLastSimulation.num_indices())
            finalPv=np.zeros(self.configLastSimulation.num_indices())
            for asset, load in self.detailedLoad.items():
                factor_type=asset.get_factor_type()
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
    
    def get_combined_load_pv(self)->Tuple[np.ndarray,np.ndarray]: #resta pv a load i retorna un array per pv i un per load amb aquesta combinacio, load sera 0 si la combinacio es negativa i pv 0 si es positiva, es a dir: Exemple: initialLoad=[1,2] initialPv=[0,3] -> combinacio=[1,-1] -> (returned load =[1,0}, returned pv=[0,1])
        if self.configLastSimulation is not None:
            combinedLoad=np.zeros(self.configLastSimulation.num_indices())
            combinedPv=np.zeros(self.configLastSimulation.num_indices())
            for asset, load in self.detailedLoad.items():
                factor_type=asset.get_factor_type()
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