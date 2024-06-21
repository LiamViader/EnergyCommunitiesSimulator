from utils.minuteInterval import MinuteInterval
import math


class SolarIrradiation:
    def __init__(self, irradianceInterval:MinuteInterval,irradiancePeak:float):
        self.irradianceInterval=irradianceInterval
        self.irradiancePeak=irradiancePeak
    

    def irradiate(self,t)->float:
        H = (2 * math.pi / 1440) * (t - (self.irradianceInterval.start_minute() + self.irradianceInterval.end_minute()) / 2)
        return self.irradiancePeak * math.sin(math.pi / 2 * math.cos(math.pi * H / 2))
 