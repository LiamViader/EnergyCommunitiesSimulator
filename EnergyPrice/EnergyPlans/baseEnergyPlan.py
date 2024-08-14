from abc import ABC, abstractmethod
from datetime import datetime


class BaseEnergyPlan(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def sell_energy(self,energy:float,instant:datetime)->float: #energy in kwh, returns earnings
        pass

    @abstractmethod
    def buy_energy(self,energy:float,instant:datetime)->float: #energy in kwh, returns cost
        pass

    @abstractmethod
    def selling_price(self,instant:datetime)->float: #returns €/kwh
        pass

    @abstractmethod
    def buying_price(self,instant:datetime)->float: #returns €/kwh
        pass