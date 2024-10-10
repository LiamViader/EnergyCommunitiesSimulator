from Profiles.Factors.baseFactor import BaseFactor
from Simulation.simulationConfiguration import SimulationConfig
from utils.enums import FactorType
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.Factors.SolarPanel.solarPanel import SolarPanel
from typing import List
import numpy as np
import pandas as pd
import math
from typing import Tuple


class SolarPV(BaseFactor):
    """
    Represents a solar photovoltaic (PV) system consisting of multiple solar panels.

    This class aggregates the energy production from multiple solar panels and provides a 
    simulation of the total energy output based on solar irradiation data.

    Attributes:
        _solarPanels (List[SolarPanel]): A list of SolarPanel instances representing the solar panels in the system.

    Methods:
        simulate(simulationConfig: SimulationConfig) -> np.ndarray:
            Simulates the total energy production of the solar PV system for the simulation day.
    """
    def __init__(self, name: str, solarPanels:List[SolarPanel]):
        """
        Initializes a SolarPV instance with the given parameters.

        Args:
            name (str): The name of the solar PV system.
            solarPanels (List[SolarPanel]): A list of SolarPanel instances that make up the solar PV system.
        """
        super().__init__(name, FactorType.Producer)
        self._solarPanels=solarPanels
    
    def simulate(self, simulationConfig: SimulationConfig) -> np.ndarray:
        """
        Simulates the total energy production of the solar PV system for the day.

        The total energy output is calculated by summing the energy production of each individual solar panel.

        Args:
            simulationConfig (SimulationConfig): The configuration object containing solar irradiation data.

        Returns:
            np.ndarray: An array containing the simulated total energy production values for each step of the day in kWh.
        """
        totalLoad = pd.Series(np.zeros(simulationConfig.num_indices()))
        for solarPanel in self._solarPanels:
            panelLoad=solarPanel.simulate(simulationConfig=simulationConfig)
            totalLoad+=panelLoad
        return totalLoad