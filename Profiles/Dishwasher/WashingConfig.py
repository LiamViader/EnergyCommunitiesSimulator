import numpy as np
import random
from typing import List
from utils.minuteInterval import MinuteInterval

#properties of how they use the dishwasher
class WashingDishesConfig:
    def __init__(self,timesWeekly:int,intervals:List[MinuteInterval]):
        #intervals is an array of intervals
        self.timesWeekly=timesWeekly #cops que posa rentaplats a la setmana
        self.intervals=np.array(intervals) #les franges a les quals sol posar la rentadora

    def times_weekly(self)->int:
        return self.timesWeekly
    
    def get_random_interval(self)->MinuteInterval:
        return self.intervals[random.randint(0,len(self.intervals)-1)]



