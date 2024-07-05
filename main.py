from Profiles.profile import Profile
from Profiles.profileConfiguration import ProfileConfig
from utils.enums import Granularity
from Profiles.Factors.Cyclic.cyclicFactor import CyclicFactor
from Profiles.Factors.useConfig import UseConfig
from utils.minuteInterval import MinuteInterval
from Profiles.Factors.SolarPanel.solarPanel import SolarPanel
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.Factors.SolarPanel.solarPV import SolarPV
from Profiles.Battery.batteriesManager import BatteriesManager
from Profiles.Factors.Continuos.continuosCyclicFactor import ContinuosCyclicFactor
from utils.geolocation import Geolocation
from datetime import datetime, date
from models import MODELS
import pandas as pd

madrid=Geolocation("Madrid, Spain")

current_date=date(2024, 6, 25)

profilesConfig=ProfileConfig(granularity=Granularity.Minute,currentDate=current_date,geolocation=madrid)



washDishesConf=UseConfig(
    timesWeekly=7,
    intervals=[
        MinuteInterval(14,15,True),
        MinuteInterval(9,11,True)
    ]
)

washDishesConf2=UseConfig(
    timesWeekly=7,
    intervals=[
        MinuteInterval(23,23.5,True)
    ]
)

dishwasherEco=CyclicFactor(
    cyclicModel=MODELS['DISHWASHERS']['ECO'],
    washingConfig=washDishesConf
)

dishwasherStd=CyclicFactor(
    MODELS['DISHWASHERS']['STANDARD'],
    washingConfig=washDishesConf2
)

refrigeratorFixed=ContinuosCyclicFactor(MODELS['REFRIGERATORS']['FIXED_COMPRESSOR_EXAMPLE'])

refrigeratorVariable=ContinuosCyclicFactor(MODELS['REFRIGERATORS']['VARIABLE_COMPRESSOR_EXAMPLE'])


standardSolarPanel=SolarPanel(
    name="solarPanel",
    productionCapacity=0.3,
    efficiency=0.18
)

pv=SolarPV(name="pv",solarPanels=[standardSolarPanel for i in range(7)])

batteriesExample=BatteriesManager([MODELS['BATTERIES']['STANDARD']])

perfil=Profile(
    loadFactors=[
        dishwasherEco,
        dishwasherStd,
        refrigeratorFixed,
        refrigeratorVariable,
        pv
    ],
    batteries=batteriesExample
)

perfil.simulate(profileConfig=profilesConfig)
df=perfil.get_detailed_load_df()
df.to_excel("DataOutputs/day1_detailed.xlsx")

profilesConfig.step_one_day()

perfil.simulate(profileConfig=profilesConfig)
df=perfil.get_detailed_load_df()
df.to_excel("DataOutputs/day2_detailed.xlsx")

profilesConfig.step_one_day()

perfil.simulate(profileConfig=profilesConfig)
df=perfil.get_detailed_load_df()
df.to_excel("DataOutputs/day3_detailed.xlsx")
