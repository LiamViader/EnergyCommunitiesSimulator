from abc import ABC, abstractmethod
from Simulation.simulationConfiguration import SimulationConfig
from utils.enums import FactorType
from typing import Tuple
import numpy as np
import pandas as pd

class BaseFactor(ABC):
    """
    Abstract base class for defining factors that can simulate energy consumption or production.

    This class serves as a blueprint for specific factor implementations, including 
    their attributes and methods. Each factor has a unique identifier, a name, 
    and a type indicating whether it is a consumer, producer, or another category.
    Each derived specific factor must implement the method simulate()

    Attributes:
        _idCounter (int): Static counter to generate unique IDs for each factor.

        _id (int): Unique identifier for the factor instance.

        _name (str): Name of the factor.
        
        _factorType (FactorType): Type of the factor, indicating its role (e.g., FactorType.Consumer, FactorType.Producer,...).

    Methods:
        simulate(simulationConfig: SimulationConfig) -> np.ndarray: Abstract method to simulate energy over a day.
        get_name() -> str: Returns the name of the factor.
        get_factor_type() -> FactorType: Returns the type of the factor.
        get_id() -> int: Returns the unique identifier of the factor.
    """
    _idCounter=0

    def __init__(self, name:str, factorType:FactorType):
        """
        Initializes the base factor with a name and type.

        Each instance is assigned a unique ID, which is incremented from a static counter.

        Args:
            name (str): The name of the factor.
            factorType (FactorType): The type of the factor, indicating its role (e.g., FactorType.Consumer, FactorType.Producer,...).
        """
        BaseFactor._idCounter+=1
        self._id=BaseFactor._idCounter
        self._name = name
        self._factorType=factorType
    
    @abstractmethod
    def simulate(self,simulationConfig:SimulationConfig)->np.ndarray:
        """
        Simulates the energy consumption or production over a day.

        This method must be implemented by subclasses. It returns an array representing 
        the energy consumed or produced over time during a day, measured in kWh.
        Each index of the array represents energy consumed or produced on the time elapsed based on granularity. 

        Args:
            simulationConfig (SimulationConfig): Configuration settings for the simulation.

        Returns:
            np.ndarray: An array where the first series represents the energy over time 
            (in kWh) Each index of the array represents energy consumed or produced on the time elapsed based on granularity. The full array represents a day
        """
        pass
    
    def get_name(self)->str:
        """
        Gets the name of the factor.

        Returns:
            str: The name of the factor.
        """
        return self._name

    def get_factor_type(self)->FactorType:
        """
        Gets the type of the factor.

        Returns:
            FactorType: The type of the factor (e.g., consumer, producer).
        """
        return self._factorType
    
    def get_id(self)->int:
        """
        Gets the unique identifier of the factor.

        Returns:
            int: The unique identifier of the factor instance.
        """
        return self._id