from Profiles.utils.profileEnergyDataAux import ProfileEnergyDataAux
from Profiles.utils.profileSharingsDataAux import ProfileSharingsDataAux
from Simulation.simulationConfiguration import SimulationConfig
from typing import List, Dict, Tuple
from abc import ABC, abstractmethod
import numpy as np

class SharingMethod(ABC):
    """
    Abstract base class for implementing energy sharing methods within a community.

    This class serves as a blueprint for various methods that can be used to share
    energy profiles among users or systems in a community. It defines the necessary
    structure and interface that all sharing methods must adhere to.

    Attributes:
        _name (str): The name of the sharing method.

    Methods:
        share(profiles: List[ProfileEnergyDataAux], sharePersonalPvs: bool, communityPv: float) -> List[ProfileSharingsDataAux]:
            Abstract method for sharing energy profiles based on the specified criteria.
        
        get_name() -> str:
            Returns the name of the sharing method.
    """
    def __init__(self, name:str) -> None:
        """
        Initializes the SharingMethod instance with a specified name.

        Args:
            name (str): The name of the sharing method.
        """
        self._name=name

    @abstractmethod
    def share(self,profiles:List[ProfileEnergyDataAux],sharePersonalPvs:bool,communityPv:float)->List[ProfileSharingsDataAux]:
        """
        Abstract method to implement the logic for sharing energy profiles within a community.

        This method must be implemented by subclasses to define how energy profiles are shared
        based on the specified criteria, including whether to share personal production
        system outputs and how much community production is available for distribution.

        Args:
            profiles (List[ProfileEnergyDataAux]): A list of energy profiles representing the consumption
                and production patterns of different community members.
            sharePersonalPvs (bool): Indicates whether the outputs from personal production systems should be included
                in the sharing process.
            communityPv (float): The total amount of community production energy available for sharing among users.

        Returns:
            List[ProfileSharingsDataAux]: A users and their respective allocateds energys that have been allocated based on the 
            sharing method's logic, reflecting the new distribution of energy among community members.
        """
        pass

    def get_name(self)->str:
        """
        Returns the name of the sharing method.

        This method allows users to identify which sharing method is being used.

        Returns:
            str: The name of the sharing method.
        """
        return self._name