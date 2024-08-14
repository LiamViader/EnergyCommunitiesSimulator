import pandas as pd
import numpy as np
import random
from typing import Tuple
from Profiles.Factors.baseFactor import BaseFactor
from Profiles.Factors.Cyclic.UseConfig.cyclicBaseUseConfig import CyclicBaseUseConfig
from Profiles.profileConfiguration import ProfileConfig
from Profiles.Factors.Cyclic.cyclicModel import CyclicModel
from utils.enums import FactorType

class CyclicFactor(BaseFactor):
    def __init__(self,
                 cyclicModel:CyclicModel, 
                 useConfig:CyclicBaseUseConfig):
        
        super().__init__(cyclicModel.get_name(),FactorType.Consumer)
        self.cyclicModel=cyclicModel
        self.useConfig=useConfig #config de rentat (dies setmana, franges horaries..)
        self.overflow=None



    def simulate(self,profileConfig:ProfileConfig)->np.ndarray:
        load=np.zeros(profileConfig.num_indices())
        if self.overflow is not None:
            overflowPadded = np.pad(self.overflow, (0, len(load) - len(self.overflow)), 'constant')
            load+=overflowPadded
        hoursElapsedPerIndex=24.0/profileConfig.num_indices()
        for i in range(profileConfig.num_indices()):#afegeixo primer el standbypower
            load[i]+=self.cyclicModel.get_stand_by_power()*hoursElapsedPerIndex

        useLoad,overflow=self.useConfig.use(self.cyclicModel,profileConfig)
        load+=useLoad
        self.overflow=overflow
        return load





    



    def changeUseConfig(self,useConfig:CyclicBaseUseConfig):
        self.useConfig=useConfig

