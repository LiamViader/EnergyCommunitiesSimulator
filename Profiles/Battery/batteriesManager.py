from typing import List
from Profiles.Battery.battery import Battery
import pandas as pd
from Profiles.Factors.baseFactor import BaseFactor
from utils.enums import FactorType
from Simulation.simulationConfiguration import SimulationConfig
import numpy as np

class BatteriesManager(BaseFactor):
    """
    Manages a collection of batteries to charge or discharge energy based on the input energy comsumption/production.

    This class acts as a bridge between the load demand or production excedents and the battery system, allowing for
    efficient energy storage and retrieval. It can charge batteries when there is excess energy
    and discharge them when energy is needed.

    Attributes:
        _batteries (List[Battery]): A list of Battery objects managed by this manager.

    Methods:
        use_on(load: np.ndarray, config: SimulationConfig) -> np.ndarray:
            Applies the input load to the batteries and returns the load profile based on battery usage.

        simulate(simulationConfig: SimulationConfig) -> np.ndarray:
            Placeholder method to fulfill the abstract base class requirement.
    """
    def __init__(self,batteries:List[Battery]):
        """
        Initializes the BatteriesManager with a list of Battery objects.

        Args:
            batteries (List[Battery]): A list of Battery instances to be managed.
        """
        super().__init__("batteries", FactorType.Battery)
        self._batteries=batteries

    def use_on(self,load:np.ndarray,config:SimulationConfig)->np.ndarray:
        """
        Applies the input load profile to the batteries, managing charge and discharge cycles.

        Args:
            load (np.ndarray): An array representing the load profile where positive values indicate consumption
                              and negative values indicate production.
            config (SimulationConfig): The simulation configuration.

        Returns:
            np.ndarray: An array representing the load profile of the batteries during the simulated day.
        """
        minutersPerIndex=1440/config.num_indices()

        def batteriesLoad(value):
            if value>0:
                charging=False
            elif value<0:
                charging=True
            else:
                return 0
            energyLeft=abs(value)
            batteriesLoad=0
            for battery in self._batteries:
                if energyLeft>0:
                    if charging:
                        usedEnergy=battery.charge(energy=energyLeft,timeElapsed=minutersPerIndex)
                        energyLeft-=usedEnergy
                        batteriesLoad+=usedEnergy
                    else:
                        producedEnergy=battery.discharge(energy=energyLeft,timeElapsed=minutersPerIndex)
                        energyLeft-=producedEnergy
                        batteriesLoad-=producedEnergy
            return batteriesLoad
        
        return np.vectorize(batteriesLoad)(load)
    
    def simulate(self, simulationConfig: SimulationConfig) -> np.ndarray: #simplement perque la classe no sigui abstracta
        return None
        


                    
