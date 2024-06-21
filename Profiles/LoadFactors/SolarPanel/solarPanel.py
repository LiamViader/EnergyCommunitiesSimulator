from Profiles.LoadFactors.loadFactor import LoadFactor
from Profiles.loadConfiguration import LoadConfig
from utils.enums import LoadType
from Profiles.LoadFactors.SolarPanel.solarIrradiation import SolarIrradiation
import numpy as np
import pandas as pd
import math

class SolarPanel(LoadFactor):
    def __init__(self, name: str, productionCapacity: float, efficiency: float):
        super().__init__(name,LoadType.Producer)
        self.productionCapacity = productionCapacity
        self.efficiency = efficiency


    def generate_load(self, loadConfig: LoadConfig, solarIrradiation:SolarIrradiation) -> pd.Series:
        load = np.zeros(loadConfig.num_indices())
        minutesPerIndex=1440/loadConfig.num_indices()
        for i in range(loadConfig.num_indices()):
            power=self.productionCapacity*self.efficiency*solarIrradiation.irradiate(i*minutesPerIndex)#power en kiloWatts
            load[i]+=power*(minutesPerIndex/60)
        return pd.Series(load)

