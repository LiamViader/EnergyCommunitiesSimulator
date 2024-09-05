from Profiles.Factors.baseFactor import BaseFactor
from Simulation.simulationConfiguration import SimulationConfig
from Profiles.Factors.ElectricCar.electricCarModel import ElectricCarModel
from Profiles.Factors.ElectricCar.UseConfig.carBaseUseConfig import CarBaseUseConfig
from utils.enums import FactorType
import numpy as np
import pandas as pd

class ElectricCarFactor(BaseFactor):
    def __init__(self, model: ElectricCarModel, useConfig: CarBaseUseConfig,startChargeLevel:float=None):
        super().__init__(model.get_name(), FactorType.Consumer)
        self.model = model
        self.useConfig = useConfig
        if startChargeLevel is None:
            self.currentBatteryLevel = model.get_battery_capacity()  #comenca amb la bateria carregada
        else:
            self.currentBatteryLevel=startChargeLevel
        self.overflow=None

    def simulate(self, simulationConfig: SimulationConfig) -> np.ndarray:
        load=np.zeros(simulationConfig.num_indices())
        lastOverflowCharge=0
        if self.overflow is not None:
            lastOverflowCharge=np.sum(self.overflow)*self.model.get_charge_efficiency()
            self.currentBatteryLevel=min(self.model.get_battery_capacity(),(lastOverflowCharge)+self.currentBatteryLevel)
            overflowPadded = np.pad(self.overflow, (0, len(load) - len(self.overflow)), 'constant')
            load+=overflowPadded
        self.overflow=np.zeros(simulationConfig.num_indices())

        weekDay=simulationConfig.get_day_of_week()
        km=self.useConfig.get_usage_at_day(weekDay)
        energyUsed=km*self.model.get_consumption_per_km()
        self.currentBatteryLevel=max(0,self.currentBatteryLevel-energyUsed)
        start,duration=self.useConfig.get_charge_usage(self.currentBatteryLevel,weekDay,self.model)
        self.__distribute_cycle_load(load,start,duration,simulationConfig)
        self.currentBatteryLevel=min(self.model.get_battery_capacity(),(np.sum(load)*self.model.get_charge_efficiency()-lastOverflowCharge)+self.currentBatteryLevel)
        return load



    def __distribute_cycle_load(self,load:np.ndarray,start:float,duration:float,simulationConfig:SimulationConfig):
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
            indexLoad=self.model.get_charge_power()*hoursElapsedThisIteration
            if(currentIndex<simulationConfig.num_indices()):#si hi cap al dia actual
                load[currentIndex]+=indexLoad
            else:#sino al overflow
                transformedCurrentIndex=currentIndex-simulationConfig.num_indices()
                self.overflow[transformedCurrentIndex]+=indexLoad
            timeRemaining=timeRemaining-hoursElapsedThisIteration*60
