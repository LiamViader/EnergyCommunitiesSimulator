from abc import ABC, abstractmethod
from Profiles.profileConfiguration import ProfileConfig
from utils.enums import FactorType
import pandas as pd

class BaseFactor(ABC):
    def __init__(self, name:str, factorType:FactorType):
        self.name = name
        self.factorType=factorType
    
    @abstractmethod
    def simulate(self,profileConfig:ProfileConfig)->pd.Series: #retorna serie que representa la potencia de consum al llarg del temps
        pass

    def get_name(self)->str:
        return self.name

    def get_factor_type(self)->FactorType:
        return self.factorType