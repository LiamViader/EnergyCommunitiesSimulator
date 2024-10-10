from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution
from typing import List, Tuple
import numpy as np

class PiecewiseUniformDistribution(BaseNumberDistribution):
    """
    Class representing a piecewise uniform distribution.

    This class generates random numbers based on specified ranges and their associated probabilities.
    Each range has an associated probability, determining the likelihood of generating a number from that range.

    Attributes:
        _ranges (List[Tuple[float, float]]): A list of tuples representing the ranges for the distribution.
        
        _probabilities (List[float]): A list of probabilities associated with each range. The probabilities must sum to 1.

    Methods:
        generate_random() -> float: Generates and returns a random number drawn from the piecewise uniform distribution.
    """
    def __init__(self,ranges:List[Tuple[float,float]],probabilities:List[float]) -> None:
        """
        Initializes the piecewise uniform distribution with specified ranges and their probabilities.

        Args:
            ranges (List[Tuple[float, float]]): A list of tuples where each tuple defines a range (min, max).
            probabilities (List[float]): A list of probabilities corresponding to each range. Must sum to 1.
        """
        self._ranges=ranges
        self._probabilities=probabilities


    def generate_random(self) -> float:
        """
        Generate a random number.

        This method overrides the abstract method from the base class and returns
        a random number drawn from one of the specified ranges according to the defined probabilities.

        Returns:
            float: A random number selected from the piecewise uniform distribution.
        """
        selected_range=np.random.choice(len(self._ranges), p=self._probabilities)
        min_range, max_range= self._ranges[selected_range]
        generated_number= np.random.uniform(min_range,max_range)
        return generated_number

