from Profiles.Factors.Cyclic.cyclicModel import CyclicModel
from utils.RandomNumbers.fixedValueDistribution import FixedValueDistribution
from utils.RandomNumbers.truncatedNormalDistribution import TruncatedNormalDistribution
from utils.RandomNumbers.piecewiseUniformDistribution import PiecewiseUniformDistribution
from Profiles.Factors.Continuos.continuosCyclicModel import ContinuosCyclicModel
from Profiles.Battery.battery import Battery

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
}