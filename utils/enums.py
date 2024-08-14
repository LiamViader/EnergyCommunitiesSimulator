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

class LightType(Enum):
    Led=1
    Cfl=2
    Incandescent=3
    Halogen=4
    FluorescentTube=5
    Neon=6

class MarketCountry(Enum):
    Spain=1
    Portugal=2