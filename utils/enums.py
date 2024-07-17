from enum import Enum

class Granularity(Enum):
    Hour = 'hour'
    Minute = 'minute'
    FifteenMinutes = 'fifteenMinutes'

class FactorType(Enum):
    Consumer=1
    Producer=2
    Prosumer=3
    Battery=4