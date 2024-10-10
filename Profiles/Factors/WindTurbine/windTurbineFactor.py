import numpy as np
from Profiles.Factors.baseFactor import BaseFactor
from Profiles.Factors.WindTurbine.windTurbineModel import WindTurbineModel
from Simulation.simulationConfiguration import SimulationConfig
from utils.enums import FactorType

class WindTurbineFactor(BaseFactor):
    """
    Represents a factor for simulating the energy production of a wind turbine.

    This class utilizes a specific wind turbine model to calculate the power generated 
    by the wind turbine over a simulation period, based on wind conditions.

    Attributes:
        _model (WindTurbineModel): The wind turbine model used for power generation calculations.
    
    Methods:
        simulate(simulationConfig: SimulationConfig) -> np.ndarray:
            Simulates the energy production of the wind turbine based on wind conditions.
    """
    def __init__(self, model:WindTurbineModel):
        """
        Initializes the WindTurbineFactor with a specified wind turbine model.

        Args:
            model (WindTurbineModel): The wind turbine model to be used for simulations.
        """
        super().__init__(model.get_name(), FactorType.Producer)
        self._model=model
    
    def simulate(self, simulationConfig: SimulationConfig) -> np.ndarray:
        """
        Simulates the energy production of the wind turbine based on wind conditions.

        Args:
            simulationConfig (SimulationConfig): The configuration settings for the simulation

        Returns:
            np.ndarray: An array containing the energy produced by the wind turbine for each time step of the day.
        """
        load=np.zeros(simulationConfig.num_indices())
        hoursPerIndex=24/simulationConfig.num_indices()
        wind=simulationConfig.get_wind()
        for i in range(simulationConfig.num_indices()):
            power=self._model.get_power(wind[i])
            load[i]+=power*hoursPerIndex
        return load
    
