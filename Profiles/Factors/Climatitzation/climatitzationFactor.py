from numpy import ndarray
from Profiles.Factors.baseFactor import BaseFactor
from Simulation.simulationConfiguration import SimulationConfig
from utils.enums import FactorType
from typing import List
from Profiles.Factors.Climatitzation.Components.climatitzationComponent import ClimatitzationComponent
from Profiles.Factors.Climatitzation.thermostat import Thermostat
import numpy as np

class ClimatitzationFactor(BaseFactor):
    """
    A simulation factor that models the climatization of a space using various components and a thermostat.

    This class simulates the energy load required to maintain a desired internal temperature 
    based on external conditions and the specified climatization components.

    Attributes:
        _climatitzationComponents (List[ClimatitzationComponent]): List of climatization components used in the simulation.

        _thermostat (Thermostat): The thermostat controlling the temperature of the climatitzationFactor zone.

        _insideVolume (float): The volume of the space being climatized, in cubic meters.
            
        _exteriorContactArea (float): The area of the climatization assets zone that contacts the exterior, in square meters.

    Methods:
        simulate(simulationConfig: SimulationConfig) -> ndarray:
            Simulates the climatization process over the simulated day.
    """
    def __init__(self,name:str,climatitzationComponents:List[ClimatitzationComponent],thermostat:Thermostat,insideVolume:float=150,exteriorContactArea:float=50) -> None:
        """
        Initializes the ClimatitzationFactor with the given parameters.

        Args:
            name (str): 
                The name of the climatization factor.
            climatitzationComponents (List[ClimatitzationComponent]): 
                List of climatization components used in the simulation.
            thermostat (Thermostat): 
                The thermostat controlling the temperature.
            insideVolume (float, optional): 
                The volume affected by the climatization assets, default is 150 cubic meters.
            exteriorContactArea (float, optional): 
                The area of the climatization assets zone that contacts the exterior, default is 50 square meters.
        """
        super().__init__(name, FactorType.Consumer)
        self._climatitzationComponents=climatitzationComponents
        self._thermostat=thermostat
        self._insideVolume=insideVolume 
        self._exteriorContactArea=exteriorContactArea 
    
    def simulate(self, simulationConfig: SimulationConfig) -> ndarray:
        """
        Simulates the climatization process over the specified simulation day.

        This method calculates the energy load required at each time step based on the current 
        and ideal temperatures, as well as the external temperature response.

        Args:
            simulationConfig (SimulationConfig): 
                Configuration of the current simulation.

        Returns:
            ndarray: 
                Array representing the energy load required for climatization during each 
                simulation time step of the day.
        """
        load=np.zeros(simulationConfig.num_indices())
        minutesPerIndex=1440/simulationConfig.num_indices()
        for i in range(simulationConfig.num_indices()):
            currentInsideTemp=self._thermostat.get_current_temperature()
            currentInsideTemp+=simulationConfig.outside_termic_response(currentInsideTemp,minutesPerIndex*i,minutesPerIndex,self._exteriorContactArea,self._insideVolume)
            self._thermostat.set_current_temperature(currentInsideTemp)
            idealTemperature=self._thermostat.get_ideal_temperature(minutesPerIndex*i)
            indexLoad=0
            for climatitzationComponent in self._climatitzationComponents:
                hoursElapsed=minutesPerIndex/60
                componentLoad,currentInsideTemp= climatitzationComponent.climatize(thermostat=self._thermostat,idealTemperature=idealTemperature,timeElapsed=hoursElapsed)
                indexLoad+=componentLoad
            load[i]=indexLoad
        return load