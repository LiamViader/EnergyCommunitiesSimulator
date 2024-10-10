from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

class BaseEnergyPlan(ABC):
    """
    An abstract base class representing a generic energy plan from an energy retailer.

    This class provides the basic structure for energy plans, including methods for 
    calculating selling and buying prices at any given time, and the flat price charged 
    for the energy plan per month.

    Attributes:
        _name (str): The name of the energy plan.

    Methods:
        get_name(): 
            Returns the name of the energy plan.

        selling_price(instant: datetime): 
            Abstract method to get the selling price of energy at a specific time.
            Must be implemented by subclasses to calculate and return the price (in €/kWh)
            for selling energy at the given time.

        buying_price(instant: datetime): 
            Abstract method to get the buying price of energy at a specific time.
            Must be implemented by subclasses to calculate and return the price (in €/kWh)
            for buying energy at the given time.

        flat_price_month(instant: Optional[datetime]): 
            Abstract method to get the flat monthly price of the energy plan.
            Must be implemented by subclasses to return the flat rate (in €) charged 
            per month for the energy plan.
    """
    def __init__(self,name:str) -> None:
        """
        Initializes the BaseEnergyPlan with the name of the plan.

        Args:
            name (str): The name of the energy plan.
        """
        self._name=name
    
    def get_name(self)->str:
        """
        Returns the name of the energy plan.

        Returns:
            str: The name of the energy plan.
        """
        return self._name

    @abstractmethod
    def selling_price(self,instant:datetime)->float:
        """
        Abstract method to get the selling price of energy at a specific time.

        This method must be implemented by subclasses to calculate and return the 
        price (in €/kWh) for selling energy at the given time.

        Args:
            instant (datetime): The specific time at which the selling price is needed.

        Returns:
            float: The selling price in €/kWh.
        """
        pass

    @abstractmethod
    def buying_price(self,instant:datetime)->float:
        """
        Abstract method to get the buying price of energy at a specific time.

        This method must be implemented by subclasses to calculate and return the 
        price (in €/kWh) for buying energy at the given time.

        Args:
            instant (datetime): The specific time at which the buying price is needed.

        Returns:
            float: The buying price in €/kWh.
        """ 
        pass
    
    @abstractmethod
    def flat_price_month(self,instant:Optional[datetime])->float:
        """
        Abstract method to get the flat monthly price of the energy plan.

        This method must be implemented by subclasses to return the flat rate (in €) 
        charged per month for the energy plan. The specific time is optional.

        Args:
            instant (Optional[datetime]): The specific time at which the flat monthly price is needed.

        Returns:
            float: The flat price in € for the month.
        """
        pass