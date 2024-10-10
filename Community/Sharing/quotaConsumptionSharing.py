from Profiles.profile import Profile
from Simulation.simulationConfiguration import SimulationConfig
from Community.Sharing.sharingMethod import SharingMethod
from Community.Sharing.quota import Quota
from Profiles.utils.profileEnergyDataAux import ProfileEnergyDataAux
from Profiles.utils.profileSharingsDataAux import ProfileSharingsDataAux
from typing import List, Dict, Tuple
import numpy as np

class QuotaConsumptionSharing(SharingMethod):
    """
    Implementation of the Quota/Consumption Sharing energy sharing method.

    This method first allocates energy to profiles based on quotas and then reassigns excess energy 
    to cover deficits among profiles. The method allows for two different approaches to redistribute 
    excess energy: based on community shares or based on the proportion of each household's residual load.

    Attributes:
        name (str): The name of the sharing method, set to "Quota/Consumption Sharing".
        
        reassignBasedOnCommunityShares (bool): Determines the method for reallocating excess energy.
    
    Methods:
        share: Shares energy among profiles based on the Quota/Consumption Sharing method.
    """
    def __init__(self,reassignBasedOnCommunityShares:bool=True) -> None:
        """
        Initializes a QuotaConsumptionSharing instance.

        Args:
            reassignBasedOnCommunityShares (bool): Flag to determine how to reassign excess energy.
        """
        super().__init__("Quota/Consumption Sharing")
        self.reassignBasedOnCommunityShares=reassignBasedOnCommunityShares


    def share(self,profiles:List[ProfileEnergyDataAux],sharePersonalPvs:bool,communityPv:float)->List[ProfileSharingsDataAux]:
        """
        Shares energy among profiles based on the Quota/Consumption Sharing method.

        The method first allocates energy using the Quota sharing method, then redistributes excess energy 
        to cover any deficits in consumption.

        Args:
            profiles (List[ProfileEnergyDataAux]): A list of profile energy data that includes load, production, and community share information.
            sharePersonalPvs (bool): Indicates whether to consider personal production in the calculations. 
            communityPv (float): The total energy produced by community PV resources.

        Returns:
            List[ProfileSharingsDataAux]: A list of sharing data for each profile, including grid import/export values.
        
        Notes:
            This method can't share personal pvs, because there is not microtrading
        """
        profilesSharingsList=Quota().share(profiles=profiles,sharePersonalPvs=sharePersonalPvs,communityPv=communityPv) #first step is to do quota sharing
        #now reassign the excedents to cover deficits
        #the paper is not clear about how to redistribute the excedents. if there's more demand than excedents, then how does this method decide which HH gets more or less energy? Same case if there's more excedents than demand, how does the method decide who which HH trades sells more or less energy.
        #There is 2 ways to do it. Based on the communityShares or based on the HHs proportion of HHnresidual/totalResidual. I implemented both, use the attribute reassignBasedOnCommunityShares in the init method to choose which way to do it
        if self.reassignBasedOnCommunityShares:
            return self._reassign_based_on_shares(profilesSharingsList=profilesSharingsList)            
        else:
            return self._reassign_based_on_proportion(profilesSharingsList=profilesSharingsList)


    def _reassign_based_on_shares(self,profilesSharingsList:List[ProfileSharingsDataAux])->List[ProfileSharingsDataAux]:
        """
        Reassigns excess energy based on community shares.

        Args:
            profilesSharingsList (List[ProfileSharingsDataAux]): A list of profile sharing data to redistribute excess energy.

        Returns:
            List[ProfileSharingsDataAux]: The updated list of sharing data with reallocated energy values.
        """
        totalExport=0
        totalExportingShares=0
        totalImportingShares=0
        totalImport=0
        for profileSharingsData in profilesSharingsList:
            if profileSharingsData.gridExport>0:
                totalExport+=profileSharingsData.gridExport
                totalExportingShares+=profileSharingsData.communityShares
            elif profileSharingsData.gridImport>0:
                totalImport+=profileSharingsData.gridImport
                totalImportingShares+=profileSharingsData.communityShares
        for profileSharingsData in profilesSharingsList:
            if totalImport>totalExport:
                if profileSharingsData.gridExport>0:
                    profileSharingsData.microgridExport=profileSharingsData.gridExport
                    profileSharingsData.gridExport=0
                elif profileSharingsData.gridImport>0:
                    if totalImportingShares!=0: shareProportionToImportingProfiles=profileSharingsData.communityShares/totalImportingShares
                    else: shareProportionToImportingProfiles=0
                    profileSharingsData.microgridImport=totalExport*shareProportionToImportingProfiles
                    profileSharingsData.gridImport=profileSharingsData.gridImport-profileSharingsData.microgridImport
            else:
                if profileSharingsData.gridExport>0:
                    if totalExportingShares!=0: shareProportionToExportingProfiles=profileSharingsData.communityShares/totalExportingShares
                    else: shareProportionToExportingProfiles=0
                    profileSharingsData.microgridExport=totalImport*shareProportionToExportingProfiles
                    profileSharingsData.gridExport=profileSharingsData.gridExport-profileSharingsData.microgridExport
                elif profileSharingsData.gridImport>0:
                    profileSharingsData.microgridImport=profileSharingsData.gridImport
                    profileSharingsData.gridImport=0
        return profilesSharingsList
    
    def _reassign_based_on_proportion(self,profilesSharingsList:List[ProfileSharingsDataAux])->List[ProfileSharingsDataAux]:
        """
        Reassigns excess energy based on the proportion of each household's residual load.

        Args:
            profilesSharingsList (List[ProfileSharingsDataAux]): A list of profile sharing data to redistribute excess energy.

        Returns:
            List[ProfileSharingsDataAux]: The updated list of sharing data with reallocated energy values.
        """
        #I think reassigning this way is the same than using Virtual Net Billing
        totalExport=0
        totalImport=0
        for profileSharingsData in profilesSharingsList:
            if profileSharingsData.gridExport>0:
                totalExport+=profileSharingsData.gridExport
            elif profileSharingsData.gridImport>0:
                totalImport+=profileSharingsData.gridImport

        for profileSharingsData in profilesSharingsList:
            if totalImport>totalExport:
                if profileSharingsData.gridExport>0:
                    profileSharingsData.microgridExport=profileSharingsData.gridExport
                    profileSharingsData.gridExport=0
                elif profileSharingsData.gridImport>0:
                    profileSharingsData.microgridImport=(profileSharingsData.gridImport/totalImport)*totalExport
                    profileSharingsData.gridImport=profileSharingsData.gridImport-profileSharingsData.microgridImport
            else:
                if profileSharingsData.gridExport>0:
                    profileSharingsData.microgridExport=(profileSharingsData.gridExport/totalExport)*totalImport
                    profileSharingsData.gridExport=profileSharingsData.gridExport-profileSharingsData.microgridExport
                elif profileSharingsData.gridImport>0:
                    profileSharingsData.microgridImport=profileSharingsData.gridImport
                    profileSharingsData.gridImport=0
        return profilesSharingsList


                

