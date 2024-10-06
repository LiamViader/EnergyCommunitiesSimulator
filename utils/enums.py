from enum import Enum

class Granularity(Enum):
    """
    Enum representing different granularities of time intervals.

    Attributes:
        Hour (str): Represents a time interval of one hour.
        Minute (str): Represents a time interval of one minute.
        FifteenMinutes (str): Represents a time interval of fifteen minutes.
    """
    Hour = 'hour'
    Minute = 'minute'
    FifteenMinutes = 'fifteenMinutes'

class FactorType(Enum):
    """
    Enum representing different types of energy factors.

    Attributes:
        Consumer (int): Represents a consumer factor.
        Producer (int): Represents a producer factor.
        Prosumer (int): Represents a prosumer factor (both consumer and producer).
        Battery (int): Represents a battery factor.
    """
    Consumer=1
    Producer=2
    Prosumer=3
    Battery=4

class LightType(Enum):
    """
    Enum representing different types of lighting.

    Attributes:
        Led (int): Represents LED lighting.
        Cfl (int): Represents Compact Fluorescent Lamp lighting.
        Incandescent (int): Represents incandescent lighting.
        Halogen (int): Represents halogen lighting.
        FluorescentTube (int): Represents fluorescent tube lighting.
        Neon (int): Represents neon lighting.
    """
    Led=1
    Cfl=2
    Incandescent=3
    Halogen=4
    FluorescentTube=5
    Neon=6

class MarketCountry(Enum):
    """
    Enum representing countries in the energy market.

    Attributes:
        Spain (int): Represents Spain.
        Portugal (int): Represents Portugal.
    """
    Spain=1
    Portugal=2