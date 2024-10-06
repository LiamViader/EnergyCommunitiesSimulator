from typing import List, Tuple
from utils.minuteInterval import MinuteInterval

class Thermostat:
    def __init__(self,idealTemperatures:List[Tuple[MinuteInterval,float]],startingTemperature:float=21) -> None:
        self._currentTemperature=startingTemperature
        self._idealTemperatures=idealTemperatures

    def get_current_temperature(self)->float:
        return self._currentTemperature
    
    def set_current_temperature(self,newTemp)->None:
        self._currentTemperature=newTemp

    def get_ideal_temperature(self,timestamp)->float:
        for idealTemperatures in self._idealTemperatures:
            if idealTemperatures[0].contains(timestamp):
                return idealTemperatures[1]