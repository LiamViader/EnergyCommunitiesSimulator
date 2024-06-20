from Profiles.profile import Profile
from Profiles.loadConfiguration import LoadConfig
from utils.enums import Granularity
from Profiles.Dishwasher.dishwasher import Dishwasher
from Profiles.Dishwasher.washingConfig import WashingDishesConfig
from utils.minuteInterval import MinuteInterval



washDishesConf=WashingDishesConfig(timesWeekly=7,
                                   intervals=[MinuteInterval(14,15,True),
                                              MinuteInterval(9,11,True)])

dishwasher=Dishwasher(name="rentaplats",
                      cycleLoad=0.9,
                      cycleTime=3.5*60,
                      washingConfig=washDishesConf)

dishwasher2=Dishwasher(name="rentaplats2",
                      cycleLoad=1.655,
                      cycleTime=2*60,
                      washingConfig=washDishesConf)

perfil=Profile(loadConsumers=[dishwasher,dishwasher2])
perfil.generate_loads(LoadConfig(Granularity.Minute),iters=500)