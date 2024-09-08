from Simulation.simulationConfiguration import SimulationConfig
from utils.enums import Granularity, FactorType, MarketCountry
from utils.geolocation import Geolocation
from Community.community import Community
from datetime import datetime, date
from models import MODELS
import pandas as pd
import numpy as np
from Profiles.Factors.SolarPanel.solarPanel import SolarPanel
from Profiles.Factors.SolarPanel.solarPV import SolarPV

from Profiles.examples import small_apartment_1, small_apartment_2, small_apartment_3, small_apartment_4, small_apartment_5, small_apartment_6
from Community.Sharing.virtualNetBilling import VirtualNetBilling
from Community.Sharing.sequentialSharing import SequentialSharing
from Community.Sharing.quotaConsumptionSharing import QuotaConsumptionSharing
from Community.Sharing.quota import Quota

from EnergyPrice.wholesaleMarket import WholesaleMarket
from EnergyPrice.EnergyPlans.SomEnergia.somEnergiaIndexadaIndustria import SomEnergiaIndexadaIndustria
from Community.Costs.alwaysUseBestPlan import AlwaysUseBestPlan


market=WholesaleMarket(country=MarketCountry.Spain)

madrid=Geolocation("Madrid, Spain")

start_date=date(2024, 1, 1)



simulationConfig=SimulationConfig(
    granularity=Granularity.Hour,
    currentDate=start_date,
    geolocation=madrid,

)

standardSolarPanel=SolarPanel(
    name="solarPanel",
    productionCapacity=0.3,
    efficiency=0.18
)

communityPanels=SolarPV(name="SolarPanels",solarPanels=[standardSolarPanel for i in range(30)])


community=Community(
    profiles=[
        (small_apartment_1,0.25),
        (small_apartment_2,0.5),
        (small_apartment_3,0.25)
    ],
    communityAssets=[communityPanels],
    sharingMethod=QuotaConsumptionSharing(),
    sharePersonalPvs=False,
    costCalculationMethod=AlwaysUseBestPlan(),
    energyPlan=SomEnergiaIndexadaIndustria()
)

for i in range(10):
    community.simulate(simulationConfig=simulationConfig)
    simulationConfig.step_one_day()

print("COST of QuotaConsumptionSharing With reassign based on shares:",community.simulatedCommunity.get_total_community_cost())
community.set_sharing_method(QuotaConsumptionSharing(reassignBasedOnCommunityShares=False))
community.shareSimulatedEnergies()
print("COST of QuotaConsumptionSharing With reassign based on proportion:",community.simulatedCommunity.get_total_community_cost())
community.set_sharing_method(SequentialSharing())
community.shareSimulatedEnergies()
print("COST of SequentialSharing:",community.simulatedCommunity.get_total_community_cost())
community.set_sharing_method(VirtualNetBilling())
community.shareSimulatedEnergies()
print("COST of VirtualNetBilling:",community.simulatedCommunity.get_total_community_cost())
community.set_sharing_method(Quota())
community.shareSimulatedEnergies()
print("COST of Quota:",community.simulatedCommunity.get_total_community_cost())


