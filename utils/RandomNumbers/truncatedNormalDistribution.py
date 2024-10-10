from utils.RandomNumbers.normalDistribution import NormalDistribution
from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution
from typing import List, Tuple, Optional
import numpy as np

class TruncatedNormalDistribution(BaseNumberDistribution):
    """
    Class representing a truncated normal distribution.

    This class generates random numbers from a normal distribution that are then truncated 
    to lie within a specified minimum and maximum range.

    Attributes:
        _min (float): The minimum value for truncation.

        _max (float): The maximum value for truncation.
        
        _normalDistribution (NormalDistribution): An instance of NormalDistribution used to generate normal random numbers.

    Methods:
        generate_random() -> float: Generates and returns a random number drawn from the truncated normal distribution.
    """
    def __init__(self,std:float,min:float,max:float,mu:Optional[float]=None) -> None:
        """
        Initializes the truncated normal distribution with specified parameters.

        If the mean (mu) is not provided, it is set to the midpoint of the specified min and max values.

        Args:
            std (float): The standard deviation of the normal distribution.
            min (float): The minimum value to which random numbers will be truncated.
            max (float): The maximum value to which random numbers will be truncated.
            mu (Optional[float]): The mean of the normal distribution. If None, defaults to the midpoint of min and max.
        """
        if mu is None:
            mu=(min+max)/2
        self._min=min
        self._max=max
        self._normalDistribution=NormalDistribution(std,mu)


    def generate_random(self) -> float:
        """
        Generate a random number.

        This method overrides the abstract method from the base class and returns
        a random number drawn from a truncated normal distribution, ensuring that the value
        lies within the defined minimum and maximum limits.

        Returns:
            float: A random number selected from the truncated normal distribution.
        """
        random_number = self._normalDistribution.generate_random()
        return max(min(random_number, self._max), self._min)

