from numpy import ndarray
from Profiles.Factors.baseFactor import BaseFactor
from Profiles.profileConfiguration import ProfileConfig
from utils.enums import FactorType
from typing import List
from Profiles.Factors.Climatitzation.Components.climatitzationComponent import ClimatitzationComponent
from Profiles.Factors.Climatitzation.thermostat import Thermostat
import numpy as np

class ClimatitzationFactor(BaseFactor):
    def __init__(self,name:str,climatitzationComponents:List[ClimatitzationComponent],thermostat:Thermostat) -> None:
        super().__init__(name, FactorType.Consumer)
        self.climatitzationComponents=climatitzationComponents
        self.thermostat=thermostat
    
    def simulate(self, profileConfig: ProfileConfig) -> ndarray:
        load=np.zeros(profileConfig.num_indices())
        minutesPerIndex=1440/profileConfig.num_indices()
        for i in range(profileConfig.num_indices()):
            currentInsideTemp=self.thermostat.get_current_temperature()
            currentInsideTemp+=profileConfig.outside_termic_response(currentInsideTemp,minutesPerIndex*i,minutesPerIndex)
            self.thermostat.set_current_temperature(currentInsideTemp)
            idealTemperature=self.thermostat.get_ideal_temperature(minutesPerIndex*i)
            indexLoad=0
            for climatitzationComponent in self.climatitzationComponents:
                hoursElapsed=minutesPerIndex/60
                componentLoad,currentInsideTemp= climatitzationComponent.climatize(thermostat=self.thermostat,idealTemperature=idealTemperature,timeElapsed=hoursElapsed)
                indexLoad+=componentLoad
            load[i]=indexLoad
        return load