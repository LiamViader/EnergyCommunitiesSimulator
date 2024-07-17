from Profiles.profile import Profile
from Community.communityConfiguration import CommunityConfig
from Community.Sharing.sharingMethod import SharingMethod
from Community.Sharing.virtualNetBilling import VirtualNetBilling
from Profiles.profileConfiguration import ProfileConfig
from typing import List
import pandas as pd

class Community():
    def __init__(self,profiles:List[Profile],sharingMethod:SharingMethod=VirtualNetBilling()) -> None:
        self.profiles=profiles
        self.sharingMethod=sharingMethod
        self.simulatedCommunity={}
        self.configLastSimulation=None


    def simulate(self,communityConfig:CommunityConfig)->None:
        for profile in self.profiles:
            config=ProfileConfig(communityConfig=communityConfig)
            profile.simulate(profileConfig=config)
        self.simulatedCommunity=communityConfig.share(self.profiles)
        self.configLastSimulation=communityConfig

    def share(self,communityConfig:CommunityConfig)->None:
        self.simulatedCommunity=self.sharingMethod.share(profiles=self.profiles,communityConfig=communityConfig)

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
            df.to_excel(f"DataOutputs/Community/{self.configLastSimulation.get_str_date()}")
        else: raise ValueError("theres no simulated load")
