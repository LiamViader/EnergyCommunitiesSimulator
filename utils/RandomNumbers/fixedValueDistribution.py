from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution
from typing import List, Tuple
import numpy as np

class FixedValueDistribution(BaseNumberDistribution):
    def __init__(self,value:float) -> None:
        self.value=value


    def generate_random(self) -> float:
        return self.value

