from abc import ABC, abstractmethod
from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution
from typing import Tuple, List
import numpy as np
import pandas as pd

class CarBaseUseConfig(ABC):
    def __init__(self,dailyUsage: Tuple[BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution,BaseNumberDistribution]):
        self.dailyUsage = dailyUsage  #llista de km migs que fa per cada dia de la setmana
    
    @abstractmethod
    def get_charge_usage(self,chargeLevel:float,weekDay:int)->Tuple[float,float]: #retorna a quina hora comença a carregar i durant quanta estona. chargeLevel ja ha estat descarregat segons els km fets, aqui no es calcula aixo
        pass
    
    def get_usage_at_day(self, day:int)->List[float]:#retorna el us que li ha donat al cotxe segons day dia de la setmana
        return self.dailyUsage[day].generate_random()