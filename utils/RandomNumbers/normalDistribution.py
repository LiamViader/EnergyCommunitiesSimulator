
from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution
from typing import List, Tuple
import numpy as np

class NormalDistribution(BaseNumberDistribution):
    """
    Class representing a normal (Gaussian) distribution.

    This class generates random numbers following a normal distribution
    characterized by a specified mean (mu) and standard deviation (std).

    Attributes:
        _std (float): The standard deviation of the normal distribution.
        _mu (float): The mean (average) value of the normal distribution.
    
    Methods:
        generate_random() -> float: Generates and returns a random number following the normal distribution.
    """
    def __init__(self,std:float,mu:float) -> None:
        """
        Initializes the normal distribution with specified standard deviation and mean.

        Args:
            std (float): The standard deviation of the normal distribution.
            mu (float): The mean value of the normal distribution.
        """
        self._std=std
        self._mu=mu


    def generate_random(self) -> float:
        """
        Generate a random number.

        This method overrides the abstract method from the base class and returns
        a random number drawn from the normal distribution defined by the specified
        mean and standard deviation.

        Returns:
            float: A random number following the normal distribution.
        """
        random_number = np.random.normal(self._mu, self._std)
        return random_number

