import numpy as np
import random
from typing import List,Tuple
from utils.minuteInterval import MinuteInterval
from Profiles.Factors.Cyclic.cyclicModel import CyclicModel
from Profiles.profileConfiguration import ProfileConfig
from Profiles.Factors.Cyclic.UseConfig.cyclicBaseUseConfig import CyclicBaseUseConfig


class CyclicDaylyUseConfig(CyclicBaseUseConfig):
    def __init__(self,weekUsage:Tuple[List[MinuteInterval],List[MinuteInterval],List[MinuteInterval],List[MinuteInterval],List[MinuteInterval],List[MinuteInterval],List[MinuteInterval]]):#weekUsage te per cada dia de la setmana, els intervals al que es sol usar
        self.weekUsage=weekUsage
        
    
    def use(self,cyclicModel:CyclicModel,profileConfig:ProfileConfig)->Tuple[np.ndarray,np.ndarray]:
        load=np.zeros(profileConfig.num_indices())
        overflow=np.array([])
        weekDay=profileConfig.get_day_of_week()
        for interval in self.weekUsage[weekDay]:
            startInMinutes=interval.random()
            overflow=self.__distribute_cycle_load(load,overflow,startInMinutes,profileConfig,cyclicModel)
        return load,overflow


    def __distribute_cycle_load(self,load:np.ndarray,overflow:np.ndarray,selectedStartWashingInMinutes:float,profileConfig:ProfileConfig,cyclicModel:CyclicModel)->np.ndarray:
        totalTime=cyclicModel.get_cycle_minutes()
        timeRemaining=totalTime
        power=cyclicModel.get_cycle_power()
        while(timeRemaining>0):
            timeElapsed=totalTime-timeRemaining
            currentTimestampMinutes=selectedStartWashingInMinutes+timeElapsed
            indicesPerMinute=profileConfig.num_indices()/1440
            currentIndex=int(currentTimestampMinutes*indicesPerMinute)
            nextIndex=currentIndex+1
            nextIndexTimestampMinutes=nextIndex/indicesPerMinute
            hoursElapsedThisIteration=min(((nextIndexTimestampMinutes-currentTimestampMinutes)/60),timeRemaining/60)
            indexLoad=power*hoursElapsedThisIteration
            if(currentIndex<profileConfig.num_indices()):#si hi cap al dia actual
                load[currentIndex]+=indexLoad
            else:#sino al overflow
                transformedCurrentIndex=currentIndex-profileConfig.num_indices()
                if transformedCurrentIndex<len(overflow):
                    overflow[transformedCurrentIndex]+=indexLoad
                else:
                    new_overflow=np.zeros(transformedCurrentIndex + 1, dtype=overflow.dtype)
                    new_overflow[:len(overflow)] = overflow
                    overflow=new_overflow
                    overflow[transformedCurrentIndex]+=indexLoad
            timeRemaining=timeRemaining-hoursElapsedThisIteration*60
        return overflow
