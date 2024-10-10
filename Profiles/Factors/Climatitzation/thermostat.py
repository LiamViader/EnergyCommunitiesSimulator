from typing import List, Tuple
from utils.minuteInterval import MinuteInterval

class Thermostat:
    """
    Represents a thermostat that controls the temperature settings for a space.

    The thermostat maintains the current temperature and allows for the retrieval of ideal temperature settings 
    based on specific time intervals throughout the day. 

    Attributes:
        _currentTemperature (float): The current temperature of the space.

        _idealTemperatures (List[Tuple[MinuteInterval, float]]):  A list of tuples where each tuple consists of a MinuteInterval and the corresponding ideal temperature.
    
    Methods:
        get_current_temperature() -> float:
            Returns the current temperature of the space.
        
        set_current_temperature(newTemp: float) -> None:
            Sets a new current temperature for the thermostat.
        
        get_ideal_temperature(timestamp: int) -> float:
            Returns the ideal temperature for the given timestamp.
    """
    def __init__(self,idealTemperatures:List[Tuple[MinuteInterval,float]],startingTemperature:float=21) -> None:
        """
        Initializes the thermostat with ideal temperature settings and an optional starting temperature.

        Args:
            idealTemperatures (List[Tuple[MinuteInterval, float]]): 
                A list of tuples containing MinuteIntervals and the ideal temperatures during those intervals.
            startingTemperature (float, optional): 
                The initial temperature of the space. Defaults to 21 degrees Celsius.
        """
        self._currentTemperature=startingTemperature
        self._idealTemperatures=idealTemperatures

    def get_current_temperature(self)->float:
        """
        Returns the current temperature of the space.

        Returns:
            float: The current temperature in degrees Celsius.
        """
        return self._currentTemperature
    
    def set_current_temperature(self,newTemp)->None:
        """
        Sets a new current temperature for the thermostat.

        Args:
            newTemp (float): The new temperature to be set in degrees Celsius.
        """
        self._currentTemperature=newTemp

    def get_ideal_temperature(self,timestamp)->float:
        """
        Returns the ideal temperature for the given timestamp.

        Args:
            timestamp (int): The timestamp for which the ideal temperature is requested.

        Returns:
            float: The ideal temperature in degrees Celsius for the specified timestamp.
        """
        for idealTemperatures in self._idealTemperatures:
            if idealTemperatures[0].contains(timestamp):
                return idealTemperatures[1]