import numpy as np
import pandas as pd
from utils.enums import Granularity
from datetime import date

#config of the load
class ProfileConfig:
    def __init__(self,granularity:Granularity=Granularity.Hour,currentDate:date=date(2024,1,1)):
        self.currentDate=currentDate
        self.granularity=granularity
        if granularity==Granularity.Hour:
            self.indices=24
        elif granularity==Granularity.Minute:
            self.indices=1440

    def num_indices(self) -> int: 
        return self.indices
    
    def get_time_series(self) -> pd.Series:
        if self.granularity == Granularity.Hour:
            index = pd.date_range('00:00', periods=self.indices, freq='h').time
        elif self.granularity == Granularity.Minute:
            index = pd.date_range('00:00', periods=self.indices, freq='min').time

        return pd.Series( data=range(self.indices), index=index)
    
    def get_current_date(self)->date:
        return self.currentDate