from Profiles.profile import Profile
from Simulation.simulationConfiguration import SimulationConfig
from Community.Sharing.sharingMethod import SharingMethod
from Profiles.utils.profileEnergyDataAux import ProfileEnergyDataAux
from Profiles.utils.profileSharingsDataAux import ProfileSharingsDataAux
from typing import List, Dict, Tuple
import numpy as np

class Quota(SharingMethod):
    def __init__(self) -> None:
        super().__init__("Quota")

    def share(self,profiles:List[ProfileEnergyDataAux],sharePersonalPvs:bool,communityPv:float)->List[ProfileSharingsDataAux]: #this method can't share personal pvs, because there is not microtrading
        if sharePersonalPvs:
            print("this method can't share personal pvs")
        profileSharingsList:List[ProfileSharingsDataAux]=[]
        for profile in profiles:
            profileSharingsData=ProfileSharingsDataAux(profile_id=profile.id)
            profileSharingsData.communityShares=profile.share
            residualLoad=profile.load-profile.production
            if residualLoad<0:
                profileSharingsData.personalPvExcedent=abs(residualLoad)
                residualLoad=0
            assignedPv=profile.share*communityPv
            profileSharingsData.totalPvAbleToShare=assignedPv
            residualLoad=residualLoad-assignedPv
            if residualLoad<0:
                profileSharingsData.gridExport=abs(residualLoad)
            else:
                profileSharingsData.gridImport=residualLoad
            profileSharingsList.append(profileSharingsData)
        return profileSharingsList
                

