import numpy as np
import random
from typing import List,Tuple
from utils.minuteInterval import MinuteInterval
from Profiles.Factors.Cyclic.cyclicModel import CyclicModel
from Simulation.simulationConfiguration import SimulationConfig
from Profiles.Factors.Cyclic.UseConfig.cyclicBaseUseConfig import CyclicBaseUseConfig


class CyclicWeeklyUseConfig(CyclicBaseUseConfig):
    """
    A configuration class that simulates the weekly usage pattern of a cyclic energy-consuming model.

    This class is designed to simulate how often a cyclic device (e.g., a washing machine or dishwasher) is used 
    on a weekly basis, based on defined time intervals for each potential usage period, and the amount of times the cyclic device is used per week.

    Attributes:
        _timesWeekly (int): The number of times the device is used per week.
        
        _intervals (np.ndarray): An array of `MinuteInterval` objects representing the possible usage periods.

    Methods:
        get_random_interval() -> MinuteInterval:
            Returns a random interval from the list of available intervals.
        use(cyclicModel: CyclicModel, simulationConfig: SimulationConfig) -> Tuple[np.ndarray, np.ndarray]:
            Simulates the energy usage of the cyclic model based on weekly configuration.
    """
    def __init__(self,timesWeekly:int,intervals:List[MinuteInterval]):
        """
        Initializes the CyclicWeeklyUseConfig instance.

        Args:
            timesWeekly (int): The number of times the device is used per week.
            intervals (List[MinuteInterval]): A list of `MinuteInterval` objects representing the potential usage periods.
        """
        self._timesWeekly=timesWeekly
        self._intervals=np.array(intervals)
        
    def get_random_interval(self)->MinuteInterval:
        """
        Returns a random interval from the list of available intervals.

        Returns:
            MinuteInterval: A randomly selected time interval.
        """
        return self._intervals[random.randint(0,len(self._intervals)-1)]
    
    def use(self,cyclicModel:CyclicModel,simulationConfig:SimulationConfig)->Tuple[np.ndarray,np.ndarray]:
        """
        Simulates the energy usage of the cyclic model based on the weekly usage pattern.

        Args:
            cyclicModel (CyclicModel): The cyclic model representing the device being simulated.
            simulationConfig (SimulationConfig): Configuration settings for the simulation.

        Returns:
            Tuple[np.ndarray, np.ndarray]: A tuple containing two arrays:
                - The first array represents the energy usage for the current day.
                - The second array contains any overflow energy that spills into the next day.
        """
        load=np.zeros(simulationConfig.num_indices())
        overflow=np.array([])
        daylyAverage=self._timesWeekly/7
        #es podria utilitzar distribucio poisson, pero penso que és més adequat que si la mitja és major que 1 la posi una vegada com a minim, ja que en el cas de posar el rentaplats si algu el posa 7/7 dies és més probable que el posi cada dia, que que el posi un dia 2 cops, un altre 1, un altre 0...
        intervals=self._intervals.copy()
        while daylyAverage>=1:
            if(len(intervals)>0):
                randomIndexInterval=random.randint(0,len(intervals)-1)
                selectedInterval=intervals[randomIndexInterval]
                intervals=np.delete(intervals,randomIndexInterval)
            else:
                selectedInterval=self.get_random_interval()
            selectedStartWashingInMinutes=selectedInterval.random()
            overflow=self._distribute_cycle_load(load,overflow,selectedStartWashingInMinutes,simulationConfig,cyclicModel)
            daylyAverage-=1
        rand_float=random.random()
        if(rand_float<daylyAverage):
            if(len(intervals)>0):
                randomIndexInterval=random.randint(0,len(intervals)-1)
                selectedInterval=intervals[randomIndexInterval]
                intervals=np.delete(intervals,randomIndexInterval)
            else:
                selectedInterval=self.get_random_interval()
            selectedStartWashingInMinutes=selectedInterval.random()
            overflow=self._distribute_cycle_load(load,overflow,selectedStartWashingInMinutes,simulationConfig,cyclicModel)
        return load, overflow


    def _distribute_cycle_load(self,load:np.ndarray,overflow:np.ndarray,selectedStartWashingInMinutes:float,simulationConfig:SimulationConfig,cyclicModel:CyclicModel):
        """
        Distributes the energy load of a usage cycle across the simulation day.

        This method ensures that the energy consumption of a cycle is correctly applied within the current day. 
        If the cycle extends beyond the current day (i.e., overflows), the excess energy is stored in the `overflow` array.

        Args:
            load (np.ndarray): The array where energy consumption for the current day is stored.
            overflow (np.ndarray): The array where any excess (overflow) energy is stored for the next day.
            selectedStartWashingInMinutes (float): The starting time of the usage cycle in minutes.
            simulationConfig (SimulationConfig): The simulation configuration that provides details like time granularity.
            cyclicModel (CyclicModel): The cyclic model whose energy usage is being simulated.

        Returns:
            np.ndarray: Updated overflow array with any excess energy that exceeds the current day's time frame.
        """
        timeRemaining=cyclicModel.get_cycle_minutes()
        while(timeRemaining>0):
            timeElapsed=cyclicModel.get_cycle_minutes()-timeRemaining
            currentTimestampMinutes=selectedStartWashingInMinutes+timeElapsed
            indicesPerMinute=simulationConfig.num_indices()/1440
            currentIndex=int(currentTimestampMinutes*indicesPerMinute)
            nextIndex=currentIndex+1
            nextIndexTimestampMinutes=nextIndex/indicesPerMinute
            hoursElapsedThisIteration=min(((nextIndexTimestampMinutes-currentTimestampMinutes)/60),timeRemaining/60)
            indexLoad=cyclicModel.get_cycle_power()*hoursElapsedThisIteration
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
