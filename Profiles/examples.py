from Profiles.profile import Profile
from Profiles.Factors.Climatitzation.Components.heating import Heating
from Profiles.Factors.Climatitzation.Components.cooling import Cooling
from Profiles.Factors.Climatitzation.climatitzationFactor import ClimatitzationFactor
from Profiles.Factors.Climatitzation.thermostat import Thermostat
from utils.minuteInterval import MinuteInterval
from Profiles.Factors.Cyclic.cyclicFactor import CyclicFactor
from Profiles.Factors.Cyclic.cyclicModel import CyclicModel
from Profiles.Factors.Cyclic.UseConfig.cyclicWeeklyUseConfig import CyclicWeeklyUseConfig
from Profiles.Factors.Cyclic.UseConfig.cyclicDaylyUseConfig import CyclicDaylyUseConfig
from Profiles.Factors.Continuos.continuosCyclicFactor import ContinuosCyclicFactor
from Profiles.Factors.Continuos.continuosCyclicModel import ContinuosCyclicModel
from Profiles.Factors.Lightning.lightningFactor import LightningFactor
from Profiles.Factors.Lightning.lightningModel import LightningModel
from utils.enums import LightType, FactorType
from utils.RandomNumbers.normalDistribution import NormalDistribution
from utils.RandomNumbers.truncatedNormalDistribution import TruncatedNormalDistribution
from utils.RandomNumbers.fixedValueDistribution import FixedValueDistribution
from Profiles.Factors.Continuos.continuosFactor import ContinuosFactor
from Profiles.Factors.SolarPanel.solarPV import SolarPV
from Profiles.Factors.SolarPanel.solarPanel import SolarPanel
from Profiles.Factors.ElectricCar.electricCarFactor import ElectricCarFactor
from Profiles.Factors.ElectricCar.electricCarModel import ElectricCarModel
from Profiles.Factors.ElectricCar.UseConfig.carOnNeedUseConfig import CarOnNeedUseConfig
from Profiles.Factors.WindTurbine.windTurbineFactor import WindTurbineFactor
from models import MODELS

