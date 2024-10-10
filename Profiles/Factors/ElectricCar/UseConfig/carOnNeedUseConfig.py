from typing import List, Tuple
from utils.minuteInterval import MinuteInterval
from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution
from Profiles.Factors.ElectricCar.UseConfig.carBaseUseConfig import CarBaseUseConfig
from Profiles.Factors.ElectricCar.electricCarModel import ElectricCarModel

class CarOnNeedUseConfig(CarBaseUseConfig):
    """
    Defines the charging behavior of an electric car based on its battery level,
    a battery threshold when the user starts charging, and predefined time intervals of charging. 
    This class models the behaviour of a user that fully charges the vehicle when the battery level 
    drops below a threshold. The time when the user starts charging its predefined by the chargeIntervals

    Attributes:
        dailyUsage (Tuple[BaseNumberDistribution, BaseNumberDistribution, BaseNumberDistribution,
                    BaseNumberDistribution, BaseNumberDistribution, BaseNumberDistribution,
                    BaseNumberDistribution]): 
        Distribution of kilometers driven each day.

        chargeIntervals (Tuple[MinuteInterval, MinuteInterval, MinuteInterval, MinuteInterval,
                        MinuteInterval, MinuteInterval, MinuteInterval]): 
        Charging intervals for each day of the week. Represents the time interval when the
        car user usually starts the charging of the EV.

        batteryThreshold (float): Threshold battery level (0-1) below which the car starts charging.
    Methods:
        get_charge_usage(chargeLevel: float, weekDay: int) -> Tuple[float, float]:
            Returns the start time and duration of charging in hours.
            The chargeLevel should have been reduced previously according to the kilometers driven that day.
    """
    def __init__(self, dailyUsage: Tuple[BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution], chargeIntervals: Tuple[MinuteInterval,MinuteInterval,MinuteInterval,MinuteInterval,MinuteInterval,MinuteInterval,MinuteInterval], batteryThreshold: float):
        """
        Initializes the CarOnNeedUseConfig with daily usage, charging intervals, and a battery threshold.

        Args:
            dailyUsage (Tuple[BaseNumberDistribution, BaseNumberDistribution, BaseNumberDistribution,
                               BaseNumberDistribution, BaseNumberDistribution, BaseNumberDistribution,
                               BaseNumberDistribution]):
                Distributions of kilometers driven each day of the week.
            chargeIntervals (Tuple[MinuteInterval, MinuteInterval, MinuteInterval, MinuteInterval,
                                   MinuteInterval, MinuteInterval, MinuteInterval]):
                Charging intervals for each day of the week.
            batteryThreshold (float):
                Threshold battery level (0-1) below which the car starts charging.
        """
        super().__init__(dailyUsage)
        self._chargeIntervals = chargeIntervals 
        self._batteryThreshold = batteryThreshold  


    def get_charge_usage(self,chargeLevel:float,weekDay:int,model:ElectricCarModel)->Tuple[float,float]:
        """
        Returns the start time and duration of charging in hours.
        The chargeLevel should have been reduced previously according to the kilometers driven that day.

        Args:
            chargeLevel (float): Current battery level of the car.
            weekDay (int): Current day of the week (0-6).
            model (ElectricCarModel): The electric car model being used.

        Returns:
            Tuple[float, float]: Start time and duration of charging.
        """
        if chargeLevel>=(model.get_battery_capacity()*self._batteryThreshold): #no carregar
            return 0,0
        else:
            if self._chargeIntervals[weekDay] is None:
                return 0,0
            else:
                start=self._chargeIntervals[weekDay].random()/60
                energyToCharge=(model.get_battery_capacity()-chargeLevel)/model.get_charge_efficiency()
                duration=energyToCharge/model.get_charge_power()
                return start, duration