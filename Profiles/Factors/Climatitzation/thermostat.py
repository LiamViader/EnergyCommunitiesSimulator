from typing import List, Tuple
from utils.minuteInterval import MinuteInterval

class Thermostat:
    def __init__(self,idealTemperatures:List[Tuple[MinuteInterval,float]],startingTemperature:float=21) -> None:
        self.currentTemperature=startingTemperature
        self.idealTemperatures=idealTemperatures

    def get_current_temperature(self)->float:
        return self.currentTemperature
    
    def set_current_temperature(self,newTemp)->None:
        self.currentTemperature=newTemp

    def get_ideal_temperature(self,timestamp)->float:
        for idealTemperatures in self.idealTemperatures:
            if idealTemperatures[0].contains(timestamp):
                return idealTemperatures[1]