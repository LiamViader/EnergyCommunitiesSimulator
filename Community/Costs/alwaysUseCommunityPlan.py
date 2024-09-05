from Profiles.utils.profileCostDataAux import ProfileCostDataAux
from Profiles.utils.profileSharingsDataAux import ProfileSharingsDataAux
from EnergyPrice.EnergyPlans.baseEnergyPlan import BaseEnergyPlan
from Simulation.simulationConfiguration import SimulationConfig
from Community.Costs.costCalculationBaseMethod import CostCalculationBaseMethod
from typing import List, Dict, Tuple
from abc import ABC, abstractmethod
import numpy as np
from datetime import datetime

class AlwaysUseCommunityPlan(CostCalculationBaseMethod):
    def __init__(self) -> None:
        super().__init__("Always using the community plan")

    def calculate(self,sharingsAndPlan:List[Tuple[ProfileSharingsDataAux,BaseEnergyPlan]],communityPlan:BaseEnergyPlan,datetimeValue:datetime)->List[ProfileCostDataAux]:
        costsList:List[ProfileCostDataAux]=[]
        gridImportPrice=profileCosts.gridImportPrice=communityPlan.buying_price(instant=datetimeValue)
        gridExportPrice=profileCosts.gridExportPrice=communityPlan.selling_price(instant=datetimeValue)
        microgridPrice=(gridImportPrice+gridExportPrice)/2
        for profileSharings,profilePlan in sharingsAndPlan:
            profileCosts=ProfileCostDataAux(id=profileSharings.id)
            profileCosts.gridImportPrice=gridImportPrice
            profileCosts.gridImportCost=profileSharings.gridImport*profileCosts.gridImportPrice
            profileCosts.gridExportPrice=gridExportPrice
            profileCosts.gridExportRevenue=profileSharings.gridExport*profileCosts.gridExportPrice
            profileCosts.personalExcedentsPrice=profilePlan.selling_price(instant=datetimeValue)
            profileCosts.personalExcedentsRevenue=profileSharings.personalPvExcedent*profileCosts.personalExcedentsPrice
            profileCosts.microgridPrice=microgridPrice
            profileCosts.microgridCost=profileSharings.microgridImport*microgridPrice
            profileCosts.microgridRevenue=profileSharings.microgridExport*microgridPrice
            profileCosts.gridImportPlan=communityPlan.get_name()
            profileCosts.gridExportPlan=communityPlan.get_name()
            profileCosts.personalExcedentsPlan=profilePlan.get_name()
            costsList.append(profileCosts)
        return costsList
            

