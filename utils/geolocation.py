import math
from typing import Tuple
from utils.geolocationInfo import coordinates, temperatures
from timezonefinder import TimezoneFinder
from datetime import datetime
from zoneinfo import ZoneInfo

class Geolocation:
    def __init__(self, name:str):
        self.name = name
        self.latitude, self.longitude=self.get_coordinates()
        self.timezoneInfo=self.get_zoneinfo_timezone()

    def get_zoneinfo_timezone(self)->ZoneInfo:
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=self.longitude, lat=self.latitude)
        if timezone_str:
            return ZoneInfo(timezone_str)
        else:
            raise ValueError("TimeZone not found")


    def get_coordinates(self)->Tuple[float, float]:
        return coordinates[self.name]

    
    def get_latitude(self)->float:
        return self.latitude

    def solar_hour(self,localDateTime:datetime)->float:
        lstm=15*(self.timezoneInfo.utcoffset(localDateTime).total_seconds()/3600)
        julianDay=localDateTime.timetuple().tm_yday
        B=(360/365)*(julianDay-81)
        eot=9.87*math.sin(2*B)-7.53*math.cos(B)-1.5*math.sin(B)
        TimeCorrection=4*(self.longitude-lstm)+eot
        localHour=localDateTime.hour + localDateTime.minute / 60 + localDateTime.second / 3600
        return localHour+(TimeCorrection/60)
    
    def solar_angle(self,localDateTime:datetime)->float:
        return 15*(self.solar_hour(localDateTime)-12)

    def get_base_temp(self)->float:
        return temperatures[self.name]['BASE']
    
    def get_amplitude_temp(self)->float:
        return temperatures[self.name]['AMPLITUDE']
    
    def get_season_offset(self)->int:
        return temperatures[self.name]['SEASON_OFFSET']