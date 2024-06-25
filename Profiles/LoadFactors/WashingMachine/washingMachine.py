import pandas as pd
import numpy as np
import random
from Profiles.LoadFactors.loadFactor import LoadFactor
from Profiles.LoadFactors.useConfig import UseConfig
from Profiles.profileConfiguration import ProfileConfig
from utils.enums import LoadType

#properties of the dishwasher
class WashingMachine(LoadFactor):
    def __init__(self,name:str,
                 cycleLoad:float, 
                 cycleTime:int, 
                 washingConfig:UseConfig):
        
        super().__init__(name,LoadType.Consumer)
        self.cycleLoad=cycleLoad #consum del cicle de rentat en kwh
        self.cycleTime=cycleTime #temps que dura el cicle de rentat en minuts
        self.washingConfig=washingConfig #config de rentat (dies setmana, franges horaries..)

    def generate_load(self,profileConfig:ProfileConfig)->pd.Series:
        pass

    def changeWashingConfig(self,washingConfig:UseConfig):
        self.washingConfig=washingConfig


