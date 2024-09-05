from Profiles.Factors.baseFactor import BaseFactor
from Simulation.simulationConfiguration import SimulationConfig
from utils.enums import FactorType
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
import numpy as np
import pandas as pd
import math
from typing import Tuple

class SolarPanel(BaseFactor):
    def __init__(self, name: str, productionCapacity: float, efficiency: float):
        super().__init__(name,FactorType.Producer)
        self.productionCapacity = productionCapacity #en kw, ja te en compte l'area del solar panel
        self.efficiency = efficiency


    def simulate(self, simulationConfig: SimulationConfig) -> np.ndarray:
        hoursPerIndex=24/simulationConfig.num_indices()
        load=simulationConfig.get_irradiation()*self.productionCapacity*self.efficiency*hoursPerIndex #en kwh
        return load

