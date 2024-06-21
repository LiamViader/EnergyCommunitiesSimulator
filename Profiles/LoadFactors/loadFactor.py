from abc import ABC, abstractmethod
from Profiles.loadConfiguration import LoadConfig
from utils.enums import LoadType

class LoadFactor(ABC):
    def __init__(self, name:str, loadType:LoadType):
        self.name = name
        self.loadType=loadType
    
    @abstractmethod
    def generate_load(self,loadConfig:LoadConfig,iters:int=None):
        pass  

    def get_name(self)->str:
        return self.name

    def get_load_type(self)->LoadType:
        return self.loadType