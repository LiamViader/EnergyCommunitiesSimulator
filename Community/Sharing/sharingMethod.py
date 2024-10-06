from Profiles.utils.profileEnergyDataAux import ProfileEnergyDataAux
from Profiles.utils.profileSharingsDataAux import ProfileSharingsDataAux
from Simulation.simulationConfiguration import SimulationConfig
from typing import List, Dict, Tuple
from abc import ABC, abstractmethod
import numpy as np

class SharingMethod(ABC):
    def __init__(self, name:str) -> None:
        self._name=name

    @abstractmethod
    def share(self,profiles:List[ProfileEnergyDataAux],sharePersonalPvs:bool,communityPv:float)->List[ProfileSharingsDataAux]:
        pass

    def get_name(self)->str:
        return self._name