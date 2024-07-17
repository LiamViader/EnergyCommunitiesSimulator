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

start_date=date(2024, 1, 25)

communityConfig=CommunityConfig(granularity=Granularity.FifteenMinutes,currentDate=start_date,geolocation=madrid)

