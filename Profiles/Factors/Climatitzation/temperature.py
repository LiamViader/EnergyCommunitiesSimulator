import numpy as np
from utils.geolocation import Geolocation
from datetime import datetime, timedelta, date
import random
import math

class Temperature:
    def __init__(self, geolocation:Geolocation,numIndices:int,currentDate:date) -> None:
        self._currentDate=currentDate
        self._geolocation=geolocation
        self._numIndices=numIndices
        self._temperature=None
        self.simulate_temperature()

    def simulate_temperature(self):
        self._temperature=np.zeros(self._numIndices)
        indicesPerHour=self._numIndices/24
        for i in range(self._numIndices):
            hour=i/indicesPerHour
            self._temperature[i]=self._simulate_temperature_at(self._currentDate,hour)
    
    def _simulate_temperature_at(self,date:date,hour:float)->float:
        baseTemp=self._geolocation.get_base_temp()+random.uniform(0, 1)
        amplitude=self._geolocation.get_amplitude_temp()+random.uniform(0, 1)
        hourOffset=10
        seasonOffset=self._geolocation.get_season_offset()
        seasonalVariation=10*math.cos(2*math.pi*(date.timetuple().tm_yday / 365.0)+2*math.pi*(seasonOffset / 365.0))
        dailyVariation=amplitude*math.cos(2*math.pi*(hour / 24.0)+2*math.pi*(hourOffset / 24.0))
        return baseTemp + seasonalVariation + dailyVariation + random.uniform(0, 1)
    
    def change_date(self,date:date):
        self._currentDate=date
        self.simulate_temperature()

    def termic_response(self,insideTemp:float,timestamp:float,timeElapsed:float,superficialArea:float,insideVolume:float)->float:
        termicTransferenceCoef=0.5
        airDensity=1.225
        airCaloricCapacity=1005
        termicCapacityOfInteriorAir=insideVolume*airDensity*airCaloricCapacity
        indexPerMinute=self._numIndices/1440
        index=int(indexPerMinute*timestamp)
        exteriorTemp=self._temperature[index]
        return (exteriorTemp-insideTemp)*(1-math.pow(math.e,-1*((termicTransferenceCoef*superficialArea)/termicCapacityOfInteriorAir)*timeElapsed*60))
    
    def get_temperature(self)->np.ndarray:
        return self._temperature



