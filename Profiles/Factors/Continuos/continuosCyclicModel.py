import random
import numpy as np

class ContinuosCyclicModel():
    def __init__(self, name: str, idlePower: float, activePower: float, maxTimeBetweenCycles: float, minTimeBetweenCycles: float, timeBetweenCyclesStd:float, maxCycleDuration: float, minCycleDuration: float, cycleDurationStd:float):
        self.name=name
        self.idlePower = idlePower #potencia quan no està en el cicle actiu en kw
        self.activePower = activePower
        self.maxTimeBetweenCycles = maxTimeBetweenCycles
        self.minTimeBetweenCycles = minTimeBetweenCycles
        self.maxCycleDuration = maxCycleDuration
        self.minCycleDuration = minCycleDuration
        self.timeBetweenCyclesStd = timeBetweenCyclesStd
        self. cycleDurationStd = cycleDurationStd



    def get_active_power(self)->float:
        return self.activePower

    def get_idle_power(self)->float:
        return self.idlePower

    def get_name(self)->str:
        return self.name
    
    def get_time_between_next_cycle(self)->float:
        mu=(self.maxTimeBetweenCycles+self.minTimeBetweenCycles)/2
        random_number = np.random.normal(mu, self.timeBetweenCyclesStd)
        return max(min(random_number, self.minTimeBetweenCycles), self.maxTimeBetweenCycles)
    
    def get_cycle_duration(self)->float:
        mu=(self.maxCycleDuration+self.minCycleDuration)/2
        random_number = np.random.normal(mu, self.cycleDurationStd)
        return max(min(random_number, self.minCycleDuration), self.maxCycleDuration)
