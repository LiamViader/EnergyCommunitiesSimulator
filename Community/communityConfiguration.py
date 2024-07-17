import numpy as np
import pandas as pd
from utils.geolocation import Geolocation
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.Factors.Climatitzation.temperature import Temperature
from typing import List, Dict
from Profiles.profile import Profile
from utils.enums import Granularity
from datetime import date, timedelta
from Community.Sharing.sharingMethod import SharingMethod
from Community.Sharing.virtualNetBilling import VirtualNetBilling

#config of the load
class CommunityConfig:
    def __init__(self,granularity:Granularity=Granularity.Hour,
                 currentDate:date=date(2024,1,1),
                 geolocation:Geolocation=Geolocation("Madrid, Spain"),
                 sharingMethod:SharingMethod=VirtualNetBilling()):
        
        self.currentDate=currentDate
        self.granularity=granularity
        self.geolocation=geolocation
        self.sharingMethod=sharingMethod

        if granularity==Granularity.Hour:
            self.indices=24
        elif granularity==Granularity.Minute:
            self.indices=1440
        elif granularity==Granularity.FifteenMinutes:
            self.indices=24*4
        
        self.solarIrradiation=SolarIrradiation(geolocation=self.geolocation,numIndices=self.indices, currentDate=self.currentDate)
        self.temperature=Temperature(self.geolocation,self.indices,self.currentDate)

    def num_indices(self) -> int: 
        return self.indices
    
    def get_time_series(self) -> pd.Series:
        if self.granularity == Granularity.Hour:
            index_start = pd.date_range('00:00', periods=self.indices, freq='h')
            index_end = index_start + pd.DateOffset(hours=1)
        elif self.granularity == Granularity.Minute:
            index_start = pd.date_range('00:00', periods=self.indices, freq='min')
            index_end = index_start + pd.DateOffset(minutes=1)
        elif self.granularity==Granularity.FifteenMinutes:
            index_start = pd.date_range('00:00', periods=self.indices, freq='15min')
            index_end = index_start + pd.DateOffset(minutes=15)

        index_str = index_start.strftime('%H:%M') + '-' + index_end.strftime('%H:%M')
        return pd.Series( data=range(self.indices), index=index_str)
    
    def get_current_date(self)->date:
        return self.currentDate
    
    def get_irradiation(self)->np.ndarray:
        return self.solarIrradiation.get_irradiation()
    
    def step_one_day(self):
        self.currentDate=self.currentDate + timedelta(days=1)
        self.solarIrradiation.change_date(self.currentDate)
        self.temperature.change_date(self.currentDate)

    def get_day_of_week(self):
        return self.currentDate.weekday()
    
    def outside_termic_response(self,currentInsideTemp:float,timestamp:float,timeElapsed:float,superficialArea:float,insideVolume:float)->float:
        return self.temperature.termic_response(currentInsideTemp,timestamp,timeElapsed,superficialArea,insideVolume)
    
    def share(self,profiles:List[Profile])->Dict[Profile,Dict[str,np.ndarray]]:
        return self.sharingMethod.share(profiles,self)
    
    def get_str_date(self):
        return self.currentDate.strftime('%Y_%m_%d')