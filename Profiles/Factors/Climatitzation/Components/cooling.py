from typing import Tuple
from Profiles.Factors.Climatitzation.Components.climatitzationComponent import ClimatitzationComponent
from Profiles.Factors.Climatitzation.thermostat import Thermostat

class Cooling(ClimatitzationComponent):
    def __init__(self, maxPower: float, minPower:float, efficiency: float, volume: float):
        self.maxPower= maxPower #max power of cooling in kw
        self.minPower= minPower
        self.efficiency = efficiency  #heating efficiency
        self.volume = volume  #volume that has to cool
    
    def climatize(self, thermostat:Thermostat,idealTemperature:float,timeElapsed:float) -> Tuple[float, float]:#timeElapsed en hores
        if idealTemperature is not None:
            tempDiff = idealTemperature - thermostat.get_current_temperature()
            if tempDiff < 0:
                tempDiff=abs(tempDiff)
                # Calculate the power to use, considering the temperature difference
                powerToUse = max(min(self.maxPower, self.maxPower * (tempDiff / 5)), self.minPower)
                
                # Calculate the energy load required in kWh
                load = powerToUse * timeElapsed
                
                # Adjust the load by the efficiency of the cooler
                effectiveLoad = load * self.efficiency
                
                # Convert kWh to Joules (1 kWh = 3.6e6 Joules)
                joules = effectiveLoad * 3.6e6
                
                # Calculate the mass of the air (density of air = 1.225 kg/m³)
                mass = self.volume * 1.225
                
                # Calculate the temperature increase in °C
                deltaTemp = joules / (mass * 1005)
                
                # Ensure we don't overshoot the ideal temperature
                newTemperature = max(thermostat.get_current_temperature()-deltaTemp, idealTemperature)
                
                # Calculate the actual energy needed to reach the ideal temperature
                joulesOfTempDiff = tempDiff * mass * 1005
                actualLoad = min(effectiveLoad, joulesOfTempDiff / 3.6e6)  # Convert Joules back to kWh
                
                thermostat.set_current_temperature(newTemperature)
                return actualLoad, newTemperature
            
        return 0, thermostat.get_current_temperature()

