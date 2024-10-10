import numpy as np
from utils.geolocation import Geolocation
from datetime import datetime, timedelta, date
import random
import math

class Temperature:
    """
    Represents the temperature simulation for a specific geolocation over a defined time period.

    The class simulates temperature variations throughout the day based on geographical factors, seasonal changes, 
    and daily fluctuations. It also allows for the adjustment of the current date to simulate temperature for different days.

    Attributes:
        _currentDate (date): The current date for which temperatures are simulated.

        _geolocation (Geolocation): The geographical context affecting temperature.

        _numIndices (int): The number of time steps for the day.
        
        _temperature (np.ndarray): An array storing simulated temperatures for each time step.
    
    Methods:
        simulate_temperature() -> None:
            Simulates the temperature for each time step based on the current date and geographical location.

        change_date(date: date) -> None:
            Changes the current date and recalculates the temperature for the new date.

        termic_response(insideTemp: float, timestamp: float, timeElapsed: float, superficialArea: float, insideVolume: float) -> float:
            Calculates the thermal response based on the inside temperature, time elapsed, and other factors.

        get_temperature() -> np.ndarray:
            Returns the array of simulated temperatures of the day.
    Notes:
        - To use real temperature data, implement a method to read temperature data for the day whenever the date changes,
          and store the values in the `_temperature` attribute.
        - The temperature simulation uses a really basic sinusoidal model for temperature variations.
    """
    def __init__(self, geolocation:Geolocation,numIndices:int,currentDate:date) -> None:
        """
        Initializes the Temperature simulation with a specific geolocation, number of indices, and the current date.

        Args:
            geolocation (Geolocation): The geographical context for temperature simulation.
            numIndices (int): The number of time indices for temperature simulation.
            currentDate (date): The current date for temperature simulation.
        """
        self._currentDate=currentDate
        self._geolocation=geolocation
        self._numIndices=numIndices
        self._temperature=None
        self.simulate_temperature()

    def simulate_temperature(self):
        """
        Simulates the temperature for each time index based on the current date and geographical location.
        """
        self._temperature=np.zeros(self._numIndices)
        indicesPerHour=self._numIndices/24
        for i in range(self._numIndices):
            hour=i/indicesPerHour
            self._temperature[i]=self._simulate_temperature_at(self._currentDate,hour)
    
    def _simulate_temperature_at(self,date:date,hour:float)->float:
        """
        Simulates the temperature at a specific date and hour.

        Args:
            date (date): The date for which the temperature is simulated.
            hour (float): The hour of the day (0-24) for which the temperature is simulated.

        Returns:
            float: The simulated temperature in degrees Celsius.
        """
        baseTemp=self._geolocation.get_base_temp()+random.uniform(0, 1)
        amplitude=self._geolocation.get_amplitude_temp()+random.uniform(0, 1)
        hourOffset=10
        seasonOffset=self._geolocation.get_season_offset()
        seasonalVariation=10*math.cos(2*math.pi*(date.timetuple().tm_yday / 365.0)+2*math.pi*(seasonOffset / 365.0))
        dailyVariation=amplitude*math.cos(2*math.pi*(hour / 24.0)+2*math.pi*(hourOffset / 24.0))
        return baseTemp + seasonalVariation + dailyVariation + random.uniform(0, 1)
    
    def change_date(self,date:date):
        """
        Changes the current date and recalculates the temperature for the new date.

        Args:
            date (date): The new date for temperature simulation.
        """
        self._currentDate=date
        self.simulate_temperature()

    def termic_response(self,insideTemp:float,timestamp:float,timeElapsed:float,superficialArea:float,insideVolume:float)->float:
        """
        Calculates the thermal response based on the inside temperature, time elapsed, and other factors.

        Args:
            insideTemp (float): The current inside temperature in degrees Celsius.
            timestamp (float): The timestamp in minutes at which the thermal response is calculated.
            timeElapsed (float): The time elapsed in hours since the last temperature calculation.
            superficialArea (float): The area in square meters that is in contact with the outside.
            insideVolume (float): The volume of the inside space in cubic meters.

        Returns:
            float: The thermal response in degrees Celsius.
        """
        termicTransferenceCoef=0.5
        airDensity=1.225
        airCaloricCapacity=1005
        termicCapacityOfInteriorAir=insideVolume*airDensity*airCaloricCapacity
        indexPerMinute=self._numIndices/1440
        index=int(indexPerMinute*timestamp)
        exteriorTemp=self._temperature[index]
        return (exteriorTemp-insideTemp)*(1-math.pow(math.e,-1*((termicTransferenceCoef*superficialArea)/termicCapacityOfInteriorAir)*timeElapsed*60))
    
    def get_temperature(self)->np.ndarray:
        """
        Returns the array of simulated temperatures.

        Returns:
            np.ndarray: An array containing the simulated temperatures for each time index.
        """
        return self._temperature



