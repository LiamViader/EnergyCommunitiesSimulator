from Profiles.profile import Profile
from Community.communityConfiguration import CommunityConfig
from Profiles.profileConfiguration import ProfileConfig
from Community.Sharing.sharingMethod import SharingMethod
from typing import List, Dict, Tuple, Optional
import numpy as np
import math

class SequentialSharing(SharingMethod):
    def __init__(self) -> None:
        pass

    def share(self,profiles:List[Tuple[Profile,float]],communityConfig:CommunityConfig,communityPv:np.ndarray)->Dict[Profile,Dict[str,np.ndarray]]:
        minWeight=1e-40
        totalPv=np.zeros(communityConfig.num_indices())
        totalLoad=np.zeros(communityConfig.num_indices())
        communitySharings={}
        if communityConfig.share_personal_pvs():
            for profile, ownership in profiles:
                load, pv=profile.get_load_pv()
                communityPvOwned=communityPv*ownership
                communitySharings[profile]={
                    'load':load,
                    'pv':pv+communityPvOwned,
                    'grid-Export':np.zeros(communityConfig.num_indices()),
                    'grid-Import':np.zeros(communityConfig.num_indices()),
                    'microgrid-Export':np.zeros(communityConfig.num_indices()),
                    'microgrid-Import':np.zeros(communityConfig.num_indices()),
                    'weight':np.full(communityConfig.num_indices(), pv+communityPvOwned)
                }
                totalLoad+=load
                totalPv+=pv
        else:
            for profile, ownership in profiles:
                load,pv=profile.get_combined_load_pv()
                communityPvOwned=communityPv*ownership
                communitySharings[profile]={
                    'load':load,
                    'pv':communityPvOwned,
                    'grid-Export':np.zeros(communityConfig.num_indices()),
                    'grid-Import':np.zeros(communityConfig.num_indices()),
                    'microgrid-Export':np.zeros(communityConfig.num_indices()),
                    'microgrid-Import':np.zeros(communityConfig.num_indices()),
                    'weight':np.full(communityConfig.num_indices(), ownership)
                }
                if communityConfig.show_personal_pv_earnings():
                    communitySharings[profile]['personalPvExcedent-grid-Export']=pv

                totalLoad+=load
                totalPv+=communityPvOwned

        for i in range(communityConfig.num_indices()):
            if totalLoad[i]>=totalPv[i]:
                pieceWiseFunc={}
                pvToExport=0
                for profile, profile_data in communitySharings.items():
                    if profile_data['pv'][i]>=profile_data['load'][i]:
                        pvToExport+=(profile_data['pv'][i]-profile_data['load'][i])
                        weight=max(profile_data['weight'][i],minWeight)
                        pieceWiseFunc[profile]=(0,weight)
                    else:
                        residualLoad=profile_data['load'][i]-profile_data['pv'][i]
                        weight=max(profile_data['weight'][i],minWeight)
                        pieceWiseFunc[profile]=(residualLoad,weight)
                x=self.solve_piecewise(pieceWiseFunc,pvToExport)
                for profile, profile_data in communitySharings.items():
                    if profile_data['pv'][i]>=profile_data['load'][i]:
                        communitySharings[profile]['microgrid-Export'][i]=profile_data['pv'][i]-profile_data['load'][i]
                    else:
                        communitySharings[profile]['microgrid-Import'][i]=min(pieceWiseFunc[profile][0],pieceWiseFunc[profile][1]*x)
                        communitySharings[profile]['grid-Import'][i]=(profile_data['load'][i]-profile_data['pv'][i])-communitySharings[profile]['microgrid-Import'][i]
            else:
                pieceWiseFunc={}
                loadToImport=0
                for profile, profile_data in communitySharings.items():
                    if profile_data['load'][i]>=profile_data['pv'][i]:
                        weight=max(profile_data['weight'][i],minWeight) #perque no sigui 0
                        loadToImport+=profile_data['load'][i]-profile_data['pv'][i]
                        pieceWiseFunc[profile]=(0,weight)
                    else:
                        residualPv=profile_data['pv'][i]-profile_data['load'][i]
                        weight=max(profile_data['weight'][i],minWeight)
                        pieceWiseFunc[profile]=(residualPv,weight)
                x=self.solve_piecewise(pieceWiseFunc,loadToImport)
                for profile, profile_data in communitySharings.items():
                    if profile_data['load'][i]>=profile_data['pv'][i]:
                        communitySharings[profile]['microgrid-Import'][i]=profile_data['load'][i]-profile_data['pv'][i]
                    else:
                        communitySharings[profile]['microgrid-Export'][i]=min(pieceWiseFunc[profile][0],pieceWiseFunc[profile][1]*x)
                        communitySharings[profile]['grid-Export'][i]=(profile_data['pv'][i]-profile_data['load'][i])-communitySharings[profile]['microgrid-Export'][i]
        return communitySharings

    def solve_piecewise(self,piecewiseFunc:Dict[Profile,Tuple[float,float]],y:float)->float:
        func=list(piecewiseFunc.values())
        # Step 1: Determine the critical points
        critical_points = set()
        func2=[]
        for a, b in func:
            if b != 0:
                critical_points.add(a / b)
                func2.append((a,b))
        func=func2
                
        if len(critical_points)==0:
            return 0
        
        critical_points.add(np.inf)
        critical_points.add(-np.inf)
        critical_points.add(0)

        # Convert the set to a sorted list
        critical_points = sorted(critical_points)

        # Step 2: Evaluate each interval

        def evaluate(x):
            return sum(min(a, b * x) for a, b in func)
        
        def isEqual(a,b):
            return math.isclose(a, b, rel_tol=1e-9, abs_tol=0.0)

        for i in range(len(critical_points) - 1):
            x1 = critical_points[i]
            x2 = critical_points[i + 1]


            # Determine the coefficients for each term in this interval
            total_constant = 0
            total_coefficient = 0
            for a, b in func:
                if np.isinf(x2) and b==0:
                    bx2=0
                else:
                    bx2=b*x2
                if bx2 <= a or isEqual(a,bx2):
                    total_coefficient += b
                else:
                    total_constant += a

            if total_coefficient != 0:
                x_sol = (y - total_constant) / total_coefficient
                if x1 < x_sol <= x2 or isEqual(x_sol,x2):
                    return x_sol
        
        print("something went bad on computing x in pieceWise func")
        print(func)
        for i in range(len(critical_points) - 1):
            x1 = critical_points[i]
            x2 = critical_points[i + 1]


            # Determine the coefficients for each term in this interval
            total_constant = 0
            total_coefficient = 0
            for a, b in func:
                if np.isinf(x2) and b==0:
                    bx2=0
                else:
                    bx2=b*x2
                if bx2 < a or isEqual(a,bx2):
                    total_coefficient += b
                else:
                    total_constant += a

            if total_coefficient != 0:
                x_sol = (y - total_constant) / total_coefficient
                print(evaluate(x_sol),y,x1, x_sol,x2)
                if x1 < x_sol <= x2 or isEqual(x_sol,x2):
                    return x_sol
            else:
                suma=0
                for a, b in func:
                    suma+=a
                print("noo",y,suma,x1,x2,bx2)
                print(critical_points)
            
        return 0
