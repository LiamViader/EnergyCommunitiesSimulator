from abc import ABC, abstractmethod

class BaseNumberDistribution(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def generate_random(self)->float:
        pass