from abc import ABC, abstractmethod
from Profiles.loadConfiguration import LoadConfig

class LoadFactor(ABC):
    def __init__(self, name:str):
        self.name = name
    
    @abstractmethod
    def generate_load(self,loadConfig:LoadConfig,iters:int=None):
        pass  

    def get_name(self)->str:
        return self.name