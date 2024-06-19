import numpy as np
import random

#properties of how they use the dishwasher
class WashingDishesConfig:
    def __init__(self,timesWeekly,intervals):
        #intervals és un array de intervals
        self.timesWeekly=timesWeekly #cops que posa rentaplats a la setmana
        self.intervals=np.array(intervals) #les franges a les quals sol posar la rentadora

    def times_weekly(self):
        return self.timesWeekly
    
    def get_random_interval(self):
        return self.intervals[random.randint(0,len(self.intervals)-1)]



