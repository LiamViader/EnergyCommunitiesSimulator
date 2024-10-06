import random
from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution

class CyclicModel():
    """
    Class representing a cyclic energy-consuming model, such as an appliance that follows a regular cycle (e.g., washing machine).

    This class models the behavior of appliances that have a regular operation cycle, including active power during cycles,
    standby power consumption, and the duration of these states.

    Attributes:
        _name (str): Name of the cyclic model.
        _cyclePower (BaseNumberDistribution): Distribution that defines the average power consumed during the cycle.
        _cycleTime (BaseNumberDistribution): Distribution that defines the duration of each cycle (in hours).
        _standByPower (BaseNumberDistribution): Distribution that defines the power consumed during standby mode.
        _standByTime (float): The average amount of time (in hours) that the model spends in standby mode per day.

    Methods:
        get_cycle_power() -> float: Returns a random value for the average cycle power.
        get_cycle_minutes() -> float: Returns a random value for the cycle duration in minutes.
        get_stand_by_power() -> float: Returns the standby power, based on probability and the standby time.
        get_name() -> str: Returns the name of the cyclic model.
    """
    def __init__(self,name:str,
                 cyclePower:BaseNumberDistribution, 
                 cycleTime:BaseNumberDistribution, 
                 standByPower:BaseNumberDistribution,
                 standByTime:float
                 ):
        """
        Initializes a CyclicModel instance with the given parameters.

        Args:
            name (str): Name of the cyclic model.
            cyclePower (BaseNumberDistribution): A distribution representing the average power consumed during each cycle (in kW).
            cycleTime (BaseNumberDistribution): A distribution representing the duration of each cycle (in hours).
            standByPower (BaseNumberDistribution): A distribution representing the power consumed while in standby (in kW).
            standByTime (float): Average time (in hours) spent in standby mode per day.
        """
        self._name=name
        self._cyclePower=cyclePower
        self._cycleTime=cycleTime 
        self._standByPower=standByPower 
        self._standByTime=standByTime 

    def get_cycle_power(self):
        """
        Retrieves the average power consumption during the active cycle, generated randomly based on the power distribution.

        Returns:
            float: The average power consumed during the cycle (in kW).
        """
        return self._cyclePower.generate_random()

    def get_cycle_minutes(self): 
        """
        Retrieves the duration of the active cycle, generated randomly from the cycle time distribution and converted to minutes.

        Returns:
            float: The duration of the cycle in minutes.
        """
        return self._cycleTime.generate_random()*60

    def get_stand_by_power(self):
        """
        Retrieves the power consumed during standby mode. This is determined based on the probability of the model
        being in standby, which is calculated from the standby time divided by 24 hours. If the model is in standby,
        the power is randomly generated from the standby power distribution.

        Returns:
            float: The standby power consumed (in kW), or 0 if not in standby.
        """
        probability=self._standByTime/24
        number=random.random()
        if number<probability:
            return self._standByPower.generate_random()
        else:
            return 0
    
    def get_name(self):
        """
        Retrieves the name of the cyclic model.

        Returns:
            str: The name of the cyclic model.
        """
        return self._name