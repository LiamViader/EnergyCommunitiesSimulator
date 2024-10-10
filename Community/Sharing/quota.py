from Profiles.profile import Profile
from Simulation.simulationConfiguration import SimulationConfig
from Community.Sharing.sharingMethod import SharingMethod
from Profiles.utils.profileEnergyDataAux import ProfileEnergyDataAux
from Profiles.utils.profileSharingsDataAux import ProfileSharingsDataAux
from typing import List, Dict, Tuple
import numpy as np

class Quota(SharingMethod):
    """
    Implementation of the Quota energy sharing method.

    This method facilitates the sharing of energy among profiles based on fixed quotas assigned to each profile.
    It calculates how much energy each profile can import or export based on their individual production, load, and community shares.

    Attributes:
        name (str): The name of the sharing method, set to "Quota".
    
    Methods:
        share: Shares energy among profiles based on the Quota method.
    """
    def __init__(self) -> None:
        """
        Initializes a Quota instance.
        """
        super().__init__("Quota")

    def share(self,profiles:List[ProfileEnergyDataAux],sharePersonalPvs:bool,communityPv:float)->List[ProfileSharingsDataAux]: #this method can't share personal pvs, because there is not microtrading
        """
        Shares energy among profiles based on the Quota method.

        It allocates a portion of community PV to each profile based on their share, 
        and calculates any residual load that needs to be imported or can be exported to the grid.

        Args:
            profiles (List[ProfileEnergyDataAux]): A list of profile energy data that includes load, production, and community share information.
            sharePersonalPvs (bool): Indicates whether to consider personal production in the calculations. This method does not support personal PV sharing.
            communityPv (float): The total energy produced by community PV resources.

        Returns:
            List[ProfileSharingsDataAux]: A list of sharing data for each profile, including grid import/export values.

        Notes:
            This method can't share personal pvs, because there is not any microtrading
        """
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
                

