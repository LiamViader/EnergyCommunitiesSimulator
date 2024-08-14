from abc import ABC, abstractmethod
from typing import Tuple
from Profiles.Factors.Climatitzation.thermostat import Thermostat

class ClimatitzationComponent(ABC):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def climatize(self,thermostat:Thermostat,idealTemperature:float,timeElapsed:float)->Tuple[float,float]:#retorna la carrega (1r element tupla) de climatitzar cap a la temperatura ideal durant timeElapsed, el segon element de la tupla és l'increment o decrement de temperatura. timeElapsed en hores
        pass