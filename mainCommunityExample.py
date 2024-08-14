from Community.communityConfiguration import CommunityConfig
from utils.enums import Granularity, FactorType, MarketCountry
from utils.geolocation import Geolocation
from Community.community import Community
from datetime import datetime, date
from models import MODELS
import pandas as pd
import numpy as np

from Profiles.examples import small_apartment_1, small_apartment_2, small_apartment_3, small_apartment_4, small_apartment_5, small_apartment_6
from Community.Sharing.virtualNetBilling import VirtualNetBilling
from Community.Sharing.sequentialSharing import SequentialSharing

from Community.EnergyPrice.wholesaleMarket import WholesaleMarket



market=WholesaleMarket(country=MarketCountry.Spain,start=date(2023,1,1),end=date(2023,1,1))
prices=market.prices_at_date(date(2023,4,1))
print(prices)

madrid=Geolocation("Madrid, Spain")

start_date=date(2024, 1, 1)



communityConfig=CommunityConfig(
    granularity=Granularity.FifteenMinutes,
    currentDate=start_date,
    geolocation=madrid,
    sharePersonalPvs=True,
    showPersonalPvEarnings=True

)

community=Community(
    profiles=[
        (small_apartment_1,0.25),
        (small_apartment_2,0.5),
        (small_apartment_3,0.25)
    ],
    communityAssets=[],
    sharingMethod=SequentialSharing()
)

community.simulate(communityConfig=communityConfig)
community.export_sharings_to_excel()
communityConfig.step_one_day()
community.simulate(communityConfig=communityConfig)
community.export_sharings_to_excel()
communityConfig.step_one_day()
community.simulate(communityConfig=communityConfig)
community.export_sharings_to_excel()
communityConfig.step_one_day()
community.simulate(communityConfig=communityConfig)
community.export_sharings_to_excel()
communityConfig.step_one_day()
community.simulate(communityConfig=communityConfig)
community.export_sharings_to_excel()
communityConfig.step_one_day()
community.simulate(communityConfig=communityConfig)
community.export_sharings_to_excel()
communityConfig.step_one_day()
community.simulate(communityConfig=communityConfig)
community.export_sharings_to_excel()
communityConfig.step_one_day()
community.simulate(communityConfig=communityConfig)
community.export_sharings_to_excel()
communityConfig.step_one_day()
community.simulate(communityConfig=communityConfig)
community.export_sharings_to_excel()
communityConfig.step_one_day()
community.simulate(communityConfig=communityConfig)
community.export_sharings_to_excel()
communityConfig.step_one_day()
community.simulate(communityConfig=communityConfig)
community.export_sharings_to_excel()
communityConfig.step_one_day()
community.simulate(communityConfig=communityConfig)
community.export_sharings_to_excel()
communityConfig.step_one_day()


