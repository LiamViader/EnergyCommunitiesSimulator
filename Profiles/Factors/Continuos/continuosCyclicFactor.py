import pandas as pd
import numpy as np
import random
from typing import Tuple
from Profiles.Factors.baseFactor import BaseFactor
from Simulation.simulationConfiguration import SimulationConfig
from Profiles.Factors.Continuos.continuosCyclicModel import ContinuosCyclicModel
from utils.enums import FactorType

class ContinuosCyclicFactor(BaseFactor):
    """
    A class representing a continuously operating factor with cyclic energy usage.

    This class models a device or process that alternates between active and idle states, consuming energy in cycles
    throughout the day (e.g. Freezer,Refrigerator...). The energy consumption is distributed over time intervals, and any overflow from cycles
    that extend beyond the current simulation day is carried over to the next simulation day.

    Attributes:
        _model (ContinuosCyclicModel): The model that defines the cyclic behavior of the factor (e.g., power usage, cycle duration, idle times).

        _overflowTime (float): Tracks any remaining time from the last cycle that spills into the next simulation day.

        _overflowPower (float): Tracks the power used during the overflow time.
        
        _idle (bool): Indicates whether the factor is in an idle state (True) or an active state (False).

    Methods:
        simulate(simulationConfig: SimulationConfig) -> np.ndarray:
            Simulates the energy consumption over a day, alternating between active and idle cycles.
    """
    def __init__(self, model:ContinuosCyclicModel):
        """
        Initializes a ContinuosCyclicFactor instance.

        Args:
            model (ContinuosCyclicModel): The model representing the cyclic energy behavior (e.g., Freezer,Refrigerator,...).
        """
        super().__init__(model.get_name(), FactorType.Consumer)
        self._model=model
        self._overflowTime=0
        self._overflowPower=0
        self._idle=True

    def simulate(self, simulationConfig: SimulationConfig) -> np.ndarray:
        """
        Simulates the energy consumption of the factor over a single day.

        The method alternates between active and idle cycles, distributing the power consumption for each cycle across
        the time intervals specified in the simulation configuration.

        Args:
            simulationConfig (SimulationConfig): Configuration object defining the simulation parameters, 
                                                 such as the number of time intervals per day.

        Returns:
            np.ndarray: An array representing the energy consumption (in kWh) for each time interval in a day based on granularity.
        """
        load=np.zeros(simulationConfig.num_indices())
        self._distribute_cycle_load(self._overflowPower,0,self._overflowTime,simulationConfig,load)
        timeElapsed=self._overflowTime
        while timeElapsed<24.0:
            if self._idle:
                cycleDurationTime=self._model.get_time_between_next_cycle()
                power=self._model.get_idle_power()
            else:
                cycleDurationTime=self._model.get_cycle_duration()
                power=self._model.get_active_power()+self._model.get_idle_power()
            nextCycleTimestamp=cycleDurationTime+timeElapsed
            self._distribute_cycle_load(power,timeElapsed,nextCycleTimestamp,simulationConfig,load)
            timeElapsed=nextCycleTimestamp
            self._idle=not self._idle
        return load

    def _distribute_cycle_load(self,power:float,start:float,end:float,simulationConfig:SimulationConfig,load:np.ndarray):
        """
        Distributes the energy load for a cycle across the specified time intervals.

        Args:
            power (float): The power used during the cycle (in kW).
            start (float): The start time of the cycle (in hours).
            end (float): The end time of the cycle (in hours).
            simulationConfig (SimulationConfig): Configuration object defining the simulation parameters, 
                                                 including the number of time intervals.
            load (np.ndarray): The array representing the energy load for each time interval in the day.
        """
        indicesPerHour=simulationConfig.num_indices()/24
        startIndex=int(start*indicesPerHour)
        endIndex=int(end*indicesPerHour)
        timestamp=start
        i=startIndex
        while i<=endIndex and i<simulationConfig.num_indices():
            nextIndex=i+1
            nextIndexTimestamp=nextIndex/indicesPerHour
            if i!=endIndex:
                load[i]+=power*(nextIndexTimestamp-timestamp)
            else:
                load[i]+=power*(end-timestamp)
            timestamp=nextIndexTimestamp
            i=nextIndex
        if endIndex>=simulationConfig.num_indices():
            self._overflowTime=end-timestamp
            self._overflowPower=power