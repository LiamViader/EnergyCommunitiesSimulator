import numpy as np
import random
from typing import List,Tuple
from utils.minuteInterval import MinuteInterval
from Profiles.Factors.Cyclic.cyclicModel import CyclicModel
from Simulation.simulationConfiguration import SimulationConfig
from abc import ABC, abstractmethod


class CyclicBaseUseConfig(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def use(self,cyclicModel:CyclicModel,simulationConfig:SimulationConfig)->Tuple[np.ndarray,np.ndarray]:
        pass




