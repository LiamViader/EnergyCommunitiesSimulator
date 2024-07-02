from Profiles.profile import Profile
from Profiles.profileConfiguration import ProfileConfig
from utils.enums import Granularity
from Profiles.Factors.Cyclic.cyclicFactor import CyclicFactor
from Profiles.Factors.useConfig import UseConfig
from utils.minuteInterval import MinuteInterval
from Profiles.Factors.SolarPanel.solarPanel import SolarPanel
from Profiles.Factors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.Factors.SolarPanel.solarPV import SolarPV
from utils.geolocation import Geolocation
from datetime import datetime, date
from models import MODELS

madrid=Geolocation("Madrid, Spain")

current_date=date(2024, 6, 25)

profilesConfig=ProfileConfig(granularity=Granularity.Hour,currentDate=current_date)


madridIrradiation=SolarIrradiation(madrid,profileConfig=profilesConfig)


washDishesConf=UseConfig(timesWeekly=7,
                        intervals=[MinuteInterval(14,15,True),
                                    MinuteInterval(9,11,True)])

washDishesConf2=UseConfig(timesWeekly=9,
                        intervals=[MinuteInterval(0,3,True),
                                    MinuteInterval(17,19,True)])

dishwasherEco=CyclicFactor(cyclicModel=MODELS['DISHWASHERS']['ECO'],
                      washingConfig=washDishesConf)

dishwasherStd=CyclicFactor(MODELS['DISHWASHERS']['STANDARD'],
                      washingConfig=washDishesConf2)

standardSolarPanel=SolarPanel(name="solarPanel",
                              productionCapacity=0.3,
                              efficiency=0.18)

pv=SolarPV(name="pv",solarPanels=[standardSolarPanel for i in range(7)])

perfil=Profile(solarIrradiation=madridIrradiation,
               loadFactors=[dishwasherEco,dishwasherStd,pv])

perfil.simulate(profileConfig=profilesConfig)