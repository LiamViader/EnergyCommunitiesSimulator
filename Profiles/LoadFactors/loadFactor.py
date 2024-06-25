from abc import ABC, abstractmethod
from Profiles.profileConfiguration import ProfileConfig
from utils.enums import LoadType

class LoadFactor(ABC):
    def __init__(self, name:str, loadType:LoadType):
        self.name = name
        self.loadType=loadType
    
    @abstractmethod
    def generate_load(self,profileConfig:ProfileConfig):
        pass  

    def get_name(self)->str:
        return self.name

    def get_load_type(self)->LoadType:
        return self.loadType