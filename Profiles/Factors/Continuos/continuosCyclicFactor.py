import pandas as pd
import numpy as np
import random
from typing import Tuple
from Profiles.Factors.baseFactor import BaseFactor
from Profiles.Factors.useConfig import UseConfig
from Profiles.profileConfiguration import ProfileConfig
from Profiles.Factors.Continuos.continuosCyclicModel import ContinuosCyclicModel
from utils.enums import FactorType

#properties of the dishwasher
class ContinuosCyclicFactor(BaseFactor):
    def __init__(self, model:ContinuosCyclicModel):
        super().__init__(model.get_name(), FactorType.Consumer)
        self.model=model

    def simulate(self, profileConfig: ProfileConfig) -> Tuple[pd.Series,pd.Series]:
        load=np.zeros(profileConfig.num_indices())
        overflow=np.zeros(profileConfig.num_indices())
        idle=True
        timeElapsed=0
        indicesPerHour=profileConfig.num_indices()/24
        while timeElapsed<24.0:
            if idle:
                cycleDurationTime=self.model.get_time_between_next_cycle()
                power=self.model.get_idle_power()
            else:
                cycleDurationTime=self.model.get_cycle_duration()
                power=self.model.get_active_power()+self.model.get_idle_power()
            nextCycleTimestamp=cycleDurationTime+timeElapsed
            while timeElapsed<nextCycleTimestamp:
                currentIndex=int(timeElapsed*indicesPerHour)
                nextIndex=currentIndex+1
                timestampNextIndex=nextIndex/indicesPerHour
                nextTimestamp=min(nextCycleTimestamp,timestampNextIndex)
                energy=(nextTimestamp-timeElapsed)*power
                if currentIndex<profileConfig.num_indices():
                    load[currentIndex]=energy
                elif not idle:
                    overflow[currentIndex-profileConfig.num_indices()]=energy
                timeElapsed=nextTimestamp
            idle=not idle
        return pd.Series(load), pd.Series(overflow)

