import pandas as pd
import numpy as np
import random

#properties of the dishwasher
class Dishwasher:
    def __init__(self,name,cycleLoad,cycleTime):
        self.name=name
        self.cycleLoad=cycleLoad #consum del cicle de rentat en kwh
        self.cycleTime=cycleTime #temps que dura el cicle de rentat en minuts

    def generate_load(self,washingConfig,iters,loadConfig):
        load=np.zeros(loadConfig.num_indices())
        for i in range(iters): #n iteracions per aproximar montecarlo
            for j in range(washingConfig.times_weekly()): #per cada vegada que renta a la setmana
                interval=washingConfig.get_random_interval() #agafo interval random d'entre els possibles
                selectedStartWashingInMinutes=interval.random()
                indicesPerMinute=loadConfig.num_indices()/1440 #quants indexs representen un minut
                start_index = int(selectedStartWashingInMinutes * indicesPerMinute)
                end_index = int((selectedStartWashingInMinutes + self.cycleTime) * indicesPerMinute)
                nToDistribute=abs(end_index-start_index)+1
                if end_index>=loadConfig.num_indices():
                    end_index=end_index-loadConfig.num_indices()
                distributedLoad=self.cycleLoad/nToDistribute
                if start_index <= end_index:
                    load[start_index:end_index + 1] += distributedLoad/7 #ja que ho vull diari i no setmanal
                else:
                    load[start_index:] += distributedLoad
                    load[:end_index + 1] += distributedLoad 
        load /= iters
        return pd.Series(load)



