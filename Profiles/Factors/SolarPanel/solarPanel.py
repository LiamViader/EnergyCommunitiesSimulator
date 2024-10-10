from Profiles.Factors.baseFactor import BaseFactor
from Simulation.simulationConfiguration import SimulationConfig
from utils.enums import FactorType
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
import numpy as np
import pandas as pd
import math
from typing import Tuple

class SolarPanel(BaseFactor):
    """
    Represents a solar panel system that simulates energy production based on solar irradiation.

    This class calculates the energy output of a solar panel based on its production capacity and efficiency
    in conjunction with the solar irradiation data provided through the simulation configuration.

    Attributes:
        _productionCapacity (float): The maximum power output of the solar panel in kilowatts (kW).
        
        _efficiency (float): The efficiency of the solar panel as a fraction (0 < efficiency < 1).

    Methods:
        simulate(simulationConfig: SimulationConfig) -> np.ndarray:
            Simulates the energy production of the solar panel for a simulation day.
    """
    def __init__(self, name: str, productionCapacity: float, efficiency: float):
        """
        Initializes a SolarPanel instance with the given parameters.

        Args:
            name (str): The name of the solar panel.
            productionCapacity (float): The maximum power output of the solar panel in kilowatts (kW).
            efficiency (float): The efficiency of the solar panel (0 < efficiency < 1).
        """
        super().__init__(name,FactorType.Producer)
        self._productionCapacity = productionCapacity 
        self._efficiency = efficiency


    def simulate(self, simulationConfig: SimulationConfig) -> np.ndarray:
        """
        Simulates the energy production of the solar panel for the simulation day.

        The energy output is calculated based on the solar irradiation data, production capacity, efficiency,
        and the number of time steps of the day.

        Args:
            simulationConfig (SimulationConfig): The configuration object containing solar irradiation data.

        Returns:
            np.ndarray: An array containing the simulated energy production values for each time step of the day in kWh.
        """
        hoursPerIndex=24/simulationConfig.num_indices()
        load=simulationConfig.get_irradiation()*self._productionCapacity*self._efficiency*hoursPerIndex
        return load

