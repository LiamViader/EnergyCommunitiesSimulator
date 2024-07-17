import numpy as np
from utils.geolocation import Geolocation
from datetime import datetime, timedelta, date
import random
import math

class Temperature:
    def __init__(self, geolocation:Geolocation,numIndices:int,currentDate:date) -> None:
        self.currentDate=currentDate
        self.geolocation=geolocation
        self.numIndices=numIndices
        self.temperature=None
        self.simulate_temperature()

    def simulate_temperature(self):
        self.temperature=np.zeros(self.numIndices)
        indicesPerHour=self.numIndices/24
        for i in range(self.numIndices):
            hour=i/indicesPerHour
            self.temperature[i]=self.simulate_temperature_at(self.currentDate,hour)
    
    def simulate_temperature_at(self,date:date,hour:float)->float:
        baseTemp=self.geolocation.get_base_temp()+random.uniform(0, 1)
        amplitude=self.geolocation.get_amplitude_temp()+random.uniform(0, 1)
        hourOffset=10
        seasonOffset=self.geolocation.get_season_offset()
        seasonalVariation=10*math.cos(2*math.pi*(date.timetuple().tm_yday / 365.0)+2*math.pi*(seasonOffset / 365.0))
        dailyVariation=amplitude*math.cos(2*math.pi*(hour / 24.0)+2*math.pi*(hourOffset / 24.0))
        return baseTemp + seasonalVariation + dailyVariation + random.uniform(0, 1)
    
    def change_date(self,date:date):
        self.currentDate=date
        self.simulate_temperature()

    def termic_response(self,insideTemp:float,timestamp:float,timeElapsed:float,superficialArea:float,insideVolume:float)->float:
        termicTransferenceCoef=0.5
        airDensity=1.225
        airCaloricCapacity=1005
        termicCapacityOfInteriorAir=insideVolume*airDensity*airCaloricCapacity
        indexPerMinute=self.numIndices/1440
        index=int(indexPerMinute*timestamp)
        exteriorTemp=self.temperature[index]
        return (exteriorTemp-insideTemp)*(1-math.pow(math.e,-1*((termicTransferenceCoef*superficialArea)/termicCapacityOfInteriorAir)*timeElapsed*60))



