import numpy as np
from Profiles.Factors.baseFactor import BaseFactor
from Profiles.Factors.WindTurbine.windTurbineModel import WindTurbineModel
from Profiles.profileConfiguration import ProfileConfig
from utils.enums import FactorType

class WindTurbineFactor(BaseFactor):
    def __init__(self, model:WindTurbineModel):
        super().__init__(model.get_name(), FactorType.Producer)
        self.model=model
    
    def simulate(self, profileConfig: ProfileConfig) -> np.ndarray:
        load=np.zeros(profileConfig.num_indices())
        hoursPerIndex=24/profileConfig.num_indices()
        wind=profileConfig.get_wind()
        for i in range(profileConfig.num_indices()):
            power=self.model.get_power(wind[i])
            load[i]+=power*hoursPerIndex
        return load
    
