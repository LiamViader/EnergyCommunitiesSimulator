from Profiles.profileConfiguration import ProfileConfig
from utils.geolocation import Geolocation
from datetime import datetime, timedelta, date
import math
import numpy as np
import pandas as pd


class SolarIrradiation:
    #simulated solar irradiation in a geolocalitzation and year averaged over the year
    def __init__(self, geolocation:Geolocation,current_date:date,profileConfig:ProfileConfig):
        self.geolocation=geolocation
        self.current_date=current_date
        self.profileConfig=profileConfig
        self.simulatedIrradiation=None #en kw/m2
        self.simulate_irradiation()
    
    def simulate_irradiation(self):
        self.simulatedIrradiation=np.zeros(self.profileConfig.num_indices())
        julianDay=self.current_date.timetuple().tm_yday-1
        B=(360/365)*(julianDay-81)
        solarDeclination=23.45*math.sin(math.radians(B))
        extraterrester_solar_irrad=1361*(1+0.033*math.cos(math.radians((360-julianDay)/365)))
        for j in range(self.profileConfig.num_indices()):
            hour=(24/self.profileConfig.num_indices())*j
            localDatetime=self.build_datetime_from_hour(hour)
            solar_angle=self.geolocation.solar_angle(localDatetime)
            cos_cenital_solar_angle=math.sin(math.radians(self.geolocation.get_latitude()))*math.sin(math.radians(solarDeclination))+math.cos(math.radians(solarDeclination))*math.cos(math.radians(self.geolocation.get_latitude()))*math.cos(math.radians(solar_angle))
            irradiation=extraterrester_solar_irrad*cos_cenital_solar_angle
            irradiation=max(irradiation,0) #per no agafar valors negatius
            self.simulatedIrradiation[j]+=irradiation/1000 #divideixo entr 1000 perque estigui en kw/m2 que sino esta en w/m2
    
    def get_irradiation(self):
        return self.simulatedIrradiation

    def build_datetime_from_hour(self, hour_decimal):
        hours = int(hour_decimal)
        minutes = int((hour_decimal - hours) * 60)
        seconds = int(((hour_decimal - hours) * 60 - minutes) * 60)
        microseconds = int((((hour_decimal - hours) * 60 - minutes) * 60 - seconds) * 1e6)
        return datetime(self.current_date.year,self.current_date.month,self.current_date.day,hours, minutes, seconds, microseconds)             