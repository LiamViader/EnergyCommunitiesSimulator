from typing import Tuple
from Profiles.Factors.Climatitzation.Components.climatitzationComponent import ClimatitzationComponent
from Profiles.Factors.Climatitzation.thermostat import Thermostat

class Heating(ClimatitzationComponent):
    """
    Represents a heating climatization component that adjusts the temperature of a space.

    This class extends the ClimatitzationComponent and provides an implementation 
    for the climatization process using heating power. It calculates the energy 
    required to heat a volume of air based on the difference between the current 
    temperature and the ideal temperature.

    Attributes:
        _maxPower (float): Maximum power of the heating system in kilowatts (kW).

        _minPower (float): Minimum power of the heating system in kilowatts (kW).

        _efficiency (float): Efficiency of the heating system.
        
        _volume (float): Volume of the space being heated in cubic meters (m³).

    Methods:
        climatize(thermostat: Thermostat, idealTemperature: float, timeElapsed: float) -> Tuple[float, float]:
            Climatizes the space towards the ideal temperature over a specified time.
    """
    def __init__(self, maxPower: float, minPower:float, efficiency: float, volume: float):
        """
        Initializes the Heating component with specified power, efficiency, and volume.

        Args:
            maxPower (float): Maximum power of the heating system in kilowatts (kW).
            minPower (float): Minimum power of the heating system in kilowatts (kW).
            efficiency (float): Efficiency of the heating system.
            volume (float): Volume of the space to be heated in cubic meters (m³).
        """
        self._maxPower= maxPower 
        self._minPower= minPower
        self._efficiency = efficiency  
        self._volume = volume  
    
    def climatize(self, thermostat:Thermostat,idealTemperature:float,timeElapsed:float) -> Tuple[float, float]:
        """
        Climatizes the space towards the ideal temperature over a specified time period.

        This method calculates the energy load required to adjust the temperature 
        towards the ideal level during the specified time elapsed.

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
                for heating, and the second element is the new temperature (in degrees Celsius).
        """
        if idealTemperature is not None:
            tempDiff = idealTemperature - thermostat.get_current_temperature()
            if tempDiff > 0:
                # Calculate the power to use, considering the temperature difference
                powerToUse = max(min(self._maxPower, self._maxPower * (tempDiff / 5)), self._minPower)
                
                # Calculate the energy load required in kWh
                load = powerToUse * timeElapsed
                
                # Adjust the load by the efficiency of the heater
                effectiveLoad = load * self._efficiency
                
                # Convert kWh to Joules (1 kWh = 3.6e6 Joules)
                joules = effectiveLoad * 3.6e6
                
                # Calculate the mass of the air (density of air = 1.225 kg/m³)
                mass = self._volume * 1.225
                
                # Calculate the temperature increase in °C
                deltaTemp = joules / (mass * 1005)
                
                # Ensure we don't overshoot the ideal temperature
                newTemperature = min(deltaTemp + thermostat.get_current_temperature(), idealTemperature)
                
                # Calculate the actual energy needed to reach the ideal temperature
                joulesOfTempDiff = tempDiff * mass * 1005
                actualLoad = min(effectiveLoad, joulesOfTempDiff / 3.6e6)  # Convert Joules back to kWh
                
                thermostat.set_current_temperature(newTemperature)
                return actualLoad, newTemperature
            
        return 0, thermostat.get_current_temperature()

