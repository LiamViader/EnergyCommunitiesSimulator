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
    """
    Cost calculation method that assumes all profiles use the community energy plan for grid import/export.  It uses personal plan for personal excedents.
    The costs and revenues are calculated based on the community plan's buying and selling prices. The microgrid price is the mean of the community plan sell price and the community plan buying price

    Methods:
        __init__():
            Initializes the cost calculation method with a predefined name.

        calculate(sharingsAndPlan: List[Tuple[ProfileSharingsDataAux, BaseEnergyPlan]], 
                  communityPlan: BaseEnergyPlan, datetimeValue: datetime) -> List[ProfileCostDataAux]:
            Calculates the energy costs and revenues for each profile based on the community energy plan.
    """
    def __init__(self) -> None:
        """
        Initializes the AlwaysUseCommunityPlan cost calculation method with a predefined name.
        """
        super().__init__("Always using the community plan")

    def calculate(self,sharingsAndPlan:List[Tuple[ProfileSharingsDataAux,BaseEnergyPlan]],communityPlan:BaseEnergyPlan,datetimeValue:datetime)->List[ProfileCostDataAux]:
        """
        Calculates the energy costs and revenues for each profile, assuming they always use the community energy plan 
        for grid import/export. It uses personal plan for personal excedents. The microgrid price is the mean of the community plan sell price and the community plan buying price

        Args:
            sharingsAndPlan (List[Tuple[ProfileSharingsDataAux, BaseEnergyPlan]]): A list of tuples where each tuple 
                contains profile sharing data and the associated energy plan for that profile.
            communityPlan (BaseEnergyPlan): The community energy plan used for all profiles.
            datetimeValue (datetime): The specific datetime for which the prices should be retrieved.

        Returns:
            List[ProfileCostDataAux]: A list of ProfileCostDataAux objects, each representing the costs and revenues 
                for a particular profile.
        """
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
            

