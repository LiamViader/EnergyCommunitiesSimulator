from Profiles.LoadFactors.loadFactor import LoadFactor
from Profiles.profileConfiguration import ProfileConfig
from utils.enums import LoadType
from Profiles.LoadFactors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.LoadFactors.SolarPanel.solarPanel import SolarPanel
from typing import List
import numpy as np
import pandas as pd
import math


class SolarPV(LoadFactor):
    def __init__(self, name: str, solarPanels:List[SolarPanel]):
        super().__init__(name, LoadType.Producer)
        self.solarPanels=solarPanels
    
    def generate_load(self, profileConfig: ProfileConfig, solarIrradiation:SolarIrradiation) -> pd.Series:
        totalLoad = pd.Series(np.zeros(profileConfig.num_indices()))
        for solarPanel in self.solarPanels:
            panelLoad=solarPanel.generate_load(profileConfig=profileConfig,solarIrradiation=solarIrradiation)
            totalLoad+=panelLoad
        return totalLoad