small_apartment_1=Profile(
    name='small_apartment_1',
    exteriorContactArea=30,
    insideVolume=125,
    loadFactors=[
        ClimatitzationFactor(
            name="Climatitzation_heating",
            climatitzationComponents=[
                Heating(
                    maxPower=5,
                    minPower=1,
                    efficiency=0.9,
                    volume=125
                ),
            ],
            thermostat=Thermostat(
                idealTemperatures=[
                    (MinuteInterval(6,10,True),22),
                    (MinuteInterval(12,24,True),22)
                ],
                startingTemperature=22
            )
        ),
        CyclicFactor(
            cyclicModel=MODELS['DISHWASHERS']['STANDARD'],
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=5,
                intervals=[
                    MinuteInterval(10,12,True),
                    MinuteInterval(16,17,True)
                ]
            )
        ),
        CyclicFactor(
            cyclicModel=MODELS['WASHING_MACHINES']['STANDARD'],
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=3,
                intervals=[
                    MinuteInterval(13,15,True),
                    MinuteInterval(20,22,True)
                ]
            )
        ),
        ContinuosCyclicFactor(
            model=MODELS['REFRIGERATORS']['VARIABLE_COMPRESSOR_EXAMPLE']
        ),
        ContinuosCyclicFactor(
            model=MODELS['FREEZERS']['VARIABLE_COMPRESSOR']
        ),
        LightningFactor(
            model=LightningModel(
                name='lightningIncandescent',
                lightsType=LightType.Incandescent,
                lightsNumber=4
            ),
            activityIntervals=[
                (MinuteInterval(5.5,7,True),0.8),
                (MinuteInterval(16,19,True),0.5),
                (MinuteInterval(19,1,True),0.9)
            ]
        ),
        LightningFactor(
            model=LightningModel(
                name='lightningLed',
                lightsType=LightType.Led,
                lightsNumber=6
            ),
            activityIntervals=[
                (MinuteInterval(5.5,7,True),0.8),
                (MinuteInterval(16,19,True),0.5),
                (MinuteInterval(19,1,True),0.9)
            ]
        ),
        CyclicFactor(
            cyclicModel=CyclicModel(
                name='Vitro',
                cyclePower=TruncatedNormalDistribution(std=1,min=1.2,max=3.6,mu=1.2),
                cycleTime=TruncatedNormalDistribution(std=0.2,min=0,max=1.2,mu=0.3),
                standByPower=FixedValueDistribution(0),
                standByTime=24
            ),
            useConfig=CyclicDaylyUseConfig(
                weekUsage=(
                    [MinuteInterval(20,22,True)],
                    [MinuteInterval(20,22,True)],
                    [MinuteInterval(20,22,True)],
                    [MinuteInterval(20,22,True)],
                    [MinuteInterval(20,22,True)],
                    [MinuteInterval(12,15,True),MinuteInterval(20,22,True)],
                    [MinuteInterval(12,15,True),MinuteInterval(20,22,True)]
                )
            )
        ),
        CyclicFactor(
            cyclicModel=CyclicModel(
                name='ElectricFurnace',
                cyclePower=FixedValueDistribution(2),
                cycleTime=TruncatedNormalDistribution(std=0.2,min=0.3,max=1.5,mu=0.6),
                standByPower=FixedValueDistribution(0.0006),
                standByTime=24
            ),
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=3,
                intervals=[MinuteInterval(20,22,True)]
            )
        ),
        ContinuosFactor(
            name='others',
            factorType=FactorType.Consumer,
            constantPower=TruncatedNormalDistribution(std=0.03,min=0.01,max=0.1,mu=0.02)
        ),
        SolarPV(
            name='SolarPv',
            solarPanels=[SolarPanel('solarPanel',0.3,0.8) for i in range(5)]
        ),
        CyclicFactor(
            cyclicModel=MODELS['OTHER_DEVICES']['TELEVISION1'],
            useConfig=CyclicDaylyUseConfig(
                weekUsage=[
                    [MinuteInterval(18, 23, True)],
                    [MinuteInterval(18, 23, True)],
                    [MinuteInterval(18, 23, True)],
                    [MinuteInterval(18, 23, True)],
                    [MinuteInterval(18, 23, True)],
                    [MinuteInterval(10, 14, True), MinuteInterval(18, 23, True)],
                    [MinuteInterval(10, 14, True), MinuteInterval(18, 23, True)]
                ]
            )
        ),
        CyclicFactor(
            cyclicModel=MODELS['OTHER_DEVICES']['LAPTOP1'],
            useConfig=CyclicDaylyUseConfig(
                weekUsage=[
                    [MinuteInterval(9, 17, True)],
                    [MinuteInterval(9, 17, True)],
                    [MinuteInterval(9, 17, True)],
                    [MinuteInterval(9, 17, True)],
                    [MinuteInterval(9, 17, True)],
                    [MinuteInterval(10, 14, True)],
                    [MinuteInterval(10, 14, True)]
                ]
            )
        ),
        CyclicFactor(
            cyclicModel=MODELS['OTHER_DEVICES']['MICROWAVE1'],
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=14,
                intervals=[
                    MinuteInterval(8, 9, True),
                    MinuteInterval(18, 19, True)
                ]
            )
        ),
        CyclicFactor(
            cyclicModel=MODELS['OTHER_DEVICES']['TOASTER1'],
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=7,
                intervals=[
                    MinuteInterval(8, 9, True)
                ]
            )
        ),
        CyclicFactor(
            cyclicModel=MODELS['OTHER_DEVICES']['HAIRDRYER1'],
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=7,
                intervals=[
                    MinuteInterval(7, 8, True)
                ]
            )
        ),
    ],
)

