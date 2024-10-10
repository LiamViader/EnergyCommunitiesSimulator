from utils.enums import Granularity
from utils.geolocation import Geolocation
from datetime import datetime, timedelta, date
import math
import numpy as np
import pandas as pd


class SolarIrradiation:
    """
    Simulates solar irradiation of a day for a given geolocation.

    This class provides functionality to calculate the solar irradiation values based on geographic
    location.

    Attributes:
        _currentDate (date): The current date for which solar irradiation is simulated.

        _geolocation (Geolocation): The geographical location information for the irradiation calculation.

        _numIndices (int): The number of time steps for the simulation day. It is based on granularity (Minutal = 1440 indices)
        
        _simulatedIrradiation (np.ndarray): An array of simulated solar irradiation values in kW/m².

    Methods:
        simulate_irradiation() -> None:
            Calculates and simulates solar irradiation based on geographical and temporal parameters.

        get_irradiation() -> np.ndarray:
            Returns the simulated solar irradiation values.

        change_date(newDate: date) -> None:
            Updates the current date and re-simulates the solar irradiation values.
    
    Notes:
        - To use real solar irradiation data, implement a method to read solar irradiation data for the day whenever the date changes,
          and store the values in the `_simulatedIrradiation` attribute.
        - The simulation does not take into account clouds or any type of atmospheric obstruction, which may affect actual solar irradiation values.
        - The model assumes a constant efficiency for solar panels; real-world efficiencies can vary based on factors such as temperature, angle of incidence, and age of the solar panels.
        - Consideration of geographic features such as mountains or tall buildings can influence solar angles and available sunlight, which are not included in this simulation.
        - The irradiance values are averaged over the year, and seasonal variations are approximated using simple mathematical models. For more accurate simulations, additional meteorological data should be integrated.
    """
    def __init__(self, geolocation:Geolocation,numIndices:int,currentDate:date):
        """
        Initializes a SolarIrradiation instance with the specified parameters.

        Args:
            geolocation (Geolocation): The geographical location for irradiation simulation.
            numIndices (int): The number of indices to represent time intervals in the simulation day.
            currentDate (date): The current date for the simulation.
        """
        self._currentDate=currentDate
        self._geolocation=geolocation
        self._numIndices=numIndices
        self._simulatedIrradiation=None
        self.simulate_irradiation()
    
    def simulate_irradiation(self):
        """
        Calculates and simulates solar irradiation based on geographical and temporal parameters.

        The function computes the solar angle, solar declination, and extraterrestrial solar irradiation
        to derive the solar irradiation values for each time index.
        """
        self._simulatedIrradiation=np.zeros(self._numIndices)
        current_date=self._currentDate
        julianDay=current_date.timetuple().tm_yday-1
        B=(360/365)*(julianDay-81)
        solarDeclination=23.45*math.sin(math.radians(B))
        extraterrester_solar_irrad=1361*(1+0.033*math.cos(math.radians((360-julianDay)/365)))
        for j in range(self._numIndices):
            hour=(24/self._numIndices)*j
            localDatetime=self._build_datetime_from_hour(hour)
            solar_angle=self._geolocation.solar_angle(localDatetime)
            cos_cenital_solar_angle=math.sin(math.radians(self._geolocation.get_latitude()))*math.sin(math.radians(solarDeclination))+math.cos(math.radians(solarDeclination))*math.cos(math.radians(self._geolocation.get_latitude()))*math.cos(math.radians(solar_angle))
            irradiation=extraterrester_solar_irrad*cos_cenital_solar_angle
            irradiation=max(irradiation,0)
            self._simulatedIrradiation[j]+=irradiation/1000 #convert from w/m2 to kw/m2
    
    def get_irradiation(self)->datetime:
        """
        Returns the simulated solar irradiation values.

        Returns:
            np.ndarray: An array of solar irradiation values in kW/m². Each index represents a time step in the simulation day
        """
        return self._simulatedIrradiation

    def _build_datetime_from_hour(self, hour_decimal):
        """
        Constructs a datetime object from a decimal hour value.

        Args:
            hour_decimal (float): The decimal hour value.

        Returns:
            datetime: A datetime object representing the specified hour on the current date.
        """
        hours = int(hour_decimal)
        minutes = int((hour_decimal - hours) * 60)
        seconds = int(((hour_decimal - hours) * 60 - minutes) * 60)
        microseconds = int((((hour_decimal - hours) * 60 - minutes) * 60 - seconds) * 1e6)
        current_date=self._currentDate
        return datetime(current_date.year,current_date.month,current_date.day,hours, minutes, seconds, microseconds)

    def change_date(self,newDate:date):
        """
        Updates the current date and re-simulates the solar irradiation values.

        Args:
            newDate (date): The new date to set for irradiation simulation.
        """
        self._currentDate=newDate
        self.simulate_irradiation()
