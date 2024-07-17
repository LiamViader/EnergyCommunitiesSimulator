import numpy as np
import pandas as pd
from Community.communityConfiguration import CommunityConfig
from datetime import date, timedelta

#config of the load
class ProfileConfig:
    def __init__(self,communityConfig:CommunityConfig):
        
        self.communityConfig=communityConfig
        self.exteriorContactArea=50
        self.insideVolume=150

    def num_indices(self) -> int: 
        return self.communityConfig.num_indices()
    
    def get_time_series(self) -> pd.Series:
        return self.communityConfig.get_time_series()
    
    def get_current_date(self)->date:
        return self.communityConfig.get_current_date()
    
    def get_irradiation(self)->np.ndarray:
        return self.communityConfig.get_irradiation()
    
    def step_one_day(self):
        self.communityConfig.step_one_day()

    def get_day_of_week(self):
        return self.communityConfig.get_day_of_week()
    
    def outside_termic_response(self,currentInsideTemp:float,timestamp:float,timeElapsed:float)->float:
        return self.communityConfig.outside_termic_response(currentInsideTemp,timestamp,timeElapsed,self.exteriorContactArea,self.insideVolume)
    
    def set_properties(self,exteriorContactArea:float,insideVolume:float):
        self.exteriorContactArea=exteriorContactArea
        self.insideVolume=insideVolume

    def get_wind(self)->np.ndarray:
        return self.communityConfig.get_wind()