small_apartment_2 = Profile(
    name='small_apartment_2',
    exteriorContactArea=35,
    insideVolume=130,
    loadFactors=[
        # Climatización (calefacción)
        ClimatitzationFactor(
            name="Climatitzation_heating",
            climatitzationComponents=[
                Heating(
                    maxPower=4,
                    minPower=1,
                    efficiency=0.9,
                    volume=130
                ),
            ],
            thermostat=Thermostat(
                idealTemperatures=[
                    (MinuteInterval(6,8,True),21),
                    (MinuteInterval(18,22,True),21)
                ],
                startingTemperature=18
            )
        ),
        # Lavavajillas
        CyclicFactor(
            cyclicModel=CyclicModel(
                name='Dishwasher',
                cyclePower=FixedValueDistribution(1.2),
                cycleTime=FixedValueDistribution(1.2),
                standByPower=FixedValueDistribution(0),
                standByTime=24
            ),
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=3,
                intervals=[
                    MinuteInterval(8,9,True),
                    MinuteInterval(20,21,True)
                ]
            )
        ),
        # Refrigerador
        ContinuosCyclicFactor(
            model=MODELS['REFRIGERATORS']['VARIABLE_COMPRESSOR_EXAMPLE']
        ),
        # Iluminación (LED)
        LightningFactor(
            model=LightningModel(
                name='lightningLed',
                lightsType=LightType.Led,
                lightsNumber=10
            ),
            activityIntervals=[
                (MinuteInterval(7,8,True),0.6),
                (MinuteInterval(18,23,True),0.7),
                (MinuteInterval(23,1,True),0.9)
            ]
        ),
        # Televisor
        CyclicFactor(
            cyclicModel=CyclicModel(
                name='Television',
                cyclePower=FixedValueDistribution(0.1),
                cycleTime=FixedValueDistribution(5),
                standByPower=FixedValueDistribution(0.01),
                standByTime=19
            ),
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=7,
                intervals=[
                    MinuteInterval(18,23,True)
                ]
            )
        ),
        # Consola de videojuegos
        CyclicFactor(
            cyclicModel=CyclicModel(
                name='GameConsole',
                cyclePower=FixedValueDistribution(0.08),
                cycleTime=FixedValueDistribution(3),
                standByPower=FixedValueDistribution(0.01),
                standByTime=21
            ),
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=5,
                intervals=[
                    MinuteInterval(19,22,True)
                ]
            )
        ),
        # Otros consumidores continuos
        ContinuosFactor(
            name='others',
            factorType=FactorType.Consumer,
            constantPower=FixedValueDistribution(0.06)
        )
    ],
)

small_apartment_3 = Profile(
    name='small_apartment_3',
    exteriorContactArea=25,
    insideVolume=110,
    loadFactors=[
        # Climatización (calefacción)
        ClimatitzationFactor(
            name="Climatitzation_heating",
            climatitzationComponents=[
                Heating(
                    maxPower=2,
                    minPower=0.5,
                    efficiency=0.9,
                    volume=110
                ),
            ],
            thermostat=Thermostat(
                idealTemperatures=[
                    (MinuteInterval(6,9,True),20),
                    (MinuteInterval(18,22,True),20)
                ],
                startingTemperature=18
            )
        ),
        # Refrigerador
        ContinuosCyclicFactor(
            model=MODELS['REFRIGERATORS']['FIXED_COMPRESSOR_EXAMPLE']
        ),
        # Iluminación (incandescente)
        LightningFactor(
            model=LightningModel(
                name='lightningIncandescent',
                lightsType=LightType.Incandescent,
                lightsNumber=6
            ),
            activityIntervals=[
                (MinuteInterval(7,9,True),0.7),
                (MinuteInterval(18,21,True),0.6),
                (MinuteInterval(21,23,True),0.8)
            ]
        ),
        # Microondas
        CyclicFactor(
            cyclicModel=CyclicModel(
                name='Microwave',
                cyclePower=FixedValueDistribution(1.2),
                cycleTime=FixedValueDistribution(0.1),
                standByPower=FixedValueDistribution(0.001),
                standByTime=23.9
            ),
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=7,
                intervals=[
                    MinuteInterval(7,8,True),
                    MinuteInterval(12,13,True),
                    MinuteInterval(18,19,True)
                ]
            )
        ),
        # Laptop
        CyclicFactor(
            cyclicModel=CyclicModel(
                name='Laptop',
                cyclePower=FixedValueDistribution(0.05),
                cycleTime=FixedValueDistribution(8),
                standByPower=FixedValueDistribution(0.01),
                standByTime=16
            ),
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=7,
                intervals=[
                    MinuteInterval(9,17,True)
                ]
            )
        ),
        # Otros consumidores continuos
        ContinuosFactor(
            name='others',
            factorType=FactorType.Consumer,
            constantPower=FixedValueDistribution(0.04)
        ),
        # Paneles solares
        SolarPV(
            name='SolarPv',
            solarPanels=[SolarPanel('solarPanel', 0.3, 0.8) for i in range(8)]
        )
    ],
)

