from Profiles.profile import Profile
from Profiles.profileConfiguration import ProfileConfig
from Community.communityConfiguration import CommunityConfig
from utils.enums import Granularity, FactorType
from Profiles.Factors.Cyclic.cyclicFactor import CyclicFactor
from Profiles.Factors.Cyclic.cyclicUseConfig import CyclicUseConfig
from utils.minuteInterval import MinuteInterval
from Profiles.Factors.SolarPanel.solarPanel import SolarPanel
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.Factors.SolarPanel.solarPV import SolarPV
from Profiles.Battery.batteriesManager import BatteriesManager
from Profiles.Factors.Continuos.continuosCyclicFactor import ContinuosCyclicFactor
from Profiles.Factors.ElectricCar.carOnNeedUseConfig import CarOnNeedUseConfig
from Profiles.Factors.ElectricCar.electricCarFactor import ElectricCarFactor
from Profiles.Factors.Continuos.continuosFactor import ContinuosFactor
from utils.geolocation import Geolocation
from utils.RandomNumbers.truncatedNormalDistribution import TruncatedNormalDistribution
from utils.RandomNumbers.normalDistribution import NormalDistribution
from Profiles.Factors.Climatitzation.climatitzationFactor import ClimatitzationFactor
from Profiles.Factors.Climatitzation.heating import Heating
from Profiles.Factors.Climatitzation.thermostat import Thermostat
from datetime import datetime, date
from models import MODELS
import pandas as pd
import numpy as np


from Profiles.Factors.Climatitzation.temperature import Temperature


madrid=Geolocation("Madrid, Spain")

current_date=date(2024, 1, 25)

communityConfig=CommunityConfig(granularity=Granularity.FifteenMinutes,currentDate=current_date,geolocation=madrid)

profilesConfig=ProfileConfig(communityConfig=communityConfig)



washDishesConf=CyclicUseConfig(
    timesWeekly=6,
    intervals=[
        MinuteInterval(14,15,True),
        MinuteInterval(9,11,True)
    ]
)

washDishesConf2=CyclicUseConfig(
    timesWeekly=5,
    intervals=[
        MinuteInterval(10,11.5,True),
        MinuteInterval(14,16,True)
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

pv=SolarPV(name="pv",solarPanels=[standardSolarPanel for i in range(15)])

batteriesExample=BatteriesManager([MODELS['BATTERIES']['STANDARD']])

carConfig=CarOnNeedUseConfig(
    dailyUsage=[
        TruncatedNormalDistribution(15,60,100,70),
        TruncatedNormalDistribution(15,60,100,70),
        TruncatedNormalDistribution(15,60,100,70),
        TruncatedNormalDistribution(15,60,100,70),
        TruncatedNormalDistribution(20,60,120,77),
        TruncatedNormalDistribution(40,0,200,20),
        TruncatedNormalDistribution(20,0,200,30)
    ],
    chargeIntervals=[
        MinuteInterval(23,1,True),
        MinuteInterval(23,1,True),
        MinuteInterval(23,1,True),
        MinuteInterval(23,1,True),
        MinuteInterval(23,1,True),
        MinuteInterval(23,1,True),
        MinuteInterval(23,1,True)
    ],
    batteryThreshold=0.99
)

tesla=ElectricCarFactor(
    model=MODELS['ELECTRIC_CARS']['TESLA'],
    useConfig=carConfig,
)

washMachineConf=CyclicUseConfig(
    timesWeekly=3,
    intervals=[
        MinuteInterval(9,11,True)
    ]
)

washingMachineStandard=CyclicFactor(
    cyclicModel=MODELS['WASHING_MACHINES']['STANDARD'],
    washingConfig=washMachineConf
)

freezerVariable=ContinuosCyclicFactor(model=MODELS['FREEZERS']['VARIABLE_COMPRESSOR'])

onlyHeatingClimatitzation=ClimatitzationFactor(
    name="only heating climatitzation",
    climatitzationComponents=[
        Heating(
            maxPower=10.0, 
            minPower=2.0, 
            efficiency=0.85, 
            volume=200.0
        ),
    ],
    thermostat=Thermostat(
        idealTemperatures=[
            (MinuteInterval(6,10,True),21),
            (MinuteInterval(12,3,True),21)
        ],
        startingTemperature=21
    )
)


perfil=Profile(
    name="Manel",
    exteriorContactArea=50,
    insideVolume=150,
    loadFactors=[
        dishwasherStd,
        washingMachineStandard,
        refrigeratorVariable,
        freezerVariable,
        pv,
        tesla,
        onlyHeatingClimatitzation
    ],
    batteries=batteriesExample
)

perfil.simulate(profileConfig=profilesConfig)
df=perfil.get_detailed_load_df()
df.to_excel("DataOutputs/day1_detailed.xlsx")

combined=perfil.get_combined_load()
series=pd.Series(combined)
df_combined=pd.DataFrame()
timeSeries=profilesConfig.get_time_series()
df_combined["TimeStamp"] = timeSeries.index
df_combined['Load']=series
df_combined.to_excel("DataOutputs/day1_combined.xlsx")

detailed_acumulator=perfil.get_detailed_load()

for i in range(360):
    profilesConfig.step_one_day()
    perfil.simulate(profileConfig=profilesConfig)
    detailed=perfil.get_detailed_load()
    for name, loads in detailed.items():
        for index, (load, factor_type) in enumerate(loads):
            acumulated=detailed_acumulator[name][index][0]+load
            detailed_acumulator[name][index]=(acumulated,factor_type)

df_detailed=pd.DataFrame()
timeSeries=profilesConfig.get_time_series()
df_detailed["TimeStamp"] = timeSeries.index
for name, loads in detailed_acumulator.items():
    for index, (load, factor_type) in enumerate(loads):
        serie = pd.Series(load/361)
        df_detailed[f"{name}_{index}"] = serie

df_detailed.to_excel("DataOutputs/anual_detailed.xlsx")

df_combinedAnual=pd.DataFrame()
df_combinedAnual["TimeStamp"] = timeSeries.index
combinedLoad=np.zeros(profilesConfig.num_indices())
for name, loads in detailed_acumulator.items():
    for index, (load, factor_type) in enumerate(loads):
        if factor_type==FactorType.Consumer or factor_type==FactorType.Prosumer:
            combinedLoad+=load/361
        else:
            combinedLoad-=load/361
df_combinedAnual['Load']=combinedLoad
df_combinedAnual.to_excel("DataOutputs/anual_combined.xlsx")

profilesConfig.step_one_day()

perfil.simulate(profileConfig=profilesConfig)
df=perfil.get_detailed_load_df()
df.to_excel("DataOutputs/day2_detailed.xlsx")

profilesConfig.step_one_day()

perfil.simulate(profileConfig=profilesConfig)
df=perfil.get_detailed_load_df()
df.to_excel("DataOutputs/day3_detailed.xlsx")
