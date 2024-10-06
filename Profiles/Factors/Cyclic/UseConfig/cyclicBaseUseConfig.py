import numpy as np
import random
from typing import List,Tuple
from utils.minuteInterval import MinuteInterval
from Profiles.Factors.Cyclic.cyclicModel import CyclicModel
from Simulation.simulationConfiguration import SimulationConfig
from abc import ABC, abstractmethod


class CyclicBaseUseConfig(ABC):
    """
    Abstract base class for configuring the use pattern of cyclic energy-consuming models.

    This class defines the basic structure and interface for different configurations of how cyclic models
    (e.g., appliances like washing machines or dishwashers) are used within a simulation. Specific use configurations
    should extend this class and implement the `use` method.

    Methods:
        use(cyclicModel: CyclicModel, simulationConfig: SimulationConfig) -> Tuple[np.ndarray, np.ndarray]:
            Abstract method to simulate energy consumption for a cyclic model based on a specific usage configuration.
            Must be implemented by subclasses.
    """
    def __init__(self):
        """
        Initializes a CyclicBaseUseConfig instance.
        This class is abstract and is meant to be subclassed.
        """
        pass
    
    @abstractmethod
    def use(self,cyclicModel:CyclicModel,simulationConfig:SimulationConfig)->Tuple[np.ndarray,np.ndarray]:
        """
        Simulates the energy usage of a cyclic model for a given simulation configuration.

        Args:
            cyclicModel (CyclicModel): The cyclic model whose usage pattern is being simulated.
            simulationConfig (SimulationConfig): The configuration parameters for the simulation.

        Returns:
            Tuple[np.ndarray, np.ndarray]: A tuple containing two arrays:
                - The first array represents the energy consumption pattern over a day.
                - The second array represents any overflow, which is energy consumption that should be carried over to the next day.
        """
        pass