small_apartment_4 = Profile(
    name='small_apartment_4',
    exteriorContactArea=45,
    insideVolume=150,
    loadFactors=[
        # Climatización (calefacción)
        ClimatitzationFactor(
            name="Climatitzation_heating",
            climatitzationComponents=[
                Heating(
                    maxPower=3,
                    minPower=0.8,
                    efficiency=0.9,
                    volume=150
                ),
            ],
            thermostat=Thermostat(
                idealTemperatures=[
                    (MinuteInterval(6,8,True),22),
                    (MinuteInterval(18,22,True),22)
                ],
                startingTemperature=20
            )
        ),
        # Lavadora
        CyclicFactor(
            cyclicModel=CyclicModel(
                name='WashingMachine',
                cyclePower=FixedValueDistribution(1.8),
                cycleTime=FixedValueDistribution(1.5),
                standByPower=FixedValueDistribution(0),
                standByTime=24
            ),
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=5,
                intervals=[
                    MinuteInterval(9,11,True),
                    MinuteInterval(17,19,True)
                ]
            )
        ),
        # Refrigerador
        ContinuosCyclicFactor(
            model=MODELS['REFRIGERATORS']['FIXED_COMPRESSOR_EXAMPLE']
        ),
        # Iluminación (fluorescente)
        LightningFactor(
            model=LightningModel(
                name='lightningFluorescent',
                lightsType=LightType.FluorescentTube,
                lightsNumber=8
            ),
            activityIntervals=[
                (MinuteInterval(7,8,True),0.7),
                (MinuteInterval(18,22,True),0.6),
                (MinuteInterval(22,1,True),0.8)
            ]
        ),
        # Cocina de gas
        CyclicFactor(
            cyclicModel=CyclicModel(
                name='GasStove',
                cyclePower=FixedValueDistribution(0.1),
                cycleTime=FixedValueDistribution(1),
                standByPower=FixedValueDistribution(0),
                standByTime=23
            ),
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=14,
                intervals=[
                    MinuteInterval(7,8,True),
                    MinuteInterval(12,13,True),
                    MinuteInterval(19,20,True)
                ]
            )
        ),
        # Coche eléctrico
        ElectricCarFactor(
            model=MODELS['ELECTRIC_CARS']['TESLA'],
            useConfig=CarOnNeedUseConfig(
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
            ),
        ),
        # Otros consumidores continuos
        ContinuosFactor(
            name='others',
            factorType=FactorType.Consumer,
            constantPower=FixedValueDistribution(0.05)
        )
    ],
)

