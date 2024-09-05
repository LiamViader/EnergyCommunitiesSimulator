from Profiles.profile import Profile
from Profiles.utils.profileEnergyDataAux import ProfileEnergyDataAux
from Profiles.utils.profileSharingsDataAux import ProfileSharingsDataAux
from Simulation.simulationConfiguration import SimulationConfig
from Community.Sharing.sharingMethod import SharingMethod
from typing import List, Dict, Tuple, Optional
import numpy as np
import math

class SequentialSharing(SharingMethod):
    def __init__(self) -> None:
        super().__init__("Sequential Sharing")

    def share(self,profiles:List[ProfileEnergyDataAux],sharePersonalPvs:bool,communityPv:float)->List[ProfileSharingsDataAux]: #profiles quedarà modificat al sortir de la funcio aixi q no usarlos. Sino cambiar una mica l'implementació i ja, pero ho fare més endavant.
        sharings:List[ProfileSharingsDataAux]=[]
        minWeight=1e-10 # perque ningu tingui un pes de 0, ja que sino no se li comparteix res encara que sobri. És a dir si un individu A té weight de 0 i una demanda de 1kwh, llavors encara que un individu B tingui excedent de 1kwh, aquest s'exportarà al grid en comptes de vendreho a A, el qual seria més logic ja que els dos guanyarien mes
        #a més a més, un pes de 0 dóna problemes amb els calculs, si es necessita, s'ha de tractar aquest cas, directament no tinguent en compte als individus amb weight 0, no posantlos a la funcio, i obviament no afegint el seu load al calcul tampoc. És a dir exclourels totalment de la repartició
        #tal i com he comentat, ara no està implementat perque funcioni amb 0 i assignant un weight molt infim als que tindrien 0, fa que sigui més rentable per la comunitat
        totalPv=0
        totalLoad=0
        weights:Dict[ProfileEnergyDataAux,float]={}
        if sharePersonalPvs:
            for profile in profiles:
                load=profile.load
                communityPvOwned=communityPv*profile.share
                pv=profile.production+communityPvOwned

                profile.production=pv
                profile.personalPvExcedent=0
                profile.load=load

                weights[profile]=pv+communityPvOwned
                totalLoad+=load
                totalPv+=pv
        else:
            for profile in profiles:
                energy=profile.load-profile.production
                if energy>=0:
                    load=energy
                    pv=0
                else:
                    pv=abs(energy)
                    load=0
                communityPvOwned=communityPv*profile.share

                profile.load=load
                profile.production=communityPvOwned
                profile.personalPvExcedent=pv

                weights[profile]=profile.share
                totalLoad+=load
                totalPv+=communityPvOwned

        if totalLoad>=totalPv:
            pieceWiseFunc:Dict[ProfileEnergyDataAux,Tuple[float,float]]={}
            pvToExport=0
            for profile, weight in weights.items():
                weight=max(weight,minWeight) #perque no sigui 0
                if profile.production>=profile.load:
                    pvToExport+=(profile.production-profile.load)
                    pieceWiseFunc[profile]=(0,weight)
                else:
                    residualLoad=profile.load-profile.production
                    pieceWiseFunc[profile]=(residualLoad,weight)
            x=self.solve_piecewise(pieceWiseFunc,pvToExport)
            for profile, weight in weights.items():
                profileSharings=ProfileSharingsDataAux(profile_id=profile.id)
                profileSharings.communityShares=profile.share
                profileSharings.personalPvExcedent=profile.personalPvExcedent
                profileSharings.totalPvAbleToShare=profile.production
                if profile.production>=profile.load:
                    profileSharings.microgridExport=profile.production-profile.load
                else:
                    profileSharings.microgridImport=min(pieceWiseFunc[profile][0],pieceWiseFunc[profile][1]*x)
                    profileSharings.gridImport=(profile.load-profile.production)-profileSharings.microgridImport
                sharings.append(profileSharings)
        else:
            pieceWiseFunc={}
            loadToImport=0
            for profile, weight in weights.items():
                weight=max(weight,minWeight) #perque no sigui 0
                if profile.load>=profile.production:
                    loadToImport+=profile.load-profile.production
                    pieceWiseFunc[profile]=(0,weight)
                else:
                    residualPv=profile.production-profile.load
                    pieceWiseFunc[profile]=(residualPv,weight)
            x=self.solve_piecewise(pieceWiseFunc,loadToImport)
            for profile, weight in weights.items():
                profileSharings=ProfileSharingsDataAux(profile_id=profile.id)
                profileSharings.communityShares=profile.share
                profileSharings.personalPvExcedent=profile.personalPvExcedent
                profileSharings.totalPvAbleToShare=profile.production
                if profile.load>=profile.production:
                    profileSharings.microgridImport=profile.load-profile.production
                else:
                    profileSharings.microgridExport=min(pieceWiseFunc[profile][0],pieceWiseFunc[profile][1]*x)
                    profileSharings.gridExport=(profile.production-profile.load)-profileSharings.microgridExport
                sharings.append(profileSharings)
        return sharings

    def solve_piecewise(self,piecewiseFunc:Dict[ProfileEnergyDataAux,Tuple[float,float]],y:float)->float:
        func=list(piecewiseFunc.values())
        #determinar punts critics
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

        #llista ordenada
        critical_points = sorted(critical_points)

        #evaluar cada interval

        def evaluate(x):
            return sum(min(a, b * x) for a, b in func)
        
        def isEqual(a,b):
            return math.isclose(a, b, rel_tol=1e-9, abs_tol=0.0)

        for i in range(len(critical_points) - 1):
            x1 = critical_points[i]
            x2 = critical_points[i + 1]


            # Determinar coeficients per cada terme en aquest interval
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


            # Determinar coeficients per cada terme en aquest interval
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
