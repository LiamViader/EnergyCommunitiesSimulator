import pandas as pd
import numpy as np
import random
from typing import Tuple
from Profiles.Factors.baseFactor import BaseFactor
from Simulation.simulationConfiguration import SimulationConfig
from Profiles.Factors.Continuos.continuosCyclicModel import ContinuosCyclicModel
from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution
from utils.enums import FactorType


class ContinuosFactor(BaseFactor):
    """
    A class representing a continuous energy consumption factor.

    This class simulates the continuous consumption of energy over a period of time, using a constant power value
    that can vary slightly based on a random distribution.

    Attributes:
        _constant_power (BaseNumberDistribution): A distribution model representing the constant power usage 
        (with potential variations) for each time interval.

    Methods:
        simulate(simulationConfig: SimulationConfig) -> np.ndarray:
            Simulates the energy consumption over a given day based on the configuration and the constant power usage.
    """
    def __init__(self, name: str, factorType: FactorType, constantPower:BaseNumberDistribution):
        """
        Initializes the ContinuosFactor instance.

        Args:
            name (str): The name of the continuous factor (e.g., the name of the device or factor).
            factorType (FactorType): The type of factor (e.g., consumer, producer) as defined in the simulation.
            constantPower (BaseNumberDistribution): A distribution model representing the constant power usage for this factor.
        """
        super().__init__(name, factorType)
        self._constant_power=constantPower
    
    def simulate(self, simulationConfig: SimulationConfig) -> np.ndarray:
        """
        Simulates the energy consumption for the continuous factor over a single day.

        Args:
            simulationConfig (SimulationConfig): Configuration object that defines the simulation parameters, 
                                                 such as the number of time intervals (indices) per day.

        Returns:
            np.ndarray: An array representing the energy consumption (in kWh) for each time interval in a day based on granularity
        """
        load=np.zeros(simulationConfig.num_indices())
        hoursPerIndex=24/simulationConfig.num_indices()
        for i in range(simulationConfig.num_indices()):
            load[i]+=self._constant_power.generate_random()*hoursPerIndex
        return load