small_apartment_5 = Profile(
    name='small_apartment_5',
    exteriorContactArea=50,
    insideVolume=160,
    loadFactors=[
        # Climatización (aire acondicionado)
        ClimatitzationFactor(
            name="Climatitzation_cooling",
            climatitzationComponents=[
                Cooling(
                    maxPower=4,
                    minPower=1,
                    efficiency=0.85,
                    volume=160
                ),
            ],
            thermostat=Thermostat(
                idealTemperatures=[
                    (MinuteInterval(8,10,True),24),
                    (MinuteInterval(12,18,True),24),
                    (MinuteInterval(20,24,True),24)
                ],
                startingTemperature=26
            )
        ),
        # Lavavajillas
        CyclicFactor(
            cyclicModel=CyclicModel(
                name='Dishwasher',
                cyclePower=FixedValueDistribution(1.5),
                cycleTime=FixedValueDistribution(1.2),
                standByPower=FixedValueDistribution(0),
                standByTime=24
            ),
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=3,
                intervals=[
                    MinuteInterval(8,9,True),
                    MinuteInterval(20,21,True)
                ]
            )
        ),
        # Refrigerador
        ContinuosCyclicFactor(
            model=MODELS['REFRIGERATORS']['VARIABLE_COMPRESSOR_EXAMPLE']
        ),
        # Iluminación (LED)
        LightningFactor(
            model=LightningModel(
                name='lightningLed',
                lightsType=LightType.Led,
                lightsNumber=10
            ),
            activityIntervals=[
                (MinuteInterval(7,8,True),0.6),
                (MinuteInterval(18,23,True),0.7),
                (MinuteInterval(23,1,True),0.9)
            ]
        ),
        # Oficina en casa (computadora y otros dispositivos)
        CyclicFactor(
            cyclicModel=CyclicModel(
                name='HomeOffice',
                cyclePower=FixedValueDistribution(0.2),
                cycleTime=FixedValueDistribution(8),
                standByPower=FixedValueDistribution(0.05),
                standByTime=16
            ),
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=5,
                intervals=[
                    MinuteInterval(9,17,True)
                ]
            )
        ),
        # Turbina eólica
        WindTurbineFactor(
            model=MODELS['WIND_TURBINES']['SMALL2KW']
        ),
        # Otros consumidores continuos
        ContinuosFactor(
            name='others',
            factorType=FactorType.Consumer,
            constantPower=FixedValueDistribution(0.06)
        )
    ],
)

small_apartment_6 = Profile(
    name='small_apartment_6',
    exteriorContactArea=35,
    insideVolume=140,
    loadFactors=[
        # Climatización (calefacción)
        ClimatitzationFactor(
            name="Climatitzation_heating",
            climatitzationComponents=[
                Heating(
                    maxPower=2,
                    minPower=0.5,
                    efficiency=0.9,
                    volume=140
                ),
            ],
            thermostat=Thermostat(
                idealTemperatures=[
                    (MinuteInterval(7,9,True),20),
                    (MinuteInterval(18,22,True),20)
                ],
                startingTemperature=18
            )
        ),
        # Refrigerador
        ContinuosCyclicFactor(
            model=MODELS['REFRIGERATORS']['VARIABLE_COMPRESSOR_EXAMPLE']
        ),
        # Iluminación (incandescente)
        LightningFactor(
            model=LightningModel(
                name='lightningIncandescent',
                lightsType=LightType.Incandescent,
                lightsNumber=6
            ),
            activityIntervals=[
                (MinuteInterval(7,9,True),0.7),
                (MinuteInterval(18,21,True),0.6),
                (MinuteInterval(21,23,True),0.8)
            ]
        ),
        # Microondas
        CyclicFactor(
            cyclicModel=CyclicModel(
                name='Microwave',
                cyclePower=FixedValueDistribution(1.2),
                cycleTime=FixedValueDistribution(0.1),
                standByPower=FixedValueDistribution(0.001),
                standByTime=23.9
            ),
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=7,
                intervals=[
                    MinuteInterval(7,8,True),
                    MinuteInterval(12,13,True),
                    MinuteInterval(18,19,True)
                ]
            )
        ),
        # Laptop
        CyclicFactor(
            cyclicModel=CyclicModel(
                name='Laptop',
                cyclePower=FixedValueDistribution(0.05),
                cycleTime=FixedValueDistribution(8),
                standByPower=FixedValueDistribution(0.01),
                standByTime=16
            ),
            useConfig=CyclicWeeklyUseConfig(
                timesWeekly=7,
                intervals=[
                    MinuteInterval(9,17,True)
                ]
            )
        ),
        # Otros consumidores continuos
        ContinuosFactor(
            name='others',
            factorType=FactorType.Consumer,
            constantPower=FixedValueDistribution(0.04)
        ),
        # Paneles solares
        SolarPV(
            name='SolarPv',
            solarPanels=[SolarPanel('solarPanel', 0.3, 0.8) for i in range(6)]
        ),
        # Turbina eólica
        WindTurbineFactor(
            model=MODELS['WIND_TURBINES']['BASIC5KW']
        )
    ],
)
