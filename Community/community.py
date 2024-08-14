from Profiles.profile import Profile
from utils.enums import FactorType
from Community.communityConfiguration import CommunityConfig
from Community.Sharing.sharingMethod import SharingMethod
from Community.Sharing.virtualNetBilling import VirtualNetBilling
from Profiles.profileConfiguration import ProfileConfig
from Profiles.Factors.baseFactor import BaseFactor
from EnergyPrice.EnergyPlans.baseEnergyPlan import BaseEnergyPlan
from typing import List, Tuple, Optional
import pandas as pd
import numpy as np

class Community():
    def __init__(self,profiles:List[Tuple[Profile,float]],
                 communityAssets:List[BaseFactor],
                 sharingMethod:SharingMethod=VirtualNetBilling(),
                 energyPlan:Optional[BaseEnergyPlan]=None) -> None:
        
        self.profiles=profiles
        self.communityAssets=communityAssets
        self.energyPlan=energyPlan
        self.pv=None
        self.sharingMethod=sharingMethod
        self.simulatedCommunity={}
        self.configLastSimulation=None


    def simulate(self,communityConfig:CommunityConfig)->None:
        self.pv=np.zeros(communityConfig.num_indices())
        for asset in self.communityAssets:
            assetLoad=asset.simulate(profileConfig=ProfileConfig(communityConfig=communityConfig))
            if asset.get_factor_type()==FactorType.Producer:
                self.pv+=assetLoad
        

        for profile, ownership in self.profiles:
            config=ProfileConfig(communityConfig=communityConfig)
            profile.simulate(profileConfig=config)
        self.share(communityConfig)
        self.configLastSimulation=communityConfig

    def share(self,communityConfig:CommunityConfig)->None:
        self.simulatedCommunity=self.sharingMethod.share(profiles=self.profiles,communityConfig=communityConfig,communityPv=self.pv)

    def export_sharings_to_excel(self):
        if self.configLastSimulation is not None:
            df=pd.DataFrame()
            timeSeries=self.configLastSimulation.get_time_series()
            df["TimeStamp"] = timeSeries.index
            for profile, data in self.simulatedCommunity.items():
                profileName=profile.get_name()
                for columnName, columnData in data.items():
                    serie=pd.Series(columnData)
                    df[f"{profileName}_{columnName}"]=serie
            df.to_excel(f"DataOutputs/Community/{self.configLastSimulation.get_str_date()}.xlsx")
        else: raise ValueError("theres no simulated load")
