from Profiles.utils.profileCostDataAux import ProfileCostDataAux
from Profiles.utils.profileSharingsDataAux import ProfileSharingsDataAux
from EnergyPrice.EnergyPlans.baseEnergyPlan import BaseEnergyPlan
from Simulation.simulationConfiguration import SimulationConfig
from typing import List, Dict, Tuple
from abc import ABC, abstractmethod
import numpy as np
from datetime import datetime

class CostCalculationBaseMethod(ABC):
    def __init__(self, name:str) -> None:
        self._name=name

    @abstractmethod
    def calculate(self,sharingsAndPlan:List[Tuple[ProfileSharingsDataAux,BaseEnergyPlan]],communityPlan:BaseEnergyPlan,datetimeValue:datetime)->List[ProfileCostDataAux]:
        pass

    def get_name(self)->str:
        return self._name