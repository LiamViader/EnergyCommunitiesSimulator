from Profiles.profile import Profile
from Profiles.profileConfiguration import ProfileConfig
from utils.enums import Granularity
from Profiles.LoadFactors.Dishwasher.dishwasher import Dishwasher
from Profiles.LoadFactors.useConfig import UseConfig
from utils.minuteInterval import MinuteInterval
from Profiles.LoadFactors.SolarPanel.solarPanel import SolarPanel
from Profiles.LoadFactors.SolarPanel.solarIrradiation import SolarIrradiation
from Profiles.LoadFactors.SolarPanel.solarPV import SolarPV
from utils.geolocation import Geolocation
from datetime import datetime, date

madrid=Geolocation("Madrid, Spain")

profilesConfig=ProfileConfig(granularity=Granularity.Hour)

current_date=date(2024, 6, 25)

madridIrradiation=SolarIrradiation(madrid,current_date,profileConfig=profilesConfig)


washDishesConf=UseConfig(timesWeekly=7,
                        intervals=[MinuteInterval(14,15,True),
                                    MinuteInterval(9,11,True)])

dishwasherEco=Dishwasher(name="rentaplats Cicle Eco",
                      cycleLoad=0.9,
                      cycleTime=3.5*60,
                      washingConfig=washDishesConf)

dishwasherStd=Dishwasher(name="rentaplats Cicle Standard",
                      cycleLoad=1.655,
                      cycleTime=2*60,
                      washingConfig=washDishesConf)

standardSolarPanel=SolarPanel(name="solarPanel",
                              productionCapacity=0.3,
                              efficiency=0.18)

pv=SolarPV("pv",[standardSolarPanel for i in range(7)])

perfil=Profile(solarIrradiation=madridIrradiation,
               loadFactors=[dishwasherEco,dishwasherStd,pv])

perfil.generate_loads(profileConfig=profilesConfig)