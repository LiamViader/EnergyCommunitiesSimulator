from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

class BaseEnergyPlan(ABC):
    def __init__(self,name:str) -> None:
        self.name=name
    
    def get_name(self)->str:
        return self.name

    @abstractmethod
    def selling_price(self,instant:datetime)->float: #returns €/kwh
        pass

    @abstractmethod
    def buying_price(self,instant:datetime)->float: #returns €/kwh
        pass
    
    @abstractmethod
    def flat_price_month(self,instant:Optional[datetime])->float: #returns €
        pass