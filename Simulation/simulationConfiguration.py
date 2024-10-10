import numpy as np
import pandas as pd
from utils.geolocation import Geolocation
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.Factors.Climatitzation.temperature import Temperature
from typing import List, Dict
from utils.enums import Granularity
from datetime import date, timedelta
from Profiles.Factors.WindTurbine.wind import Wind

class SimulationConfig:
    """
    A class for configuring simulation parameters related to energy profiles.

    This class manages the simulation settings, including granularity of time intervals,
    current date, and geolocation. It also initializes environmental factors like solar irradiation, 
    temperature, and wind based on the configured settings.

    Attributes:
        _currentDate (date): The current date for the simulation.

        _granularity (Granularity): The time granularity for the simulation (e.g., Granularity.Hour, Granularity.Minute, ..).

        _geolocation (Geolocation): The geographical location for the simulation.

        _indices (int): The number of time indices a day array has based on the granularity.

        _solarIrradiation (SolarIrradiation): An instance that provides solar irradiation data.

        _temperature (Temperature): An instance that provides temperature data.
        
        _wind (Wind): An instance that provides wind data.

    Methods:
        num_indices() -> int:
            Returns the number of indices an array for a day simulation should have based on the granularity.

        get_current_date() -> date:
            Retrieves the current date of the simulation.

        get_irradiation() -> np.ndarray:
            Retrieves solar irradiation data as a NumPy array. 
            Each index of the array contains the irradiation value
            at the timestamp index, based on the specified granularity. 
            The entire array represents a full day.

        step_one_day() -> None:
            Advances the current date by one day and updates the environmental factors.

        get_day_of_week() -> int:
            Retrieves the current day of the week (0=Monday, 6=Sunday).

        outside_termic_response(currentInsideTemp: float, timestamp: float, 
                                timeElapsed: float, superficialArea: float, 
                                insideVolume: float) -> float:
            Calculates the thermal response based on inside temperature, area that contacts the exterior and environmental factors.

        get_str_date() -> str:
            Retrieves the current date formatted as a string.

        get_wind() -> np.ndarray:
            Retrieves wind data as a NumPy array.  
            Each index of the array contains the wind velocity value
            at the timestamp index, based on the specified granularity. 
            The entire array represents a full day.

        get_temperature() -> np.ndarray:
            Retrieves temperature of the current day as a NumPy array.  
            Each index of the array contains the temperature value
            at the timestamp index, based on the specified granularity. 
            The entire array represents a full day.
    """
    def __init__(self,granularity:Granularity=Granularity.Hour,
                 currentDate:date=date(2024,1,1),
                 geolocation:Geolocation=Geolocation("Madrid, Spain")):
        """
        Initializes a new SimulationConfig instance.

        Args:
            granularity (Granularity): The granularity of the simulation (default is Granularity.Hour).
            currentDate (date): The current date for the simulation (default is January 1, 2024).
            geolocation (Geolocation): The geographical location for the simulation (default is Madrid, Spain) Currently there are not more locations available, because they are written by hand.

        Raises:
            None
        """
        self._currentDate=currentDate
        self._granularity=granularity
        self._geolocation=geolocation

        if granularity==Granularity.Hour:
            self._indices=24
        elif granularity==Granularity.Minute:
            self._indices=1440
        elif granularity==Granularity.FifteenMinutes:
            self._indices=24*4
        
        self._solarIrradiation=SolarIrradiation(geolocation=self._geolocation,numIndices=self._indices, currentDate=self._currentDate)
        self._temperature=Temperature(self._geolocation,self._indices,self._currentDate)
        self._wind=Wind(self._indices,self._currentDate)

    def num_indices(self) -> int:
        """
       Returns the number of indices an array for a day simulation should have based on the granularity

        Returns:
            int: The number of indices based on the granularity.
        """
        return self._indices
    
    
    def get_current_date(self)->date:
        """
        Retrieves the current date of the simulation.

        Returns:
            date: The current date of the simulation.
        """
        return self._currentDate
    
    def get_irradiation(self)->np.ndarray:
        """
        Retrieves solar irradiation of the current date as a NumPy array.

        Returns:
            np.ndarray: An array of solar irradiation values. 
            Each index of the array contains the irradiation value
            at the timestamp index, based on the specified granularity. 
            The entire array represents a full day.
        """
        return self._solarIrradiation.get_irradiation()
    
    def step_one_day(self):
        """
        Advances the current date by one day and updates the environmental factors.

        """
        self._currentDate=self._currentDate + timedelta(days=1)
        self._solarIrradiation.change_date(self._currentDate)
        self._temperature.change_date(self._currentDate)
        self._wind.change_date(self._currentDate)

    def get_day_of_week(self):
        """
        Retrieves the current day of the week.

        Returns:
            int: The current day of the week (0=Monday, 6=Sunday).
        """
        return self._currentDate.weekday()
    
    def outside_termic_response(self,currentInsideTemp:float,timestamp:float,timeElapsed:float,superficialArea:float,insideVolume:float)->float:
        """
        Calculates the thermal response based on inside temperature and environmental factors.

        Args:
            currentInsideTemp (float): The current inside temperature.
            timestamp (float): The current timestamp.
            timeElapsed (float): The time elapsed since the last calculation.
            superficialArea (float): The superficial area exposed to the environment.
            insideVolume (float): The inside volume of the space.

        Returns:
            float: The calculated thermal response.
        """
        return self._temperature.termic_response(currentInsideTemp,timestamp,timeElapsed,superficialArea,insideVolume)
    
    def get_str_date(self)->str:
        """
        Retrieves the current date formatted as a string.

        Returns:
            str: The current date formatted as 'YYYY_MM_DD'.
        """
        return self._currentDate.strftime('%Y_%m_%d')
    
    def get_wind(self)->np.ndarray:
        """
        Retrieves wind velocity of the current date as a NumPy array.

        Returns:
            np.ndarray: An array of wind speed values.
            Each index of the array contains the wind velocity value
            at the timestamp index, based on the specified granularity. 
            The entire array represents a full day.
        """
        return self._wind.get_wind()
    
    
    def get_temperature(self)->np.ndarray:
        """
        Retrieves temperature of the current date as a NumPy array.

        Returns:
            np.ndarray: An array of temperature values.
            Each index of the array contains the temperature value
            at the timestamp index, based on the specified granularity. 
            The entire array represents a full day.
        """
        return self._temperature.get_temperature()