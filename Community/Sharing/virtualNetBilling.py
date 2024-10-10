from Profiles.profile import Profile
from Simulation.simulationConfiguration import SimulationConfig
from Community.Sharing.sharingMethod import SharingMethod
from Profiles.utils.profileEnergyDataAux import ProfileEnergyDataAux
from Profiles.utils.profileSharingsDataAux import ProfileSharingsDataAux
from typing import List, Dict, Tuple
import numpy as np

class VirtualNetBilling(SharingMethod):
    """
    Implementation of the Virtual Net Billing energy sharing method.

    This method calculates the energy sharing among profiles based on a virtual net billing system.

    Attributes:
        name (str): The name of the sharing method, set to "Virtual Net Billing".

    Methods:
        share: Shares energy among profiles based on the Virtual Net Billing method.
    """
    def __init__(self) -> None:
        """
        Initializes a VirtualNetBilling instance.
        """

        super().__init__("Virtual Net Billing")

    def share(self,profiles:List[ProfileEnergyDataAux],sharePersonalPvs:bool,communityPv:float)->List[ProfileSharingsDataAux]:
        """
        Shares energy among profiles based on the Virtual Net Billing method.

        Args:
            profiles (List[ProfileEnergyDataAux]): A list of profile energy data that includes load, production and community share information.
            sharePersonalPvs (bool): Indicates whether to consider personal production in the calculations.
            communityPv (float): The total energy produced by community PV resources.

        Returns:
            List[ProfileSharingsDataAux]: A list of sharing data for each profile, including grid and microgrid import/export values.
        """
        totalToImport=0
        totalToExport=0
        for profileEnergy in profiles:
            if sharePersonalPvs:
                pv=profileEnergy.production+communityPv*profileEnergy.share
                load=profileEnergy.load
            else:
                pv=profileEnergy.share *communityPv
                load=profileEnergy.load-profileEnergy.production
                if load<0:
                    load=0
            residual=load-pv
            if residual>0:
                totalToImport+=residual
            else:
                totalToExport+=abs(residual)
        sharingsList=[]
        for profileEnergy in profiles:
            profileSharings=ProfileSharingsDataAux(profile_id=profileEnergy.id)
            profileSharings.communityShares=profileEnergy.share
            if sharePersonalPvs:
                    pv=profileEnergy.production+communityPv*profileEnergy.share
                    load=profileEnergy.load
                    profileSharings.totalPvAbleToShare=pv
            else:
                pv=profileEnergy.share *communityPv
                load=profileEnergy.load-profileEnergy.production
                if load<0:
                    profileSharings.personalPvExcedent=abs(load)
                    load=0
                profileSharings.totalPvAbleToShare=pv
            residual=load-pv
            if totalToImport>totalToExport:
                if residual>0:
                    if totalToImport!=0: weight=residual/totalToImport #to avoid dividing by 0
                    else: weight=0
                    profileSharings.microgridImport=weight*totalToExport
                    profileSharings.gridImport=residual-profileSharings.microgridImport
                    profileSharings.gridExport=0
                    profileSharings.microgridExport=0
                else:
                    profileSharings.microgridImport=0
                    profileSharings.gridImport=0
                    profileSharings.microgridExport=abs(residual)
                    profileSharings.gridExport=0
            else:
                if residual<0:
                    if totalToExport!=0: weight=abs(residual)/totalToExport #to avoid dividing by 0
                    else: weight=0
                    profileSharings.microgridExport=weight*totalToImport
                    profileSharings.gridExport=abs(residual)-profileSharings.microgridExport
                    profileSharings.gridImport=0
                    profileSharings.microgridImport=0
                else:
                    profileSharings.microgridImport=residual
                    profileSharings.gridImport=0
                    profileSharings.microgridExport=0
                    profileSharings.gridExport=0
            sharingsList.append(profileSharings)
        return sharingsList
                

