from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution
from typing import List, Tuple
import numpy as np

class PiecewiseUniformDistribution(BaseNumberDistribution):
    def __init__(self,ranges:List[Tuple[float,float]],probabilities:List[float]) -> None:
        self.ranges=ranges
        self.probabilities=probabilities


    def generate_random(self) -> float:
        selected_range=np.random.choice(len(self.ranges), p=self.probabilities)
        min_range, max_range= self.ranges[selected_range]
        generated_number= np.random.uniform(min_range,max_range)
        return generated_number

