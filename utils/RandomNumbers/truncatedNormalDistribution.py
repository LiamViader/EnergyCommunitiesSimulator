from utils.RandomNumbers.normalDistribution import NormalDistribution
from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution
from typing import List, Tuple, Optional
import numpy as np

class TruncatedNormalDistribution(BaseNumberDistribution):
    def __init__(self,std:float,min:float,max:float,mu:Optional[float]=None) -> None:
        if mu is None:
            mu=(min+max)/2
        self.min=min
        self.max=max
        self.normalDistribution=NormalDistribution(std,mu)


    def generate_random(self) -> float:
        random_number = self.normalDistribution.generate_random()
        return max(min(random_number, self.min), self.max)

