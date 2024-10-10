from abc import ABC, abstractmethod
from typing import Tuple
from Profiles.Factors.Climatitzation.thermostat import Thermostat

class ClimatitzationComponent(ABC):
    """
    Abstract base class for climatization components.

    This class serves as a blueprint for all climatization components that will 
    interact with a thermostat to achieve the desired indoor temperature. 
    Each component must implement its specific climatization behavior.

    Methods:
        climatize(thermostat: Thermostat, idealTemperature: float, timeElapsed: float) -> Tuple[float, float]:
            Abstract method to climatize towards the ideal temperature over a specified time.
    """
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def climatize(self,thermostat:Thermostat,idealTemperature:float,timeElapsed:float)->Tuple[float,float]:
        """
        Climatizes the space towards the ideal temperature over a specified time period.

        This method must be implemented by subclasses. It calculates the energy load 
        required to adjust the temperature towards the ideal level during the specified 
        time elapsed.

        Args:
            thermostat (Thermostat): 
                The thermostat controlling the climatization process.
            idealTemperature (float): 
                The desired temperature to reach.
            timeElapsed (float): 
                The time duration over which to climatize, in hours.

        Returns:
            Tuple[float, float]: 
                A tuple where the first element is the energy load (in kWh) required 
                for climatization, and the second element is the temperature.
                (in degrees Celsius).
        """
        pass