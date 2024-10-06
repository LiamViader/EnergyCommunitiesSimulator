import pandas as pd
import numpy as np
import random
from typing import Tuple
from Profiles.Factors.baseFactor import BaseFactor
from Profiles.Factors.Cyclic.UseConfig.cyclicBaseUseConfig import CyclicBaseUseConfig
from Simulation.simulationConfiguration import SimulationConfig
from Profiles.Factors.Cyclic.cyclicModel import CyclicModel
from utils.enums import FactorType

class CyclicFactor(BaseFactor):
    """
    Class representing a cyclic energy-consuming factor, such as appliances with repetitive usage patterns. (eg. Dishwashers, Washing machines...)

    This class models the behavior of cyclic consumers, such as appliances that follow specific usage patterns
    throughout the day or week. It simulates energy consumption, including standby power and active use, based
    on a defined configuration and cyclic model.

    Attributes:
        _cyclicModel (CyclicModel): The model representing the characteristics of the cyclic factor.
        _useConfig (CyclicBaseUseConfig): Configuration for usage, such as weekly schedules and hourly ranges.
        _overflow (Optional[np.ndarray]): Stores energy overflow from the current simulated day to carry over to the next day.

    Methods:
        simulate(simulationConfig: SimulationConfig) -> np.ndarray: Simulates the energy consumption of the factor.
        changeUseConfig(useConfig: CyclicBaseUseConfig): Changes the usage configuration for the cyclic factor.
    """
    def __init__(self,
                 cyclicModel:CyclicModel, 
                 useConfig:CyclicBaseUseConfig):
        """
        Initializes a CyclicFactor instance with a given cyclic model and usage configuration.

        Args:
            cyclicModel (CyclicModel): The cyclic model that defines the energy usage characteristics.
            useConfig (CyclicBaseUseConfig): The configuration that specifies usage patterns, such as days of the week,
                                             and time slots for operation.
        """
        super().__init__(cyclicModel.get_name(),FactorType.Consumer)
        self._cyclicModel=cyclicModel
        self._useConfig=useConfig #config de rentat (dies setmana, franges horaries..)
        self._overflow=None



    def simulate(self,simulationConfig:SimulationConfig)->np.ndarray:
        """
        Simulates the energy consumption of the cyclic factor over a day.

        This method computes the energy consumption for each time interval (as defined by the simulation configuration),
        including standby power and active usage as dictated by the cyclic model and the usage configuration.

        Args:
            simulationConfig (SimulationConfig): The configuration settings for the simulation, such as the number of time indices based on granularity.

        Returns:
            np.ndarray: An array representing the energy consumption of the cyclic factor over the simulation day.
            Each index of the array represents energy consumed or produced on the time elapsed based on granularity. The full array represents a day
        """
        load=np.zeros(simulationConfig.num_indices())
        if self._overflow is not None:
            overflowPadded = np.pad(self._overflow, (0, len(load) - len(self._overflow)), 'constant')
            load+=overflowPadded
        hoursElapsedPerIndex=24.0/simulationConfig.num_indices()
        for i in range(simulationConfig.num_indices()):#afegeixo primer el standbypower
            load[i]+=self._cyclicModel.get_stand_by_power()*hoursElapsedPerIndex

        useLoad,overflow=self._useConfig.use(self._cyclicModel,simulationConfig)
        load+=useLoad
        self._overflow=overflow
        return load


    def changeUseConfig(self,useConfig:CyclicBaseUseConfig):
        """
        Changes the usage configuration for the cyclic factor.

        This method allows updating the configuration that controls the usage patterns of the cyclic factor,
        such as the days of the week or the time intervals during which the factor operates.

        Args:
            useConfig (CyclicBaseUseConfig): The new usage configuration to apply.
        """
        self._useConfig=useConfig

