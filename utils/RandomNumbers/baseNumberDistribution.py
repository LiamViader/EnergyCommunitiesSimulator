from abc import ABC, abstractmethod

class BaseNumberDistribution(ABC):
    """
    Abstract base class for number distribution generators.

    This class serves as a template for creating various types of number distributions. 
    Subclasses must implement the `generate_random` method to generate random numbers 
    according to the specific distribution.

    Methods:
        generate_random() -> float: Generates a random number based on the distribution.
    """
    def __init__(self) -> None:
        """
        Initializes the base number distribution.

        This constructor does not perform any specific operations.
        """
        pass

    @abstractmethod
    def generate_random(self)->float:
        """
        Generate a random number.

        This method must be implemented by subclasses to return a random number
        based on the specific distribution logic.

        Returns:
            float: A randomly generated number.
        """
        pass