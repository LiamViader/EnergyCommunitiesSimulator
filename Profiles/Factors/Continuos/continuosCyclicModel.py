import random
import numpy as np
from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution

class ContinuosCyclicModel():
    def __init__(self, name: str, idlePower: BaseNumberDistribution, activePower: BaseNumberDistribution, timeBetweenCycles:BaseNumberDistribution, cycleDuration:BaseNumberDistribution):
        self.name=name
        self.idlePower = idlePower #potencia quan no està en el cicle actiu en kw
        self.activePower = activePower
        self.timeBetweenCycles = timeBetweenCycles
        self.cycleDuration = cycleDuration



    def get_active_power(self)->float:
        return self.activePower.generate_random()

    def get_idle_power(self)->float:
        return self.idlePower.generate_random()

    def get_name(self)->str:
        return self.name
    
    def get_time_between_next_cycle(self)->float:
        return self.timeBetweenCycles.generate_random()
    
    def get_cycle_duration(self)->float:
        return self.cycleDuration.generate_random()
