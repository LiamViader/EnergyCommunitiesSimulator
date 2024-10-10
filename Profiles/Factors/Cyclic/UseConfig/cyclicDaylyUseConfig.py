import numpy as np
import random
from typing import List,Tuple
from utils.minuteInterval import MinuteInterval
from Profiles.Factors.Cyclic.cyclicModel import CyclicModel
from Simulation.simulationConfiguration import SimulationConfig
from Profiles.Factors.Cyclic.UseConfig.cyclicBaseUseConfig import CyclicBaseUseConfig


class CyclicDaylyUseConfig(CyclicBaseUseConfig):
    """
    A configuration class that simulates the daily usage pattern of a cyclic energy-consuming model.
    
    This class specifies the usage intervals for each day of the week, determining when a cyclic model (e.g., a washing machine)
    is used during the day based on pre-defined time intervals for each day.

    Attributes:
        _weekUsage (Tuple[List[MinuteInterval],List[MinuteInterval],List[MinuteInterval],
                    List[MinuteInterval],List[MinuteInterval],List[MinuteInterval],
                    List[MinuteInterval]]): 
        A tuple containing lists of time intervals for each day of the week.
        Each day (Monday-Sunday) has a list of `MinuteInterval` objects representing the potential times when the device is used.
    
    Methods:
        use(cyclicModel: CyclicModel, simulationConfig: SimulationConfig) -> Tuple[np.ndarray, np.ndarray]:
            Simulates the energy usage of the cyclic model for a specific day based on the configured time intervals.
    """
    def __init__(self,weekUsage:Tuple[List[MinuteInterval],List[MinuteInterval],List[MinuteInterval],List[MinuteInterval],List[MinuteInterval],List[MinuteInterval],List[MinuteInterval]]):#weekUsage te per cada dia de la setmana, els intervals al que es sol usar
        """
        Initializes a CyclicDaylyUseConfig instance.
        
        Args:
            weekUsage (Tuple[List[MinuteInterval],List[MinuteInterval],List[MinuteInterval],
                        List[MinuteInterval],List[MinuteInterval],List[MinuteInterval],
                        List[MinuteInterval]]): 
                A tuple with seven lists, one for each day of the week.
                Each list contains `MinuteInterval` objects that represent intervals of possible usage times for that day.
        """
        self._weekUsage=weekUsage
        
    
    def use(self,cyclicModel:CyclicModel,simulationConfig:SimulationConfig)->Tuple[np.ndarray,np.ndarray]:
        """
        Simulates the energy usage of the cyclic model for the current day based on configured usage intervals.
        
        Args:
            cyclicModel (CyclicModel): The cyclic model to simulate (e.g., a washing machine).
            simulationConfig (SimulationConfig): Configuration settings for the simulation.
        
        Returns:
            Tuple[np.ndarray, np.ndarray]: A tuple with two arrays:
                - The first array represents the energy usage over the course of the day.
                - The second array contains any energy overflow that spills into the next day.
        """
        load=np.zeros(simulationConfig.num_indices())
        overflow=np.array([])
        weekDay=simulationConfig.get_day_of_week()
        for interval in self._weekUsage[weekDay]:
            startInMinutes=interval.random()
            overflow=self._distribute_cycle_load(load,overflow,startInMinutes,simulationConfig,cyclicModel)
        return load,overflow


    def _distribute_cycle_load(self,load:np.ndarray,overflow:np.ndarray,selectedStartWashingInMinutes:float,simulationConfig:SimulationConfig,cyclicModel:CyclicModel)->np.ndarray:
        """
        Distributes the energy load of a usage cycle across the simulation day.
        
        This method ensures that the energy consumption of a cycle is correctly applied within the current day. If
        the cycle extends beyond the current day (i.e., overflows), the excess energy is stored in the `overflow` array.
        
        Args:
            load (np.ndarray): The array where energy consumption for the current day is stored.
            overflow (np.ndarray): The array where any excess (overflow) energy is stored for the next day.
            selectedStartWashingInMinutes (float): The starting time of the usage cycle in minutes (e.g., 780 for 1:00 PM).
            simulationConfig (SimulationConfig): The simulation configuration that provides details like time granularity.
            cyclicModel (CyclicModel): The cyclic model whose energy usage is being simulated.

        Returns:
            np.ndarray: Updated overflow array with any excess energy that exceeds the current day's time frame.
        """
        totalTime=cyclicModel.get_cycle_minutes()
        timeRemaining=totalTime
        power=cyclicModel.get_cycle_power()
        while(timeRemaining>0):
            timeElapsed=totalTime-timeRemaining
            currentTimestampMinutes=selectedStartWashingInMinutes+timeElapsed
            indicesPerMinute=simulationConfig.num_indices()/1440
            currentIndex=int(currentTimestampMinutes*indicesPerMinute)
            nextIndex=currentIndex+1
            nextIndexTimestampMinutes=nextIndex/indicesPerMinute
            hoursElapsedThisIteration=min(((nextIndexTimestampMinutes-currentTimestampMinutes)/60),timeRemaining/60)
            indexLoad=power*hoursElapsedThisIteration
            if(currentIndex<simulationConfig.num_indices()):#si hi cap al dia actual
                load[currentIndex]+=indexLoad
            else:#sino al overflow
                transformedCurrentIndex=currentIndex-simulationConfig.num_indices()
                if transformedCurrentIndex<len(overflow):
                    overflow[transformedCurrentIndex]+=indexLoad
                else:
                    new_overflow=np.zeros(transformedCurrentIndex + 1, dtype=overflow.dtype)
                    new_overflow[:len(overflow)] = overflow
                    overflow=new_overflow
                    overflow[transformedCurrentIndex]+=indexLoad
            timeRemaining=timeRemaining-hoursElapsedThisIteration*60
        return overflow
