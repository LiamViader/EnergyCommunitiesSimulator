import math
from typing import Tuple
from utils.geolocationInfo import coordinates, temperatures
from timezonefinder import TimezoneFinder
from datetime import datetime
from zoneinfo import ZoneInfo

class Geolocation:
    """
    Class representing geolocation information for a specific location.

    This class handles the retrieval of coordinates, timezone information, and climatic data such as 
    temperature and wind characteristics for the given location. It also provides methods to compute 
    solar hour and solar angle based on the local date and time.

    Attributes:
        _name (str): The name of the location.
        _latitude (float): The latitude of the location.
        _longitude (float): The longitude of the location.
        _timezoneInfo (ZoneInfo): The timezone information for the location.

    Methods:     
        get_latitude() -> float:
            Returns the latitude of the location.
        
        solar_hour(localDateTime: datetime) -> float:
            Calculates the solar hour for a given local date and time.
        
        solar_angle(localDateTime: datetime) -> float:
            Calculates the solar angle for a given local date and time.
        
        get_base_temp() -> float:
            Returns the base temperature for the location.
        
        get_amplitude_temp() -> float:
            Returns the amplitude of temperature variation for the location.
        
        get_season_offset() -> int:
            Returns the seasonal offset for the location.
        
        get_wind(season: str) -> Tuple[float, float]:
            Retrieves the mean and standard deviation of wind for the specified season.
    """
    def __init__(self, name:str):
        """
        Initializes a Geolocation instance.

        Args:
            name (str): The name of the location.
        
        Raises:
            ValueError: If the timezone cannot be determined.
        """
        self._name = name
        self._latitude, self.longitude=self._get_coordinates()
        self._timezoneInfo=self.get_zoneinfo_timezone()

    def get_zoneinfo_timezone(self)->ZoneInfo:
        """
        Retrieves the timezone information for the location.

        Returns:
            ZoneInfo: The timezone information for the location.

        Raises:
            ValueError: If the timezone cannot be found.
        """
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=self.longitude, lat=self._latitude)
        if timezone_str:
            return ZoneInfo(timezone_str)
        else:
            raise ValueError("TimeZone not found")


    def _get_coordinates(self)->Tuple[float, float]:
        """
        Retrieves the latitude and longitude coordinates for the location.

        Returns:
            Tuple[float, float]: The latitude and longitude of the location.
        """
        return coordinates[self._name]

    
    def get_latitude(self)->float:
        """
        Returns the latitude of the location.

        Returns:
            float: The latitude of the location.
        """
        return self._latitude

    def solar_hour(self,localDateTime:datetime)->float:
        """
        Calculates the solar hour for a given local date and time.

        Args:
            localDateTime (datetime): The local date and time for which to calculate the solar hour.

        Returns:
            float: The solar hour adjusted for the location's timezone.
        """
        lstm=15*(self._timezoneInfo.utcoffset(localDateTime).total_seconds()/3600)
        julianDay=localDateTime.timetuple().tm_yday
        B=(360/365)*(julianDay-81)
        eot=9.87*math.sin(2*B)-7.53*math.cos(B)-1.5*math.sin(B)
        TimeCorrection=4*(self.longitude-lstm)+eot
        localHour=localDateTime.hour + localDateTime.minute / 60 + localDateTime.second / 3600
        return localHour+(TimeCorrection/60)
    
    def solar_angle(self,localDateTime:datetime)->float:
        """
        Calculates the solar angle for a given local date and time.

        Args:
            localDateTime (datetime): The local date and time for which to calculate the solar angle.

        Returns:
            float: The solar angle in degrees.
        """
        return 15*(self.solar_hour(localDateTime)-12)

    def get_base_temp(self)->float:
        """
        Returns the base temperature for the location.

        Returns:
            float: The base temperature of the location.
        """
        return temperatures[self._name]['BASE']
    
    def get_amplitude_temp(self)->float:
        """
        Returns the amplitude of temperature variation for the location.

        Returns:
            float: The amplitude of temperature variation.
        """
        return temperatures[self._name]['AMPLITUDE']
    
    def get_season_offset(self)->int:
        """
        Returns the seasonal offset for the location.

        Returns:
            int: The seasonal offset value.
        """
        return temperatures[self._name]['SEASON_OFFSET']
    
