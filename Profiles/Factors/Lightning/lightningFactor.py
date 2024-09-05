from Profiles.Factors.baseFactor import BaseFactor
from Simulation.simulationConfiguration import SimulationConfig
from Profiles.Factors.Lightning.lightningModel import LightningModel
from utils.enums import FactorType
from typing import List, Tuple
from utils.minuteInterval import MinuteInterval
import numpy as np
import pandas as pd

class LightningFactor(BaseFactor):
    def __init__(self, model: LightningModel,activityIntervals:List[Tuple[MinuteInterval,float]]):
        super().__init__(model.get_name(), FactorType.Consumer)
        self.model=model
        self.activityIntervals=activityIntervals


    def simulate(self, simulationConfig: SimulationConfig) -> np.ndarray:
        load=np.zeros(simulationConfig.num_indices())
        hoursPerIndex=24/simulationConfig.num_indices()
        irradiation=simulationConfig.get_irradiation()
        for i in range(simulationConfig.num_indices()):
            load[i]+=hoursPerIndex*self.get_power_at(hoursPerIndex*i,irradiation[i])
        return load
    
    def get_power_at(self,hour:float,irradiation:float)->float:
        maxPower=self.model.get_max_power()
        mean=0.5
        std=0.2
        maxIrradiation=1.1
        irradiationFactor=1-(irradiation/maxIrradiation)
        mean=mean*irradiationFactor
        activityFactor=0
        for activityInterval in self.activityIntervals:
            if activityInterval[0].contains(hour*60):
                activityFactor=activityInterval[1]
                break
        mean=mean*activityFactor
        std=std*activityFactor
        lightsProportionUsed=np.random.normal(mean, std)
        lightsProportionUsed=max(min(lightsProportionUsed,1),0)
        power=lightsProportionUsed*maxPower
        return power

        
