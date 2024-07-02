from typing import List
from Profiles.Battery.battery import Battery
import pandas as pd
from Profiles.profileConfiguration import ProfileConfig

class BatteriesManager:
    def __init__(self,batteries:List[Battery]):
        self.batteries=batteries

    def use(self,load:pd.Series,config:ProfileConfig)->pd.Series: #rep una carrega on consum es positiu i produccio negatiu, i retorna un perfil de carrega de les bateries si son usades sobre la carrega d'entrada
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
            for battery in self.batteries:
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
        
        return load.apply(batteriesLoad)
        


                    
