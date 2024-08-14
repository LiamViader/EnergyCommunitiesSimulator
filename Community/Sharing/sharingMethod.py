from Profiles.profile import Profile
from Community.communityConfiguration import CommunityConfig
from typing import List, Dict, Tuple
from abc import ABC, abstractmethod
import numpy as np

class SharingMethod(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def share(self,profiles:List[Tuple[Profile,float]],communityConfig:CommunityConfig,communityPv:np.ndarray)->Dict[Profile,Dict[str,np.ndarray]]:
        pass