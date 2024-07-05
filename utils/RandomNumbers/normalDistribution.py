
from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution
from typing import List, Tuple
import numpy as np

class NormalDistribution(BaseNumberDistribution):
    def __init__(self,std:float,mu:float) -> None:
        self.std=std
        self.mu=mu


    def generate_random(self) -> float:
        random_number = np.random.normal(self.mu, self.std)
        return random_number

