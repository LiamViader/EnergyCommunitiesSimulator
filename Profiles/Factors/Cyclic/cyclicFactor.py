import pandas as pd
import numpy as np
import random
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

    def simulate(self,profileConfig:ProfileConfig)->pd.Series:
        power=np.zeros(profileConfig.num_indices())
        for i in range(profileConfig.num_indices()):#afegeixo primer el standbypower
            power[i]+=self.cyclicModel.get_stand_by_power()
        
        indicesPerMinute=profileConfig.num_indices()/1440
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
            start_index = int(selectedStartWashingInMinutes * indicesPerMinute)
            end_index = int((selectedStartWashingInMinutes + self.cyclicModel.get_cycle_time()) * indicesPerMinute)
            power=self.__distribute_cycle_power(power,start_index,end_index,profileConfig)
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
            start_index = int(selectedStartWashingInMinutes * indicesPerMinute)
            end_index = int((selectedStartWashingInMinutes + self.cyclicModel.get_cycle_time()) * indicesPerMinute)
            power=self.__distribute_cycle_power(power,start_index,end_index,profileConfig)
        return pd.Series(power)
        
    def __distribute_cycle_power(self,power:np.array,startIndex:int,endIndex:int,profileConfig:ProfileConfig)->np.array:
        if endIndex>=profileConfig.num_indices():
            endIndex=endIndex-profileConfig.num_indices()
        instantPower=self.cyclicModel.get_cycle_power()
        if startIndex <= endIndex:
            power[startIndex:endIndex + 1] += instantPower
        else:
            power[startIndex:] += instantPower
            power[:endIndex + 1] += instantPower
        return power
                
    def changeWashingConfig(self,washingConfig:UseConfig):
        self.washingConfig=washingConfig



    """
    def generate_averaged_load(self,profileConfig:ProfileConfig,iters:int=100)->pd.Series:
        load=np.zeros(profileConfig.num_indices())
        for i in range(iters): #n iteracions per aproximar montecarlo
            for j in range(self.washingConfig.times_weekly()): #per cada vegada que renta a la setmana
                interval=self.washingConfig.get_random_interval() #agafo interval random d'entre els possibles
                selectedStartWashingInMinutes=interval.random()
                indicesPerMinute=profileConfig.num_indices()/1440 #quants indexs representen un minut
                start_index = int(selectedStartWashingInMinutes * indicesPerMinute)
                end_index = int((selectedStartWashingInMinutes + self.cycleTime) * indicesPerMinute)
                nToDistribute=abs(end_index-start_index)+1
                if end_index>=profileConfig.num_indices():
                    end_index=end_index-profileConfig.num_indices()
                distributedLoad=self.cycleLoad/nToDistribute
                if start_index <= end_index:
                    load[start_index:end_index + 1] += distributedLoad/7 #ja que ho vull diari i no setmanal
                else:
                    load[start_index:] += distributedLoad
                    load[:end_index + 1] += distributedLoad 
        load /= iters
        return pd.Series(load)
    """