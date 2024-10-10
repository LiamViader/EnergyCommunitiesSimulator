from Profiles.Factors.baseFactor import BaseFactor
from Simulation.simulationConfiguration import SimulationConfig
from Profiles.Factors.ElectricCar.electricCarModel import ElectricCarModel
from Profiles.Factors.ElectricCar.UseConfig.carBaseUseConfig import CarBaseUseConfig
from utils.enums import FactorType
import numpy as np
import pandas as pd

class ElectricCarFactor(BaseFactor):
    """
    A simulation factor that models the charging and discharging behavior of an electric car.

    This class simulates the energy usage of an electric car based on its model, usage patterns, and charging behavior.
    It accounts the recharging process based on usage configuration.

    Attributes:
        _model (ElectricCarModel): The model of the electric car being simulated.

        _useConfig (CarBaseUseConfig): Configuration detailing the car's usage and charging behavior.

        _currentBatteryLevel (float): The current battery level of the car in kWh.
        
        _overflow (np.ndarray): Tracks the overflow of energy usage when charging spills over into the next day.

    Methods:
        simulate(simulationConfig):
            Simulates the energy usage of the electric car and the charging consumption during the simulation day.
    """
    def __init__(self, model: ElectricCarModel, useConfig: CarBaseUseConfig,startChargeLevel:float=None):
        """
        Initializes the ElectricCarFactor with a specific car model, usage configuration, and an optional starting charge level.

        Args:
            model (ElectricCarModel): The electric car model.
            useConfig (CarBaseUseConfig): The usage configuration for the car's energy consumption and charging.
            startChargeLevel (float, optional): Initial battery level in kWh. Defaults to a full charge.
        """
        super().__init__(model.get_name(), FactorType.Consumer)
        self._model = model
        self._useConfig = useConfig
        if startChargeLevel is None:
            self._currentBatteryLevel = model.get_battery_capacity()  #comenca amb la bateria carregada
        else:
            self._currentBatteryLevel=startChargeLevel
        self._overflow=None

    def simulate(self, simulationConfig: SimulationConfig) -> np.ndarray:
        """
        Simulates the energy usage of the electric car recharging over the simulation period.

        Args:
            simulationConfig (SimulationConfig): Configuration of the current simulation.

        Returns:
            np.ndarray: Array representing the energy consumption during each simulation time step of the day.
        """
        load=np.zeros(simulationConfig.num_indices())
        lastOverflowCharge=0
        if self._overflow is not None:
            lastOverflowCharge=np.sum(self._overflow)*self._model.get_charge_efficiency()
            self._currentBatteryLevel=min(self._model.get_battery_capacity(),(lastOverflowCharge)+self._currentBatteryLevel)
            overflowPadded = np.pad(self._overflow, (0, len(load) - len(self._overflow)), 'constant')
            load+=overflowPadded
        self._overflow=np.zeros(simulationConfig.num_indices())

        weekDay=simulationConfig.get_day_of_week()
        km=self._useConfig.get_usage_at_day(weekDay)
        energyUsed=km*self._model.get_consumption_per_km()
        self._currentBatteryLevel=max(0,self._currentBatteryLevel-energyUsed)
        start,duration=self._useConfig.get_charge_usage(self._currentBatteryLevel,weekDay,self._model)
        self._distribute_cycle_load(load,start,duration,simulationConfig)
        self._currentBatteryLevel=min(self._model.get_battery_capacity(),(np.sum(load)*self._model.get_charge_efficiency()-lastOverflowCharge)+self._currentBatteryLevel)
        return load



    def _distribute_cycle_load(self,load:np.ndarray,start:float,duration:float,simulationConfig:SimulationConfig):
        """
        Distributes the charging load over the simulation time steps, adjusting for overflow if necessary.

        Args:
            load (np.ndarray): The array representing energy comsumption in each time step.
            start (float): The start time of the charging cycle (in hours).
            duration (float): The duration of the charging cycle (in hours).
            simulationConfig (SimulationConfig): The simulation configuration with time indices.
        """
        #faig que si el start son entre les 00 i la 05, es refereix al següent dia realment
        if start<=5.0:
            start+=24
        
        duration=duration*60
        start=start*60
        timeRemaining=duration
        while(timeRemaining>0):
            timeElapsed=duration-timeRemaining
            currentTimestampMinutes=start+timeElapsed
            indicesPerMinute=simulationConfig.num_indices()/1440
            currentIndex=int(currentTimestampMinutes*indicesPerMinute)
            nextIndex=currentIndex+1
            nextIndexTimestampMinutes=nextIndex/indicesPerMinute
            hoursElapsedThisIteration=min(((nextIndexTimestampMinutes-currentTimestampMinutes)/60),timeRemaining/60)
            indexLoad=self._model.get_charge_power()*hoursElapsedThisIteration
            if(currentIndex<simulationConfig.num_indices()):#si hi cap al dia actual
                load[currentIndex]+=indexLoad
            else:#sino al overflow
                transformedCurrentIndex=currentIndex-simulationConfig.num_indices()
                self._overflow[transformedCurrentIndex]+=indexLoad
            timeRemaining=timeRemaining-hoursElapsedThisIteration*60
