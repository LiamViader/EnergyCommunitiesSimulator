import numpy as np
from datetime import date
from typing import Tuple
import math

class Wind:
    """
    Simulates wind speed variations over a day.

    This class generates wind speed data for each time step of a day based on seasonal patterns and provides methods
    to retrieve and change the simulated wind data.

    Attributes:
        _wind (np.ndarray): An array of wind speed values for each time step of the day.

        _indices (int): The number of indices representing time intervals of the day.
        
        _currentDate (date): The current date used to determine the season for wind speed simulation.

    Methods:
        simulate_wind() -> None:
            Generates wind speed data for each hour of the day and interpolates it across the specified indices.

        get_wind() -> np.ndarray:
            Returns the simulated wind speed data.

        change_date(date: date) -> None:
            Changes the current date and re-simulates the wind speed data based on the new date.

        get_season() -> str:
            Determines the current season based on the current date.
    Notes:
        - To use real wind data, implement a method to read wind data for the day whenever the date changes,
          and store the values in the `_wind` attribute.
        - The wind simulation uses a really basic model and does not take into account the geolocation.
    """
    def __init__(self,indices:int,currentDate:date) -> None:
        """
        Initializes the Wind simulation with the specified number of indices and the current date.

        Args:
            indices (int): The number of indices representing time intervals for wind speed simulation day.
            currentDate (date): The current date used for seasonal calculations.
        """
        self._wind=None
        self._indices=indices
        self._currentDate=currentDate
        self.simulate_wind()

    def simulate_wind(self)->None:
        """
        Generates wind speed data for each hour of the day and interpolates it across the specified indices.
        """
        season=self.get_season()
        windHour=np.zeros(24)

        for hour in range(24):
            mean,std=self._get_mean_std(hour,season)
            windHour[hour] = max(np.random.normal(mean, std),0.5)
        
        self._wind=np.zeros(self._indices)
        for i in range(24):
            start_index = i * (self._indices // 24)
            end_index = (i + 1) * (self._indices // 24)
            if i == 23:  # Para el último intervalo, asegurarse de llegar al final
                end_index = self._indices
            # Interpolar entre windHour[i] i windHour[i + 1]
            next_wind = windHour[(i + 1) % 24] 
            self._wind[start_index:end_index] = np.linspace(windHour[i], next_wind, end_index - start_index)
            
            

    def get_wind(self)->np.ndarray:
        """
        Returns the simulated wind speed data.

        Returns:
            np.ndarray: The array of simulated wind speed values for each index.
        """
        return self._wind
    
    def change_date(self,date:date):
        """
        Changes the current date and re-simulates the wind speed data based on the new date.

        Args:
            date (date): The new date to set for wind speed simulation.
        """
        self._currentDate=date
        self.simulate_wind()
    
    def get_season(self):
        """
        Determines the current season based on the current date.

        Returns:
            str: The current season ('WINTER', 'SPRING', 'SUMMER', 'AUTUMN').
        """
        month=self._currentDate.month
        if 3 <= month <= 5:
            return 'SPRING'
        elif 6 <= month <= 8:
            return 'SUMMER'
        elif 9 <= month <= 11:
            return 'AUTUMN'
        else:
            return 'WINTER'
    
    def _get_mean_std(self,hour:int,season:str)->Tuple[float,float]:
        """
        Returns the mean and standard deviation of wind speed for a given hour and season.

        Args:
            hour (int): The hour of the day (0-23).
            season (str): The current season.

        Returns:
            Tuple[float, float]: A tuple containing the mean wind speed and the standard deviation.
        """
        if season == 'WINTER':
            if 6 <= hour < 10:
                mean_wind_speed = 3.0
                std_dev = 1.5
            elif 10 <= hour < 18:
                mean_wind_speed = 5.0
                std_dev = 2
            else:
                mean_wind_speed = 2.5 
                std_dev = 1.5
        elif season == 'SPRING':
            if 6 <= hour < 10:
                mean_wind_speed = 4.0
                std_dev = 2
            elif 10 <= hour < 18:
                mean_wind_speed = 6.0
                std_dev = 2.5
            else:
                mean_wind_speed = 3.0
                std_dev = 2
        elif season == 'SUMMER':
            if 6 <= hour < 10:
                mean_wind_speed = 3.0
                std_dev = 1.5
            elif 10 <= hour < 18:
                mean_wind_speed = 4.5
                std_dev = 2
            else:
                mean_wind_speed = 2.0
                std_dev = 1
        elif season == 'AUTUMN':
            if 6 <= hour < 10:
                mean_wind_speed = 3.5
                std_dev = 1.8
            elif 10 <= hour < 18:
                mean_wind_speed = 5.5
                std_dev = 2.4
            else:
                mean_wind_speed = 3.0
                std_dev = 1.5
        else:
            mean_wind_speed = 4.0
            std_dev = 1.7
        return mean_wind_speed, std_dev