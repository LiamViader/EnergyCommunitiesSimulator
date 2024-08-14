import pandas as pd
import numpy as np
import random
from typing import Tuple
from Profiles.Factors.baseFactor import BaseFactor
from Profiles.profileConfiguration import ProfileConfig
from Profiles.Factors.Continuos.continuosCyclicModel import ContinuosCyclicModel
from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution
from utils.enums import FactorType


class ContinuosFactor(BaseFactor):
    def __init__(self, name: str, factorType: FactorType, constantPower:BaseNumberDistribution):
        super().__init__(name, factorType)
        self.constant_power=constantPower
    
    def simulate(self, profileConfig: ProfileConfig) -> np.ndarray:
        load=np.zeros(profileConfig.num_indices())
        hoursPerIndex=24/profileConfig.num_indices()
        for i in range(profileConfig.num_indices()):
            load[i]+=self.constant_power.generate_random()*hoursPerIndex
        return load