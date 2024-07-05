import pandas as pd
import numpy as np
import random
from typing import Tuple
from Profiles.Factors.baseFactor import BaseFactor
from Profiles.Factors.Cyclic.cyclicUseConfig import UseConfig
from Profiles.profileConfiguration import ProfileConfig
from Profiles.Factors.Continuos.continuosCyclicModel import ContinuosCyclicModel
from utils.enums import FactorType

#properties of the dishwasher
class ContinuosCyclicFactor(BaseFactor):
    def __init__(self, model:ContinuosCyclicModel):
        super().__init__(model.get_name(), FactorType.Consumer)
        self.model=model
        self.overflowTime=0
        self.overflowPower=0
        self.idle=True

    def simulate(self, profileConfig: ProfileConfig) -> np.ndarray:
        load=np.zeros(profileConfig.num_indices())
        self.distribute_cycle_load(self.overflowPower,0,self.overflowTime,profileConfig,load)
        timeElapsed=self.overflowTime
        while timeElapsed<24.0:
            if self.idle:
                cycleDurationTime=self.model.get_time_between_next_cycle()
                power=self.model.get_idle_power()
            else:
                cycleDurationTime=self.model.get_cycle_duration()
                power=self.model.get_active_power()+self.model.get_idle_power()
            nextCycleTimestamp=cycleDurationTime+timeElapsed
            self.distribute_cycle_load(power,timeElapsed,nextCycleTimestamp,profileConfig,load)
            timeElapsed=nextCycleTimestamp
            self.idle=not self.idle
        return load

    def distribute_cycle_load(self,power:float,start:float,end:float,profileConfig:ProfileConfig,load:np.ndarray): #distributes this cycle load on the load array
        indicesPerHour=profileConfig.num_indices()/24
        startIndex=int(start*indicesPerHour)
        endIndex=int(end*indicesPerHour)
        timestamp=start
        i=startIndex
        while i<=endIndex and i<profileConfig.num_indices():
            nextIndex=i+1
            nextIndexTimestamp=nextIndex/indicesPerHour
            if i!=endIndex:
                load[i]+=power*(nextIndexTimestamp-timestamp)
            else:
                load[i]+=power*(end-timestamp)
            timestamp=nextIndexTimestamp
            i=nextIndex
        if endIndex>=profileConfig.num_indices():
            self.overflowTime=end-timestamp
            self.overflowPower=power