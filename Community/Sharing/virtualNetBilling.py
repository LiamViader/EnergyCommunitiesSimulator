from Profiles.profile import Profile
from Community.communityConfiguration import CommunityConfig
from Profiles.profileConfiguration import ProfileConfig
from Community.Sharing.sharingMethod import SharingMethod
from typing import List, Dict, Tuple
import numpy as np

class VirtualNetBilling(SharingMethod):
    def __init__(self) -> None:
        pass

    def share(self,profiles:List[Tuple[Profile,float]],communityConfig:CommunityConfig,communityPv:np.ndarray)->Dict[Profile,Dict[str,np.ndarray]]:
        totalPvExcedent=np.zeros(communityConfig.num_indices())
        totalLoadExcedent=np.zeros(communityConfig.num_indices())
        communityExcedents={}
        communitySharings={}
        for profile in profiles:
            load, pv=profile.get_load_pv()
            communitySharings[profile]={
                'load':load,
                'pv':pv,
            }
            excedents=load-pv
            for index, value in enumerate(excedents):
                if value>0:
                    totalLoadExcedent[index]+=value
                else:
                    totalPvExcedent[index]+=abs(value)
            communityExcedents[profile]=excedents
        for profile in profiles:
            gridExports=np.zeros(communityConfig.num_indices())
            gridImports=np.zeros(communityConfig.num_indices())
            microgridExports=np.zeros(communityConfig.num_indices())
            microgridImports=np.zeros(communityConfig.num_indices())
            for i in range(communityConfig.num_indices()):
                if communityExcedents[profile][i]>0:
                    if totalLoadExcedent[i]!=0:
                        microImportProportion=communityExcedents[profile][i]/totalLoadExcedent[i]
                    else:
                        microImportProportion=0
                    microgridImports[i]=min(microImportProportion*totalPvExcedent[i],communityExcedents[profile][i])
                    gridImports[i]=communityExcedents[profile][i]-microgridImports[i]
                else:
                    if totalPvExcedent[i]!=0:
                        microExportProportion=abs(communityExcedents[profile][i])/totalPvExcedent[i]
                    else:
                        microExportProportion=0
                    microgridExports[i]=min(microExportProportion*totalLoadExcedent[i],abs(communityExcedents[profile][i]))
                    gridExports[i]=abs(communityExcedents[profile][i])-microgridExports[i]
            communitySharings[profile].update({
                'grid-Export':gridExports,
                'grid-Import':gridImports,
                'microgrid-Export':microgridExports,
                'microgrid-Import':microgridImports
            })
        return communitySharings

