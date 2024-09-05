from Profiles.utils.profileCostDataAux import ProfileCostDataAux
from Profiles.utils.profileSharingsDataAux import ProfileSharingsDataAux
from EnergyPrice.EnergyPlans.baseEnergyPlan import BaseEnergyPlan
from Simulation.simulationConfiguration import SimulationConfig
from Community.Costs.costCalculationBaseMethod import CostCalculationBaseMethod
from typing import List, Dict, Tuple
from abc import ABC, abstractmethod
import numpy as np
from datetime import datetime
import math

class AlwaysUseBestPlan(CostCalculationBaseMethod):
    def __init__(self) -> None:
        super().__init__("Always using the best plan")

    def calculate(self,sharingsAndPlan:List[Tuple[ProfileSharingsDataAux,BaseEnergyPlan]],communityPlan:BaseEnergyPlan,datetimeValue:datetime)->List[ProfileCostDataAux]:
        costsList:List[ProfileCostDataAux]=[]
        minImportPrice=math.inf
        maxExportPrice=0
        for profileSharings,profilePlan in sharingsAndPlan:
            profileCosts=ProfileCostDataAux(id=profileSharings.id)

            profileImportPrice=profilePlan.buying_price(instant=datetimeValue)
            communityImportPrice=communityPlan.buying_price(instant=datetimeValue)
            if communityImportPrice>profileImportPrice:
                profileCosts.gridImportPrice=profileImportPrice
                profileCosts.gridImportPlan=profilePlan.get_name()
            else:
                profileCosts.gridImportPrice=communityImportPrice
                profileCosts.gridImportPlan=communityPlan.get_name()
            profileCosts.gridImportCost=profileSharings.gridImport*profileCosts.gridImportPrice

            profileExportPrice=profilePlan.selling_price(instant=datetimeValue)
            communityExportPrice=communityPlan.selling_price(instant=datetimeValue)
            if communityExportPrice<profileExportPrice:
                profileCosts.gridExportPrice=profileExportPrice
                profileCosts.gridExportPlan=profilePlan.get_name()
            else:
                profileCosts.gridExportPrice=communityExportPrice
                profileCosts.gridExportPlan=communityPlan.get_name()

            profileCosts.gridExportRevenue=profileSharings.gridExport*profileCosts.gridExportPrice
            profileCosts.personalExcedentsPrice=profilePlan.selling_price(instant=datetimeValue)
            profileCosts.personalExcedentsRevenue=profileSharings.personalPvExcedent *profileCosts.personalExcedentsPrice

            profileCosts.personalExcedentsPlan=profilePlan.get_name()
            minImportPrice=min(profileCosts.gridImportPrice,minImportPrice)
            maxExportPrice=max(profileCosts.gridExportPrice,maxExportPrice)
            costsList.append(profileCosts)
        
        microgridPrice=(minImportPrice+maxExportPrice)/2
        for profileCostAux, (profileSharings, profilePlan) in zip(costsList,sharingsAndPlan):
            profileCostAux.microgridPrice=microgridPrice
            profileCostAux.microgridCost=profileSharings.microgridImport*microgridPrice
            profileCostAux.microgridRevenue=profileSharings.microgridExport*microgridPrice

        return costsList
            

