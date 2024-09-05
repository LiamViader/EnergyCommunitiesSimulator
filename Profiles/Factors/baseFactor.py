from abc import ABC, abstractmethod
from Simulation.simulationConfiguration import SimulationConfig
from utils.enums import FactorType
from typing import Tuple
import numpy as np
import pandas as pd

class BaseFactor(ABC):
    _idCounter=0

    def __init__(self, name:str, factorType:FactorType):
        BaseFactor._idCounter+=1
        self.id=BaseFactor._idCounter
        self.name = name
        self.factorType=factorType
    
    @abstractmethod
    def simulate(self,simulationConfig:SimulationConfig)->np.ndarray: #retorna array que representa la energia consumida/produida al llarg del temps durant un dia. en kwh. la segona serie es overflow (energia que s'ha simulat pel següent dia)
        pass
    
    def get_name(self)->str:
        return self.name

    def get_factor_type(self)->FactorType:
        return self.factorType
    
    def get_id(self)->int:
        return self.id