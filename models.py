from Profiles.Factors.Cyclic.cyclicModel import CyclicModel
from utils.RandomNumbers.fixedValueDistribution import FixedValueDistribution
from utils.RandomNumbers.truncatedNormalDistribution import TruncatedNormalDistribution
from utils.RandomNumbers.piecewiseUniformDistribution import PiecewiseUniformDistribution
from Profiles.Factors.Continuos.continuosCyclicModel import ContinuosCyclicModel
from Profiles.Battery.battery import Battery
from Profiles.Factors.ElectricCar.electricCarModel import ElectricCarModel
from Profiles.Factors.WindTurbine.windTurbineModel import WindTurbineModel

MODELS ={
    'DISHWASHERS': {
        'STANDARD': CyclicModel(
            name='dishwasher standard',
            cyclePower=0.825,
            cycleTime=2,
            standByPower=0.0007,
            standByTime=24
        ),
        'ECO': CyclicModel(
            name='dishwasher eco',
            cyclePower=0.26,
            cycleTime=3.5,
            standByPower=0.0007,
            standByTime=24
        ),
    },
    'WASHING_MACHINES':{
        'STANDARD': CyclicModel(
            name='washing machine standard',
            cyclePower=1.0,
            cycleTime=1.5,
            standByPower=0.0005,
            standByTime=22.5   
        ),
        'HIGH_EFFICIENCY': CyclicModel(
            name='washing machine high efficiency',
            cyclePower=0.75,
            cycleTime=1.25,
            standByPower=0.0003,
            standByTime=22.75
        ),
        'FRONT_LOAD': CyclicModel(
            name='washing machine front load',
            cyclePower=0.9,
            cycleTime=1.75,
            standByPower=0.0004,
            standByTime=22.25
        ),
        'COMPACT': CyclicModel(
            name='washing machine compact',
            cyclePower=0.5,
            cycleTime=1.0,
            standByPower=0.0002,
            standByTime=23.0
        ),
    },
    'BATTERIES':{
        'STANDARD': Battery(
            capacity=13.5,
            chargeRate=5.0,
            dischargeRate=5.0,
            chargingEfficiency=0.95,
            dischargingEfficiency=0.95
        ),
    },
    'REFRIGERATORS':{
        'FIXED_COMPRESSOR_EXAMPLE': ContinuosCyclicModel(
            name="refrigerator standard fixed compressor",
            idlePower=FixedValueDistribution(0.002),
            activePower=FixedValueDistribution(0.16),
            timeBetweenCycles=TruncatedNormalDistribution(0.2,40/60,50/60),
            cycleDuration=TruncatedNormalDistribution(0.2,30/60,35/60)
        ),
        'VARIABLE_COMPRESSOR_EXAMPLE': ContinuosCyclicModel(
            name="refrigerator standard variable compressor",
            idlePower=FixedValueDistribution(0.002),
            activePower=PiecewiseUniformDistribution(
                ranges=[(0.2, 0.15), (0.15, 0.125), (0.125, 0.06), (0.06, 0.04)],
                probabilities=[0.15, 0.08, 0.07, 0.70]
            ),
            timeBetweenCycles=TruncatedNormalDistribution(0.3,20/60,60/60,40/60),
            cycleDuration=TruncatedNormalDistribution(0.5,150/60,30/60,90/60)
        )

    },
    'FREEZERS':{
        'FIXED_COMPRESSOR': ContinuosCyclicModel(
            name="freezer standard fixed compressor",
            idlePower=FixedValueDistribution(0.003),
            activePower=FixedValueDistribution(0.25),
            timeBetweenCycles=TruncatedNormalDistribution(0.3, 50/60, 70/60),
            cycleDuration=TruncatedNormalDistribution(0.3, 40/60, 50/60)
        ),
        'VARIABLE_COMPRESSOR': ContinuosCyclicModel(
            name="freezer standard variable compressor",
            idlePower=FixedValueDistribution(0.003),
            activePower=PiecewiseUniformDistribution(
                ranges=[(0.25, 0.2), (0.2, 0.15), (0.15, 0.1), (0.1, 0.05)],
                probabilities=[0.15, 0.2, 0.3, 0.35]
            ),
            timeBetweenCycles=TruncatedNormalDistribution(0.4, 30/60, 90/60, 60/60),
            cycleDuration=TruncatedNormalDistribution(0.5, 60/60, 90/60, 75/60)
        ),
        'HIGH_EFFICIENCY_VARIABLE_COMPRESSOR': ContinuosCyclicModel(
            name="freezer high efficiency variable compressor",
            idlePower=FixedValueDistribution(0.002),
            activePower=PiecewiseUniformDistribution(
                ranges=[(0.2, 0.15), (0.15, 0.1), (0.1, 0.05), (0.05, 0.03)],
                probabilities=[0.2, 0.25, 0.3, 0.25] 
            ),
            timeBetweenCycles=TruncatedNormalDistribution(0.4, 45/60, 120/60, 75/60),
            cycleDuration=TruncatedNormalDistribution(0.4, 70/60, 100/60, 85/60)
        ),
        'COMPACT_FIXED_COMPRESSOR': ContinuosCyclicModel(
            name="compact freezer fixed compressor",
            idlePower=FixedValueDistribution(0.002),
            activePower=FixedValueDistribution(0.18),
            timeBetweenCycles=TruncatedNormalDistribution(0.3, 40/60, 60/60),
            cycleDuration=TruncatedNormalDistribution(0.3, 30/60, 40/60)
        ),
    },
    'ELECTRIC_CARS':{
        'TESLA': ElectricCarModel(
            name="Tesla",
            chargePower=11.5,
            consumptionPerKm=0.18,
            batteryCapacity=75,
            chargeEfficiency=0.95
        ),
    },
    'WIND_TURBINES':{
        'TUGE10KW':WindTurbineModel(
            name="WindTurbine-TUGE10KW",
            minWindVel=4,
            optimalWindVel=10.7,
            nominalPower=9
        )
    },
}