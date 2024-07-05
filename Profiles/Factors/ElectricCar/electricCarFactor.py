from Profiles.Factors.baseFactor import BaseFactor
from Profiles.profileConfiguration import ProfileConfig
from Profiles.Factors.ElectricCar.electricCarModel import ElectricCarModel
from Profiles.Factors.ElectricCar.carBaseUseConfig import CarBaseUseConfig
from utils.enums import FactorType
import numpy as np
import pandas as pd

class ElectricCarFactor(BaseFactor):
    def __init__(self, model: ElectricCarModel, useConfig: CarBaseUseConfig,startChargeLevel:float=None):
        super().__init__(model.get_name(), FactorType.Consumer)
        self.model = model
        self.useConfig = useConfig
        if startChargeLevel is not None:
            self.currentBatteryLevel = model.get_battery_capacity()  #comenca amb la bateria carregada
        self.overflow=None

    def simulate(self, profileConfig: ProfileConfig) -> np.ndarray:
        load=np.zeros(profileConfig.num_indices())
        if self.overflow is not None:
            self.currentBatteryLevel=max(self.model.get_battery_capacity(),np.sum(self.overflow)+self.currentBatteryLevel)
            overflowPadded = np.pad(self.overflow, (0, len(load) - len(self.overflow)), 'constant')
            load+=overflowPadded
        self.overflow=np.array([])

        weekDay=profileConfig.get_day_of_week()
        km=self.useConfig.get_usage_at_day(weekDay)
        energyUsed=km*self.model.get_consumption_per_km
        self.currentBatteryLevel=max(0,self.currentBatteryLevel-energyUsed)
        start,duration=self.useConfig.get_charge_usage(self.currentBatteryLevel,weekDay,self.model)
        self.__distribute_cycle_load(load,start,duration,profileConfig)
        self.currentBatteryLevel=max(self.model.get_battery_capacity(),np.sum(load)+self.currentBatteryLevel)
        return load



    def __distribute_cycle_load(self,load:np.ndarray,start:float,duration:float,profileConfig:ProfileConfig):
        #faig que si el start son entre les 00 i la 05, es refereix al següent dia realment
