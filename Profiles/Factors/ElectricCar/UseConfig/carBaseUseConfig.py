from abc import ABC, abstractmethod
from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution
from typing import Tuple, List
import numpy as np
import pandas as pd

class CarBaseUseConfig(ABC):
    """
    Abstract base class for defining electric car usage configuration.

    This class models the typical daily usage of an electric car across the days of the week, where each day can have different usage patterns. 
    It provides an interface to define how the car charges based on the current charge level and the day of the week.

    Attributes:
        dailyUsage (Tuple[BaseNumberDistribution, BaseNumberDistribution, BaseNumberDistribution,
                          BaseNumberDistribution, BaseNumberDistribution, BaseNumberDistribution,
                          BaseNumberDistribution]): 
            A tuple of distributions representing average kilometers driven each day of the week.

    Methods:
        get_charge_usage(chargeLevel: float, weekDay: int) -> Tuple[float, float]:
            Abstract method to return the charging configuration based on the current charge level and the day of the week.
        get_usage_at_day(day: int) -> List[float]:
            Returns the car's usage for a given day of the week.
    """
    def __init__(self,dailyUsage: Tuple[BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution]):
        """
        Initializes the CarBaseUseConfig with daily usage distributions.

        Args:
            dailyUsage (Tuple[BaseNumberDistribution, BaseNumberDistribution, BaseNumberDistribution,
                          BaseNumberDistribution, BaseNumberDistribution, BaseNumberDistribution,
                          BaseNumberDistribution]): 
                List of BaseNumberDistribution objects, each representing a different day of the week car usage in kilometers.
        """
        self.dailyUsage = dailyUsage 
    
    @abstractmethod
    def get_charge_usage(self,chargeLevel:float,weekDay:int)->Tuple[float,float]:
        """
        Abstract method to return the charging configuration.

        This method must be implemented by subclasses. It should calculate when the car will start charging and for how long based on the charge level and day of the week.

        Args:
            chargeLevel (float): Current charge level of the battery, after daily usage has been deducted.
            weekDay (int): The current day of the week (0 for Monday, 6 for Sunday).

        Returns:
            Tuple[float, float]: Start time (hours) and charging duration (hours).
        """
        pass
    
    def get_usage_at_day(self, day:int)->List[float]:
        """
        Returns the car's usage for a given day of the week.

        This method generates a random number of kilometers driven based on the daily usage distribution for the given day.

        Args:
            day (int): Day of the week (0 for Monday, 6 for Sunday).

        Returns:
            float: The number of kilometers driven that day.
        """
        return self.dailyUsage[day].generate_random()