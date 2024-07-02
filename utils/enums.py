from enum import Enum

class Granularity(Enum):
    Hour = 'hour'
    Minute = 'minute'

class FactorType(Enum):
    Consumer=1
    Producer=2