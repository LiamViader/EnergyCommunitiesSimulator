from utils.minuteInterval import MinuteInterval
from utils.enums import Granularity
from Profiles.loadConfiguration import LoadConfig
import math
import numpy as np
import pandas as pd


class SolarIrradiation:
    def __init__(self, latitude:float,longitude:float,longitudeCentralMeridian:float,loadConfig:LoadConfig):
        self.latitude=latitude
        self.longitude=longitude
        self.longitudeCentralMeridian=longitudeCentralMeridian
        self.loadConfig=loadConfig
        self.simulatedIrradiation=None
        self.simulate_irradiation()
    

    def simulate_irradiation(self):
        self.simulatedIrradiation=np.zeros(self.loadConfig.num_indices())
        for i in range(365):#simula els 365 dies de l'any
            B=(360/365)*(i-81)
            eot=9.87*math.sin(2*B)-7.53*math.cos(B)-1.5*math.sin(B)
            solarDeclination=23.45*math.sin((B))
            extraterrester_solar_irrad=1361*(1+0.033*math.cos((360-i)/365))
            for j in range(self.loadConfig.num_indices()):
                hour=(24/self.loadConfig.num_indices())*j
                solar_hour=solar_hour(hour,eot)
                hour_angle=15*(solar_hour-12)
                cos_cenital_solar_angle=math.sin(self.latitude)*math.sin(solarDeclination)+math.cos(solarDeclination)*math.cos(self.latitude)*math.cos(hour_angle)
                irradiation=extraterrester_solar_irrad*cos_cenital_solar_angle
                self.simulatedIrradiation[j]=irradiation/1000 #divideixo entr 1000 perque estigui en kw/m2 que sino esta en w/m2
        self.simulatedIrradiation=self.simulatedIrradiation/365
        serie=pd.Series(self.simulatedIrradiation)
        serie.to_excel("AAAAAAA.xlsx")
                 
    
    def solar_hour(self,localHour, eot)->float:
        return localHour+((self.longitude-self.longitude_central_meridian)/15)+eot
    
