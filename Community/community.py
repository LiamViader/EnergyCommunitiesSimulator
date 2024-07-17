from Profiles.profile import Profile
from Community.communityConfiguration import CommunityConfig
from Profiles.profileConfiguration import ProfileConfig
from typing import List
import pandas as pd

class Community():
    def __init__(self,profiles:List[Profile]) -> None:
        self.profiles=profiles
        self.simulatedCommunity={}
        self.configLastSimulation=None


    def simulate(self,communityConfig:CommunityConfig)->None:
        for profile in self.profiles:
            config=ProfileConfig(communityConfig=communityConfig)
            profile.simulate(profileConfig=config)
        self.simulatedCommunity=communityConfig.share(self.profiles)
        self.configLastSimulation=communityConfig

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
