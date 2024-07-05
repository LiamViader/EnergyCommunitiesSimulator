from typing import List, Tuple
from utils.minuteInterval import MinuteInterval
from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution
from Profiles.Factors.ElectricCar.carBaseUseConfig import CarBaseUseConfig

class CarOnNeedUseConfig(CarBaseUseConfig):
    def __init__(self, dailyUsage: List[BaseNumberDistribution], chargeIntervals: List[List[MinuteInterval]], batteryThreshold: float):
        super().__init__(dailyUsage)
        self.chargeIntervals = chargeIntervals  #per cada dia de la setmana, intervals als que sol carregar aquell dia
        self.batteryThreshold = batteryThreshold  #Nivell de bateria passat el qual carrega (0-1) p.e 0.8


    def get_charge_usage(self,chargeLevel:float,weekDay:int)->Tuple[float,float]: #retorna a quina hora comença a carregar i durant quanta estona en hores. chargeLevel ja ha estat descarregat segons els km fets, aqui no es calcula aixo
        pass