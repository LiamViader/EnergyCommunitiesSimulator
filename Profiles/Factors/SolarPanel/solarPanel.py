from Profiles.Factors.baseFactor import BaseFactor
from Profiles.profileConfiguration import ProfileConfig
from utils.enums import FactorType
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
import numpy as np
import pandas as pd
import math

class SolarPanel(BaseFactor):
    def __init__(self, name: str, productionCapacity: float, efficiency: float):
        super().__init__(name,FactorType.Producer)
        self.productionCapacity = productionCapacity #en kw, ja te en compte l'area del solar panel
        self.efficiency = efficiency


    def simulate(self, profileConfig: ProfileConfig, solarIrradiation:SolarIrradiation) -> pd.Series:
        power=solarIrradiation.get_irradiation()*self.productionCapacity*self.efficiency #en kw
        return pd.Series(power)

