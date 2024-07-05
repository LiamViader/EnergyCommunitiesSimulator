import pandas as pd
import numpy as np
import random
from typing import Tuple
from Profiles.Factors.baseFactor import BaseFactor
from Profiles.Factors.useConfig import UseConfig
from Profiles.profileConfiguration import ProfileConfig
from Profiles.Factors.Cyclic.cyclicModel import CyclicModel
from utils.enums import FactorType

#properties of the dishwasher
class CyclicFactor(BaseFactor):
    def __init__(self,
                 cyclicModel:CyclicModel, 
                 washingConfig:UseConfig):
        
        super().__init__(cyclicModel.get_name(),FactorType.Consumer)
        self.cyclicModel=cyclicModel
        self.washingConfig=washingConfig #config de rentat (dies setmana, franges horaries..)
        self.overflow=None

    def simulate(self,profileConfig:ProfileConfig)->np.ndarray:
        load=np.zeros(profileConfig.num_indices())
        if self.overflow is not None:
            overflowPadded = np.pad(self.overflow, (0, len(load) - len(self.overflow)), 'constant')
            load+=overflowPadded
        self.overflow=np.array([])
        hoursElapsedPerIndex=24.0/profileConfig.num_indices()
        for i in range(profileConfig.num_indices()):#afegeixo primer el standbypower
            load[i]+=self.cyclicModel.get_stand_by_power()*hoursElapsedPerIndex

        daylyAverage=self.washingConfig.times_weekly()/7
        #es podria utilitzar distribucio poisson, pero penso que és més adequat que si la mitja és major que 1 la posi una vegada com a minim, ja que en el cas de posar el rentaplats si algu el posa 7/7 dies és més probable que el posi cada dia, que que el posi un dia 2 cops, un altre 1, un altre 0...
        intervals=self.washingConfig.get_intervals()
        while daylyAverage>=1:
            if(len(intervals)>0):
                randomIndexInterval=random.randint(0,len(intervals)-1)
                selectedInterval=intervals[randomIndexInterval]
                intervals=np.delete(intervals,randomIndexInterval)
            else:
                selectedInterval=self.washingConfig.get_random_interval()
            selectedStartWashingInMinutes=selectedInterval.random()
            self.__distribute_cycle_load(load,selectedStartWashingInMinutes,profileConfig)
            daylyAverage-=1
        rand_float=random.random()
        if(rand_float<daylyAverage):
            if(len(intervals)>0):
                randomIndexInterval=random.randint(0,len(intervals)-1)
                selectedInterval=intervals[randomIndexInterval]
                intervals=np.delete(intervals,randomIndexInterval)
            else:
                selectedInterval=self.washingConfig.get_random_interval()
            selectedStartWashingInMinutes=selectedInterval.random()
            self.__distribute_cycle_load(load,selectedStartWashingInMinutes,profileConfig)
        return load



    def __distribute_cycle_load(self,load:np.ndarray,selectedStartWashingInMinutes:float,profileConfig:ProfileConfig):
        timeRemaining=self.cyclicModel.get_cycle_time()
        while(timeRemaining>0):
            timeElapsed=self.cyclicModel.get_cycle_time()-timeRemaining
            currentTimestampMinutes=selectedStartWashingInMinutes+timeElapsed
            indicesPerMinute=profileConfig.num_indices()/1440
            currentIndex=int(currentTimestampMinutes*indicesPerMinute)
            nextIndex=currentIndex+1
            nextIndexTimestampMinutes=nextIndex/indicesPerMinute
            hoursElapsedThisIteration=min(((nextIndexTimestampMinutes-currentTimestampMinutes)/60),timeRemaining/60)
            indexLoad=self.cyclicModel.get_cycle_power()*hoursElapsedThisIteration
            if(currentIndex<profileConfig.num_indices()):#si hi cap al dia actual
                load[currentIndex]+=indexLoad
            else:#sino al overflow
                transformedCurrentIndex=currentIndex-profileConfig.num_indices()
                if transformedCurrentIndex<len(self.overflow):
                    self.overflow[transformedCurrentIndex]+=indexLoad
                else:
                    new_overflow=np.zeros(transformedCurrentIndex + 1, dtype=self.overflow.dtype)
                    new_overflow[:len(self.overflow)] = self.overflow
                    self.overflow=new_overflow
                    self.overflow[transformedCurrentIndex]+=indexLoad
            timeRemaining=timeRemaining-hoursElapsedThisIteration*60



    def changeWashingConfig(self,washingConfig:UseConfig):
        self.washingConfig=washingConfig

