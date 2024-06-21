from Profiles.profile import Profile
from Profiles.loadConfiguration import LoadConfig
from utils.enums import Granularity
from Profiles.LoadFactors.Dishwasher.dishwasher import Dishwasher
from Profiles.LoadFactors.useConfig import UseConfig
from utils.minuteInterval import MinuteInterval
from Profiles.LoadFactors.SolarPanel.solarPanel import SolarPanel
from Profiles.LoadFactors.SolarPanel.solarIrradiation import SolarIrradiation


solarIrradiation=SolarIrradiation(MinuteInterval(7,22,True),1)

washDishesConf=UseConfig(timesWeekly=7,
                                   intervals=[MinuteInterval(14,15,True),
                                              MinuteInterval(9,11,True)])

dishwasherEco=Dishwasher(name="rentaplats Cicle Eco",
                      cycleLoad=0.9,
                      cycleTime=3.5*60,
                      washingConfig=washDishesConf)

solarPanel=SolarPanel(name="pv",
                      productionCapacity=0.3,
                      efficiency=0.18)

dishwasherStd=Dishwasher(name="rentaplats Cicle Standard",
                      cycleLoad=1.655,
                      cycleTime=2*60,
                      washingConfig=washDishesConf)

perfil=Profile(solarIrradiation=solarIrradiation,
               loadFactors=[dishwasherEco,dishwasherStd,solarPanel])

perfil.generate_loads(LoadConfig(Granularity.Hour),iters=500)