import pandas as pd
import numpy as np
from typing import List, Tuple, Optional, Dict
from Profiles.Factors.baseFactor import BaseFactor
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.Factors.SolarPanel.solarPV import SolarPV
from Profiles.Battery.batteriesManager import BatteriesManager
from utils.enums import Granularity
from utils.enums import FactorType
from EnergyPrice.EnergyPlans.baseEnergyPlan import BaseEnergyPlan
from Simulation.simulationConfiguration import SimulationConfig

class Profile:
    """
    A class representing an energy profile.

    This class simulates the energy consumption and production of a profile over a day, 
    using load factors and batteries if available. It also stores the profile's energy plan and
    detailed load calculations.

    Attributes:
        _idCounter (int): A class variable to generate unique IDs for each profile.

        _id (int): The unique identifier for the profile instance.

        _name (str): The name of the profile.

        _energyPlan (BaseEnergyPlan): The energy plan associated with this profile.

        _loadFactors (List[BaseFactor]): A list of factors that produce or consume energy used in the simulation.

        _batteries (BatteriesManager): The battery manager for the profile.

        _detailedLoad (Dict[BaseFactor, np.ndarray]): A dictionary mapping factors to their simulated energy arrays.
        
        _configLastSimulation (Optional[SimulationConfig]): The last simulation configuration used for the profile.

    Methods:
        simulate(simulationConfig: SimulationConfig) -> None:
            Simulates the energy consumed over time based on load factors and batteries.

        get_detailed_load() -> Dict[BaseFactor, np.ndarray]:
            Retrieves the detailed load for the profile.

        get_name() -> str:
            Retrieves the name of the profile.

        get_id() -> int:
            Retrieves the unique identifier of the profile.

        get_load_pv() -> Tuple[np.ndarray, np.ndarray]:
            Returns separate arrays for the load and production.

        get_combined_load_pv() -> Tuple[np.ndarray, np.ndarray]:
            Returns the combined load and PV production.

        get_energy_plan() -> BaseEnergyPlan:
            Retrieves the energy plan associated with the profile.
    """
    _idCounter=0

    def __init__(self, 
                name:str,
                energyPlan: BaseEnergyPlan,
                loadFactors: List[BaseFactor]=[],
                batteries: BatteriesManager=None):
        """
        Initializes a new Profile instance.

        Args:
            name (str): The name of the profile.
            energyPlan (BaseEnergyPlan): The energy plan associated with this profile.
            loadFactors (List[BaseFactor], optional): A list of energy factors that will be used in the simulation. Defaults to an empty list.
            batteries (BatteriesManager, optional): An instance of BatteriesManager to manage battery loads. Defaults to None.

        Raises:
            None
        """

        Profile._idCounter+=1
        self._id=Profile._idCounter
        self._name=name
        self._energyPlan=energyPlan
        self._loadFactors=loadFactors
        self._batteries=batteries
        self._detailedLoad:Dict[BaseFactor,np.ndarray]={}
        self._configLastSimulation=None

    def simulate(self,simulationConfig: SimulationConfig): #in kwh
        """
        Simulates the energy consumed over time at intervals defined by the selected granularity in the simulationConfig.

        This method calculates the detailed load and production based on the provided simulation configuration,
        using the defined energy factors and batteries (if available).

        Args:
            simulationConfig (SimulationConfig): The configuration settings for the simulation.

        """
        self._detailedLoad:Dict[BaseFactor,np.ndarray]={}
        self._configLastSimulation=simulationConfig

        for factor in self._loadFactors:
            load=factor.simulate(simulationConfig=simulationConfig)
            self._detailedLoad[factor]=load
            
        if self._batteries is not None:
            batteriesLoad=self._batteries.use_on(self.get_combined_load(),simulationConfig)
            self._detailedLoad[self._batteries]=batteriesLoad
            


    def get_detailed_load(self)->Dict[BaseFactor,np.ndarray]:
        """
        Retrieves the detailed energy consumption and production for the profile.

        This method returns a dictionary where each key is a energy factor and the corresponding value 
        is the simulated consumption or production as a NumPy array.

        Returns:
            Dict[BaseFactor, np.ndarray]: A dictionary mapping each energy factor to its detailed energy consumed or produced.
        """
        return self._detailedLoad
    

    def get_name(self)->str:
        """
        Retrieves the name of the profile.

        Returns:
            str: The name of the profile.
        """
        return self._name
    
    def get_id(self)->int:
        """
        Retrieves the unique identifier of the profile.

        Returns:
            int: The unique ID of the profile.
        """
        return self._id

    def get_load_pv(self)->Tuple[np.ndarray,np.ndarray]:
        """
        Returns separate arrays for the agreggated load and the aggregated production.

        This method computes the total load and production output based on the last day simulation.


        Returns:
            Tuple[np.ndarray, np.ndarray]: A tuple containing two NumPy arrays, one for load and 
            another for PV production. Each index of the array containing the energy consumed or produced for the timeElapsed based on granularity. The entire array represents a day

        Raises:
            ValueError: If there is no simulated load available.
        """
        if self._configLastSimulation is not None:
            finalLoad=np.zeros(self._configLastSimulation.num_indices())
            finalPv=np.zeros(self._configLastSimulation.num_indices())
            for asset, load in self._detailedLoad.items():
                factor_type=asset.get_factor_type()
                if factor_type==FactorType.Consumer:
                    finalLoad+=load
                elif factor_type==FactorType.Producer:
                    finalPv+=load
                elif factor_type==FactorType.Prosumer:
                    for i in range(self._configLastSimulation.num_indices()):
                        if load[i]>0:
                            finalLoad[i]+=load[i]
                        else:
                            finalPv[i]+=abs(load[i])
                elif factor_type==FactorType.Battery:
                    for i in range(self._configLastSimulation.num_indices()):
                        if load[i]<0:
                            finalLoad[i]+=load[i]
                        else:
                            finalPv[i]-=load[i]

            return finalLoad,finalPv
        else: raise ValueError("theres no simulated load")
    
    def get_combined_load_pv(self)->Tuple[np.ndarray,np.ndarray]: #resta pv a load i retorna un array per pv i un per load amb aquesta combinacio, load sera 0 si la combinacio es negativa i pv 0 si es positiva, es a dir: Exemple: initialLoad=[1,2] initialPv=[0,3] -> combinacio=[1,-1] -> (returned load =[1,0}, returned pv=[0,1])
        """
        Returns the combined load and production.

        This method subtracts the aggregated production from the aggregated load and returns two arrays: one for 
        the adjusted load and another for the adjusted PV production. If the adjusted load is 
        negative, it is set to zero, and the corresponding production output is adjusted.

        Returns:
            Tuple[np.ndarray, np.ndarray]: A tuple containing two NumPy arrays, one for the adjusted load 
            and another for the adjusted production. Each index of the array containing the energy consumed or produced for the timeElapsed based on granularity. The entire array represents a day

        Raises:
            ValueError: If there is no simulated load available.
        """
        if self._configLastSimulation is not None:
            combinedLoad=np.zeros(self._configLastSimulation.num_indices())
            combinedPv=np.zeros(self._configLastSimulation.num_indices())
            for asset, load in self._detailedLoad.items():
                factor_type=asset.get_factor_type()
                if factor_type==FactorType.Consumer or factor_type==FactorType.Prosumer or factor_type==FactorType.Battery:
                    combinedLoad+=load
                elif factor_type==FactorType.Producer:
                    combinedLoad-=load
            for i in range(self._configLastSimulation.num_indices()):
                if combinedLoad[i]<0:
                    combinedPv[i]=abs(combinedLoad[i])
                    combinedLoad[i]=0
            return combinedLoad, combinedPv
        else: raise ValueError("theres no simulated load")

    def get_energy_plan(self)->BaseEnergyPlan:
        """
        Retrieves the energy plan associated with the profile.

        Returns:
            BaseEnergyPlan: The energy plan object linked to this profile.
        """
        return self._energyPlan