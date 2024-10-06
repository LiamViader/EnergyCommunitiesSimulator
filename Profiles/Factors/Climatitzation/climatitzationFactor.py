from numpy import ndarray
from Profiles.Factors.baseFactor import BaseFactor
from Simulation.simulationConfiguration import SimulationConfig
from utils.enums import FactorType
from typing import List
from Profiles.Factors.Climatitzation.Components.climatitzationComponent import ClimatitzationComponent
from Profiles.Factors.Climatitzation.thermostat import Thermostat
import numpy as np

class ClimatitzationFactor(BaseFactor):
    def __init__(self,name:str,climatitzationComponents:List[ClimatitzationComponent],thermostat:Thermostat,insideVolume:float=150,exteriorContactArea:float=50) -> None:
        super().__init__(name, FactorType.Consumer)
        self._climatitzationComponents=climatitzationComponents
        self._thermostat=thermostat
        self._insideVolume=insideVolume #volume affected by the climatitzationAsset
        self._exteriorContactArea=exteriorContactArea #the area of the climatitzationAsset insideVolume that contacts exterior
    
    def simulate(self, simulationConfig: SimulationConfig) -> ndarray:
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