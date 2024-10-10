from Profiles.Factors.baseFactor import BaseFactor
from Simulation.simulationConfiguration import SimulationConfig
from Profiles.Factors.Lightning.lightningModel import LightningModel
from utils.enums import FactorType
from typing import List, Tuple
from utils.minuteInterval import MinuteInterval
import numpy as np
import pandas as pd

class LightningFactor(BaseFactor):
    """
    Represents the lightning load factor based on the given model and activity intervals.

    This class simulates the power consumption of lighting based on irradiation and specified activity intervals.

    Attributes:
        _model (LightningModel): The model that defines the characteristics of the lighting system.

        _activityIntervals (List[Tuple[MinuteInterval, float]]): A list of activity intervals and their respective amount of activity (0-1). Activity meaning how much active the residents are at home.
        Translating to how much they might be using lightning.

    Methods:
        simulate(simulationConfig: SimulationConfig) -> np.ndarray:
            Simulates the lighting load through the day.
    """
    def __init__(self, model: LightningModel,activityIntervals:List[Tuple[MinuteInterval,float]]):
        """
        Initializes a LightningFactor instance with the specified lighting model and activity intervals.

        Args:
            model (LightningModel): The model that defines the lighting characteristics.
            activityIntervals (List[Tuple[MinuteInterval, float]]): A list of tuples containing activity intervals
                Activity meaning how much active the residents are at home. Translating to how much they might be using lightning.
        """
        super().__init__(model.get_name(), FactorType.Consumer)
        self._model=model
        self._activityIntervals=activityIntervals


    def simulate(self, simulationConfig: SimulationConfig) -> np.ndarray:
        """
        Simulates the lighting load based on residents activity and irradiation.

        Args:
            simulationConfig (SimulationConfig): Configuration settings for the simulation.

        Returns:
            np.ndarray: An array of simulated energy consumption values for each time step of the day.
        """
        load=np.zeros(simulationConfig.num_indices())
        hoursPerIndex=24/simulationConfig.num_indices()
        irradiation=simulationConfig.get_irradiation()
        for i in range(simulationConfig.num_indices()):
            load[i]+=hoursPerIndex*self._get_power_at(hoursPerIndex*i,irradiation[i])
        return load
    
    def _get_power_at(self,hour:float,irradiation:float)->float:
        """
        Calculates the power consumption at a given hour based on irradiation and activity intervals.

        Args:
            hour (float): The hour for which the power consumption is calculated.
            irradiation (float): The irradiation value at the specified hour.

        Returns:
            float: The calculated power consumption at the specified hour.
        """
        maxPower=self._model.get_max_power()
        mean=0.5
        std=0.2
        maxIrradiation=1.1
        irradiationFactor=1-(irradiation/maxIrradiation)
        mean=mean*irradiationFactor
        activityFactor=0
        for activityInterval in self._activityIntervals:
            if activityInterval[0].contains(hour*60):
                activityFactor=activityInterval[1]
                break
        mean=mean*activityFactor
        std=std*activityFactor
        lightsProportionUsed=np.random.normal(mean, std)
        lightsProportionUsed=max(min(lightsProportionUsed,1),0)
        power=lightsProportionUsed*maxPower
        return power

        
