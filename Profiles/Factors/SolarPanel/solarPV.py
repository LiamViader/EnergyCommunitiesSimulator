from Profiles.Factors.baseFactor import BaseFactor
from Simulation.simulationConfiguration import SimulationConfig
from utils.enums import FactorType
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.Factors.SolarPanel.solarPanel import SolarPanel
from typing import List
import numpy as np
import pandas as pd
import math
from typing import Tuple


class SolarPV(BaseFactor):
    def __init__(self, name: str, solarPanels:List[SolarPanel]):
        super().__init__(name, FactorType.Producer)
        self._solarPanels=solarPanels
    
    def simulate(self, simulationConfig: SimulationConfig) -> np.ndarray:
        totalLoad = pd.Series(np.zeros(simulationConfig.num_indices()))
        for solarPanel in self._solarPanels:
            panelLoad=solarPanel.simulate(simulationConfig=simulationConfig)
            totalLoad+=panelLoad
        return totalLoad