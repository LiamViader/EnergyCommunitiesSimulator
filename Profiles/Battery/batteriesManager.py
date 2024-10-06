from typing import List
from Profiles.Battery.battery import Battery
import pandas as pd
from Profiles.Factors.baseFactor import BaseFactor
from utils.enums import FactorType
from Simulation.simulationConfiguration import SimulationConfig
import numpy as np

class BatteriesManager(BaseFactor):
    def __init__(self,batteries:List[Battery]):
        super().__init__("batteries", FactorType.Battery)
        self._batteries=batteries

    def use_on(self,load:np.ndarray,config:SimulationConfig)->np.ndarray: #rep una carrega on consum es positiu i produccio negatiu, i retorna un perfil de carrega de les bateries si son usades sobre la carrega d'entrada
        minutersPerIndex=1440/config.num_indices()

        def batteriesLoad(value):
            if value>0:
                charging=False
            elif value<0:
                charging=True
            else:
                return 0
            energyLeft=abs(value)
            batteriesLoad=0
            for battery in self._batteries:
                if energyLeft>0:
                    if charging:
                        usedEnergy=battery.charge(energy=energyLeft,timeElapsed=minutersPerIndex)
                        energyLeft-=usedEnergy
                        batteriesLoad+=usedEnergy
                    else:
                        producedEnergy=battery.discharge(energy=energyLeft,timeElapsed=minutersPerIndex)
                        energyLeft-=producedEnergy
                        batteriesLoad-=producedEnergy
            return batteriesLoad
        
        return np.vectorize(batteriesLoad)(load)
    
    def simulate(self, simulationConfig: SimulationConfig) -> np.ndarray: #simplement perque la classe no sigui abstracta
        return None
        


                    
