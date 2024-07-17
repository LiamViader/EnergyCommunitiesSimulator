import numpy as np
from datetime import date
from typing import Tuple
import math

class Wind:
    def __init__(self,indices:int,currentDate:date) -> None:
        self.wind=None
        self.indices=indices
        self.currentDate=currentDate
        self.simulate_wind()

    def simulate_wind(self)->None:
        season=self.get_season()
        windHour=np.zeros(24)

        for hour in range(24):
            mean,std=self.get_mean_std(hour,season)
            windHour[hour] = max(np.random.normal(mean, std),0.5)
        
        self.wind=np.zeros(self.indices)
        for i in range(24):
            start_index = i * (self.indices // 24)
            end_index = (i + 1) * (self.indices // 24)
            if i == 23:  # Para el último intervalo, asegurarse de llegar al final
                end_index = self.indices
            # Interpolar entre windHour[i] i windHour[i + 1]
            next_wind = windHour[(i + 1) % 24] 
            self.wind[start_index:end_index] = np.linspace(windHour[i], next_wind, end_index - start_index)
        print(self.wind)
            
            

    def get_wind(self)->np.ndarray:
        return self.wind
    
    def change_date(self,date:date):
        self.currentDate=date
        self.simulate_wind()
    
    def get_season(self):
        month=self.currentDate.month
        if 3 <= month <= 5:
            return 'SPRING'
        elif 6 <= month <= 8:
            return 'SUMMER'
        elif 9 <= month <= 11:
            return 'AUTUMN'
        else:
            return 'WINTER'
    
    def get_mean_std(self,hour:int,season:str)->Tuple[float,float]:
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