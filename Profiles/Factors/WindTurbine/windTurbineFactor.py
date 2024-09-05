import numpy as np
from Profiles.Factors.baseFactor import BaseFactor
from Profiles.Factors.WindTurbine.windTurbineModel import WindTurbineModel
from Simulation.simulationConfiguration import SimulationConfig
from utils.enums import FactorType

class WindTurbineFactor(BaseFactor):
    def __init__(self, model:WindTurbineModel):
        super().__init__(model.get_name(), FactorType.Producer)
        self.model=model
    
    def simulate(self, simulationConfig: SimulationConfig) -> np.ndarray:
        load=np.zeros(simulationConfig.num_indices())
        hoursPerIndex=24/simulationConfig.num_indices()
        wind=simulationConfig.get_wind()
        for i in range(simulationConfig.num_indices()):
            power=self.model.get_power(wind[i])
            load[i]+=power*hoursPerIndex
        return load
    
