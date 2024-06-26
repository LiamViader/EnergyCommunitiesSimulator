from enum import Enum

class Granularity(Enum):
    Hour = 1
    Minute = 2

class FactorType(Enum):
    Consumer=1
    Producer=2