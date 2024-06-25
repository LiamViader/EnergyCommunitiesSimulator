from Profiles.LoadFactors.loadFactor import LoadFactor
from Profiles.profileConfiguration import ProfileConfig
from utils.enums import LoadType
from Profiles.LoadFactors.SolarPanel.solarIrradiation import SolarIrradiation
import numpy as np
import pandas as pd
import math

class SolarPanel(LoadFactor):
    def __init__(self, name: str, productionCapacity: float, efficiency: float):
        super().__init__(name,LoadType.Producer)
        self.productionCapacity = productionCapacity #en kw, ja te en compte l'area del solar panel
        self.efficiency = efficiency


    def generate_load(self, profileConfig: ProfileConfig, solarIrradiation:SolarIrradiation) -> pd.Series:
        hoursPerIndex=24/profileConfig.num_indices()
        load=solarIrradiation.get_irradiation()*self.productionCapacity*self.efficiency*hoursPerIndex #en Kwh
        return pd.Series(load)

