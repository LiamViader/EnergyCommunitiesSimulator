from Profiles.profile import Profile
from Community.communityConfiguration import CommunityConfig
from Profiles.profileConfiguration import ProfileConfig
from typing import List, Dict
from abc import ABC, abstractmethod
import numpy as np

class SharingMethod(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def share(self,profiles:List[Profile],communityConfig:CommunityConfig)->Dict[Profile,Dict[str,np.ndarray]]:
        pass