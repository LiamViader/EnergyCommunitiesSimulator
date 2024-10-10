from Profiles.utils.profileCostDataAux import ProfileCostDataAux
from Profiles.utils.profileSharingsDataAux import ProfileSharingsDataAux
from EnergyPrice.EnergyPlans.baseEnergyPlan import BaseEnergyPlan
from Simulation.simulationConfiguration import SimulationConfig
from typing import List, Dict, Tuple
from abc import ABC, abstractmethod
import numpy as np
from datetime import datetime

class CostCalculationBaseMethod(ABC):
    """
    Abstract base class to define a cost calculation method for energy plans. 

    This class requires implementation of the `calculate` method, which should calculate the cost 
    for different profiles sharing energy, considering individual and community energy plans.

    Attributes:
        _name (str): Name of the cost calculation method.
    
    Methods:
        calculate(sharingsAndPlan: List[Tuple[ProfileSharingsDataAux, BaseEnergyPlan]], 
                  communityPlan: BaseEnergyPlan, datetimeValue: datetime) -> List[ProfileCostDataAux]:
            Abstract method to calculate the cost for profiles sharing energy based on energy plans.
        
        get_name() -> str:
            Returns the name of the cost calculation method.
    """
    def __init__(self, name:str) -> None:
        """
        Initializes the CostCalculationBaseMethod class with a name.
        
        Args:
            name (str): The name of the cost calculation method.
        """
        self._name=name

    @abstractmethod
    def calculate(self,sharingsAndPlan:List[Tuple[ProfileSharingsDataAux,BaseEnergyPlan]],communityPlan:BaseEnergyPlan,datetimeValue:datetime)->List[ProfileCostDataAux]:
        """
        Abstract method to calculate the cost for profiles sharing energy based on energy plans.
        
        Args:
            sharingsAndPlan (List[Tuple[ProfileSharingsDataAux, BaseEnergyPlan]]): A list of tuples, 
                each containing sharing data and the corresponding energy plan for a profile.
            communityPlan (BaseEnergyPlan): The community's shared energy plan.
            datetimeValue (datetime): The datetime for which the cost is calculated.
        
        Returns:
            List[ProfileCostDataAux]: A list of cost data for each profile.
        """
        pass

    def get_name(self)->str:
        """
        Returns the name of the cost calculation method.
        
        Returns:
            str: The name of the cost calculation method.
        """
        return self._name