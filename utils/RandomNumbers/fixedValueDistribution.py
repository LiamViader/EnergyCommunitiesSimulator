from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution
from typing import List, Tuple
import numpy as np

class FixedValueDistribution(BaseNumberDistribution):
    """
    Class representing a fixed value distribution.

    This class generates number that is always equal to a predefined fixed value.

    Attributes:
        _value (float): The fixed value that will be returned by the generator.
    
    Methods:
        generate_random() -> float: Returns the fixed value.
    """
    def __init__(self,value:float) -> None:
        """
        Initializes the fixed value distribution with a specified value.

        Args:
            value (float): The fixed value to be used by the distribution.
        """
        self._value=value


    def generate_random(self) -> float:
        """
        Returns a fixed number.

        This method overrides the abstract method from the base class and returns
        the fixed value set during initialization.

        Returns:
            float: The fixed value specified when creating the instance.
        """
        return self._value

