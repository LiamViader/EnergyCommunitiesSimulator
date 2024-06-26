from Profiles.Factors.baseFactor import BaseFactor
from Profiles.profileConfiguration import ProfileConfig
from utils.enums import FactorType
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.Factors.SolarPanel.solarPanel import SolarPanel
from typing import List
import numpy as np
import pandas as pd
import math


class SolarPV(BaseFactor):
    def __init__(self, name: str, solarPanels:List[SolarPanel]):
        super().__init__(name, FactorType.Producer)
        self.solarPanels=solarPanels
    
    def simulate(self, profileConfig: ProfileConfig, solarIrradiation:SolarIrradiation) -> pd.Series:
        totalPower = pd.Series(np.zeros(profileConfig.num_indices()))
        for solarPanel in self.solarPanels:
            panelPower=solarPanel.simulate(profileConfig=profileConfig,solarIrradiation=solarIrradiation)
            totalPower+=panelPower
        return totalPower