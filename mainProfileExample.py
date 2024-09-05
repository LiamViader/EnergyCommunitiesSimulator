from Profiles.profile import Profile
from Simulation.simulationConfiguration import SimulationConfig
from utils.enums import Granularity, FactorType, LightType
from Profiles.Factors.Cyclic.cyclicFactor import CyclicFactor
from Profiles.Factors.Cyclic.UseConfig.cyclicWeeklyUseConfig import CyclicWeeklyUseConfig
from utils.minuteInterval import MinuteInterval
from Profiles.Factors.SolarPanel.solarPanel import SolarPanel
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.Factors.SolarPanel.solarPV import SolarPV
from Profiles.Battery.batteriesManager import BatteriesManager
from Profiles.Factors.Continuos.continuosCyclicFactor import ContinuosCyclicFactor
from Profiles.Factors.ElectricCar.UseConfig.carOnNeedUseConfig import CarOnNeedUseConfig
from Profiles.Factors.ElectricCar.electricCarFactor import ElectricCarFactor
from Profiles.Factors.Continuos.continuosFactor import ContinuosFactor
from utils.geolocation import Geolocation
from utils.RandomNumbers.truncatedNormalDistribution import TruncatedNormalDistribution
from utils.RandomNumbers.normalDistribution import NormalDistribution
from Profiles.Factors.Climatitzation.climatitzationFactor import ClimatitzationFactor
from Profiles.Factors.Climatitzation.Components.heating import Heating
from Profiles.Factors.Climatitzation.thermostat import Thermostat
from Profiles.Factors.WindTurbine.windTurbineFactor import WindTurbineFactor
from Profiles.Factors.Lightning.lightningFactor import LightningFactor
from Profiles.Factors.Lightning.lightningModel import LightningModel
from datetime import datetime, date
from models import MODELS
import pandas as pd
import numpy as np
from Profiles.examples import small_apartment_5



madrid=Geolocation("Madrid, Spain")

current_date=date(2024, 7, 25)

simulationConfig=SimulationConfig(granularity=Granularity.FifteenMinutes,currentDate=current_date,geolocation=madrid)



washDishesConf=CyclicWeeklyUseConfig(
    timesWeekly=6,
    intervals=[
        MinuteInterval(14,15,True),
        MinuteInterval(9,11,True)
    ]
)

washDishesConf2=CyclicWeeklyUseConfig(
    timesWeekly=12,
    intervals=[
        MinuteInterval(10,11.5,True),
        MinuteInterval(23,24,True)
    ]
)

dishwasherEco=CyclicFactor(
    cyclicModel=MODELS['DISHWASHERS']['ECO'],
    useConfig=washDishesConf
)

dishwasherStd=CyclicFactor(
    MODELS['DISHWASHERS']['STANDARD'],
    useConfig=washDishesConf2
)

refrigeratorFixed=ContinuosCyclicFactor(MODELS['REFRIGERATORS']['FIXED_COMPRESSOR_EXAMPLE'])

refrigeratorVariable=ContinuosCyclicFactor(MODELS['REFRIGERATORS']['VARIABLE_COMPRESSOR_EXAMPLE'])


standardSolarPanel=SolarPanel(
    name="solarPanel",
    productionCapacity=0.3,
    efficiency=0.18
)

pv=SolarPV(name="SolarPanels",solarPanels=[standardSolarPanel for i in range(15)])

batteriesExample=BatteriesManager([MODELS['BATTERIES']['STANDARD']])

carConfig=CarOnNeedUseConfig(
    dailyUsage=(
        TruncatedNormalDistribution(15,60,100,70),
        TruncatedNormalDistribution(15,60,100,70),
        TruncatedNormalDistribution(15,60,100,70),
        TruncatedNormalDistribution(15,60,100,70),
        TruncatedNormalDistribution(20,60,120,77),
        TruncatedNormalDistribution(40,0,200,20),
        TruncatedNormalDistribution(20,0,200,30)
    ),
    chargeIntervals=(
        MinuteInterval(23,1,True),
        MinuteInterval(23,1,True),
        MinuteInterval(23,1,True),
        MinuteInterval(23,1,True),
        MinuteInterval(23,1,True),
        MinuteInterval(23,1,True),
        MinuteInterval(23,1,True)
    ),
    batteryThreshold=0.99
)

tesla=ElectricCarFactor(
    model=MODELS['ELECTRIC_CARS']['TESLA'],
    useConfig=carConfig,
)

washMachineConf=CyclicWeeklyUseConfig(
    timesWeekly=3,
    intervals=[
        MinuteInterval(9,11,True)
    ]
)

washingMachineStandard=CyclicFactor(
    cyclicModel=MODELS['WASHING_MACHINES']['STANDARD'],
    useConfig=washMachineConf
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

windTurbine=WindTurbineFactor(MODELS['WIND_TURBINES']['TUGE10KW'])


perfil=small_apartment_5

perfil.simulate(simulationConfig=simulationConfig)
df=perfil.get_detailed_load_df()
df.to_excel("DataOutputs/day1_detailed.xlsx")

combined=perfil.get_combined_load()
series=pd.Series(combined)
df_combined=pd.DataFrame()
timeSeries=simulationConfig.get_time_series()
df_combined["TimeStamp"] = timeSeries.index
df_combined['Load']=series
df_combined.to_excel("DataOutputs/day1_combined.xlsx")


simulationConfig.step_one_day()

perfil.simulate(simulationConfig=simulationConfig)
df=perfil.get_detailed_load_df()
df.to_excel("DataOutputs/day2_detailed.xlsx")

simulationConfig.step_one_day()

perfil.simulate(simulationConfig=simulationConfig)
df=perfil.get_detailed_load_df()
df.to_excel("DataOutputs/day3_detailed.xlsx")
