from typing import List, Tuple
from utils.minuteInterval import MinuteInterval
from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution
from Profiles.Factors.ElectricCar.UseConfig.carBaseUseConfig import CarBaseUseConfig
from Profiles.Factors.ElectricCar.electricCarModel import ElectricCarModel

class CarOnNeedUseConfig(CarBaseUseConfig):
    def __init__(self, dailyUsage: Tuple[BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution], chargeIntervals: Tuple[MinuteInterval,MinuteInterval,MinuteInterval,MinuteInterval,MinuteInterval,MinuteInterval,MinuteInterval], batteryThreshold: float):
        super().__init__(dailyUsage)
        self.chargeIntervals = chargeIntervals  #per cada dia de la setmana, intervals al que sol comencar a carregar aquell dia
        self.batteryThreshold = batteryThreshold  #Nivell de bateria passat el qual carrega (0-1) p.e 0.8


    def get_charge_usage(self,chargeLevel:float,weekDay:int,model:ElectricCarModel)->Tuple[float,float]: #retorna a quina hora comença a carregar i durant quanta estona en hores. chargeLevel ja ha estat descarregat segons els km fets, aqui no es calcula aixo
        if chargeLevel>=(model.get_battery_capacity()*self.batteryThreshold): #no carregar
            return 0,0
        else:
            if self.chargeIntervals[weekDay] is None:
                return 0,0
            else:
                start=self.chargeIntervals[weekDay].random()/60
                energyToCharge=(model.get_battery_capacity()-chargeLevel)/model.get_charge_efficiency()
                duration=energyToCharge/model.get_charge_power()
                return start, duration