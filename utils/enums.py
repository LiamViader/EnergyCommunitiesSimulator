from enum import Enum

class Granularity(Enum):
    Hour = 1
    Minute = 2

class LoadType(Enum):
    Consumer=1
    Producer=2