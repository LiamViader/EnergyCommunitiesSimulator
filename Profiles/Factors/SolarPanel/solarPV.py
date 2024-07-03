from Profiles.Factors.baseFactor import BaseFactor
from Profiles.profileConfiguration import ProfileConfig
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
        self.solarPanels=solarPanels
    
    def simulate(self, profileConfig: ProfileConfig) -> Tuple[pd.Series,pd.Series]:
        totalLoad = pd.Series(np.zeros(profileConfig.num_indices()))
        for solarPanel in self.solarPanels:
            panelLoad,_=solarPanel.simulate(profileConfig=profileConfig)
            totalLoad+=panelLoad
        return totalLoad, None