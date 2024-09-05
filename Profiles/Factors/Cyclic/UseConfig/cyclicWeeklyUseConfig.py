import numpy as np
import random
from typing import List,Tuple
from utils.minuteInterval import MinuteInterval
from Profiles.Factors.Cyclic.cyclicModel import CyclicModel
from Simulation.simulationConfiguration import SimulationConfig
from Profiles.Factors.Cyclic.UseConfig.cyclicBaseUseConfig import CyclicBaseUseConfig


class CyclicWeeklyUseConfig(CyclicBaseUseConfig):
    def __init__(self,timesWeekly:int,intervals:List[MinuteInterval]):
        #intervals is an array of intervals
        self.timesWeekly=timesWeekly #cops que posa rentaplats a la setmana
        self.intervals=np.array(intervals) #les franges a les quals sol posar la rentadora
        
    def get_random_interval(self)->MinuteInterval:
        return self.intervals[random.randint(0,len(self.intervals)-1)]
    
    def use(self,cyclicModel:CyclicModel,simulationConfig:SimulationConfig)->Tuple[np.ndarray,np.ndarray]:
        load=np.zeros(simulationConfig.num_indices())
        overflow=np.array([])
        daylyAverage=self.timesWeekly/7
        #es podria utilitzar distribucio poisson, pero penso que és més adequat que si la mitja és major que 1 la posi una vegada com a minim, ja que en el cas de posar el rentaplats si algu el posa 7/7 dies és més probable que el posi cada dia, que que el posi un dia 2 cops, un altre 1, un altre 0...
        intervals=self.intervals.copy()
        while daylyAverage>=1:
            if(len(intervals)>0):
                randomIndexInterval=random.randint(0,len(intervals)-1)
                selectedInterval=intervals[randomIndexInterval]
                intervals=np.delete(intervals,randomIndexInterval)
            else:
                selectedInterval=self.get_random_interval()
            selectedStartWashingInMinutes=selectedInterval.random()
            overflow=self.__distribute_cycle_load(load,overflow,selectedStartWashingInMinutes,simulationConfig,cyclicModel)
            daylyAverage-=1
        rand_float=random.random()
        if(rand_float<daylyAverage):
            if(len(intervals)>0):
                randomIndexInterval=random.randint(0,len(intervals)-1)
                selectedInterval=intervals[randomIndexInterval]
                intervals=np.delete(intervals,randomIndexInterval)
            else:
                selectedInterval=self.get_random_interval()
            selectedStartWashingInMinutes=selectedInterval.random()
            overflow=self.__distribute_cycle_load(load,overflow,selectedStartWashingInMinutes,simulationConfig,cyclicModel)
        return load, overflow


    def __distribute_cycle_load(self,load:np.ndarray,overflow:np.ndarray,selectedStartWashingInMinutes:float,simulationConfig:SimulationConfig,cyclicModel:CyclicModel):
        timeRemaining=cyclicModel.get_cycle_minutes()
        while(timeRemaining>0):
            timeElapsed=cyclicModel.get_cycle_minutes()-timeRemaining
            currentTimestampMinutes=selectedStartWashingInMinutes+timeElapsed
            indicesPerMinute=simulationConfig.num_indices()/1440
            currentIndex=int(currentTimestampMinutes*indicesPerMinute)
            nextIndex=currentIndex+1
            nextIndexTimestampMinutes=nextIndex/indicesPerMinute
            hoursElapsedThisIteration=min(((nextIndexTimestampMinutes-currentTimestampMinutes)/60),timeRemaining/60)
            indexLoad=cyclicModel.get_cycle_power()*hoursElapsedThisIteration
            if(currentIndex<simulationConfig.num_indices()):#si hi cap al dia actual
                load[currentIndex]+=indexLoad
            else:#sino al overflow
                transformedCurrentIndex=currentIndex-simulationConfig.num_indices()
                if transformedCurrentIndex<len(overflow):
                    overflow[transformedCurrentIndex]+=indexLoad
                else:
                    new_overflow=np.zeros(transformedCurrentIndex + 1, dtype=overflow.dtype)
                    new_overflow[:len(overflow)] = overflow
                    overflow=new_overflow
                    overflow[transformedCurrentIndex]+=indexLoad
            timeRemaining=timeRemaining-hoursElapsedThisIteration*60
        return overflow
