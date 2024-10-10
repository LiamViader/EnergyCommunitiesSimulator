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

class AlwaysUsePersonalPlan(CostCalculationBaseMethod):
    """
    Cost calculation method where each profile always uses its own personal energy plan for grid import/export 
    and personal excedents. The microgrid prices are computed based on a mix of the minimum import price 
    and maximum export price across all profiles.

    Methods:
        __init__():
            Initializes the cost calculation method with a predefined name.

        calculate(sharingsAndPlan: List[Tuple[ProfileSharingsDataAux, BaseEnergyPlan]], 
                  communityPlan: BaseEnergyPlan, datetimeValue: datetime) -> List[ProfileCostDataAux]:
            Calculates the energy costs and revenues for each profile based on their individual energy plan.
    """
    def __init__(self) -> None:
        """
        Initializes the AlwaysUsePersonalPlan cost calculation method with a predefined name.
        """
        super().__init__("Always using the personal plan")

    def calculate(self,sharingsAndPlan:List[Tuple[ProfileSharingsDataAux,BaseEnergyPlan]],communityPlan:BaseEnergyPlan,datetimeValue:datetime)->List[ProfileCostDataAux]:
        """
        Calculates the energy costs and revenues for each profile, assuming they always use their personal energy plan 
        for grid import/export and personal excedents. Also calculates the cost/revenue associated with microgrid usage based on a mix of the minimum import price 
        and maximum export price across all profiles.

        Args:
            sharingsAndPlan (List[Tuple[ProfileSharingsDataAux, BaseEnergyPlan]]): A list of tuples where each tuple 
                contains profile sharing data and the associated energy plan for that profile.
            communityPlan (BaseEnergyPlan): The community energy plan (not used in this method).
            datetimeValue (datetime): The specific datetime for which the prices should be retrieved.

        Returns:
            List[ProfileCostDataAux]: A list of ProfileCostDataAux objects, each representing the costs and revenues 
                for a particular profile.
        """

        costsList:List[ProfileCostDataAux]=[]
        minImportPrice=math.inf
        maxExportPrice=0
        for profileSharings,profilePlan in sharingsAndPlan:
            profileCosts=ProfileCostDataAux(id=profileSharings.id)
            profileCosts.gridImportPrice=profilePlan.buying_price(instant=datetimeValue)
            profileCosts.gridImportCost=profileSharings.gridImport*profileCosts.gridImportPrice
            profileCosts.gridExportPrice=profilePlan.selling_price(instant=datetimeValue)
            profileCosts.gridExportRevenue=profileSharings.gridExport*profileCosts.gridExportPrice
            profileCosts.personalExcedentsPrice=profilePlan.selling_price(instant=datetimeValue)
            profileCosts.personalExcedentsRevenue=profileSharings.personalPvExcedent*profileCosts.personalExcedentsPrice
            profileCosts.gridImportPlan=profilePlan.get_name()
            profileCosts.gridExportPlan=profilePlan.get_name()
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
            

