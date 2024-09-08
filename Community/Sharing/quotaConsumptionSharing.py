from Profiles.profile import Profile
from Simulation.simulationConfiguration import SimulationConfig
from Community.Sharing.sharingMethod import SharingMethod
from Community.Sharing.quota import Quota
from Profiles.utils.profileEnergyDataAux import ProfileEnergyDataAux
from Profiles.utils.profileSharingsDataAux import ProfileSharingsDataAux
from typing import List, Dict, Tuple
import numpy as np

class QuotaConsumptionSharing(SharingMethod):
    def __init__(self,reassignBasedOnCommunityShares:bool=True) -> None:
        super().__init__("Quota/Consumption Sharing")
        self.reassignBasedOnCommunityShares=reassignBasedOnCommunityShares


    def share(self,profiles:List[ProfileEnergyDataAux],sharePersonalPvs:bool,communityPv:float)->List[ProfileSharingsDataAux]: #this method can't share personal pvs, because there is not microtrading
        profilesSharingsList=Quota().share(profiles=profiles,sharePersonalPvs=sharePersonalPvs,communityPv=communityPv) #first step is to do quota sharing
        #now reassign the excedents to cover deficits
        #the paper is not clear about how to redistribute the excedents. if there's more demand than excedents, then how does this method decide which HH gets more or less energy? Same case if there's more excedents than demand, how does the method decide who which HH trades sells more or less energy.
        #There is 2 ways to do it. Based on the communityShares or based on the HHs proportion of HHnresidual/totalResidual. I implemented both, use the attribute reassignBasedOnCommunityShares in the init method to choose which way to do it
        if self.reassignBasedOnCommunityShares:
            return self._reassign_based_on_shares(profilesSharingsList=profilesSharingsList)            
        else:
            return self._reassign_based_on_proportion(profilesSharingsList=profilesSharingsList)


    def _reassign_based_on_shares(self,profilesSharingsList:List[ProfileSharingsDataAux])->List[ProfileSharingsDataAux]:
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


                

