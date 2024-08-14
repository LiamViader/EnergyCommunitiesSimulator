import numpy as np
import random
from typing import List,Tuple
from utils.minuteInterval import MinuteInterval
from Profiles.Factors.Cyclic.cyclicModel import CyclicModel
from Profiles.profileConfiguration import ProfileConfig
from abc import ABC, abstractmethod


class CyclicBaseUseConfig(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def use(self,cyclicModel:CyclicModel,profileConfig:ProfileConfig)->Tuple[np.ndarray,np.ndarray]:
        pass




