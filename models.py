from Profiles.Factors.Cyclic.cyclicModel import CyclicModel
from Profiles.Battery.battery import Battery

MODELS ={
    'DISHWASHERS': {
        'STANDARD': CyclicModel(name='dishwasher standard',
                                cyclePower=0.825,
                                cycleTime=2,
                                standByPower=0.0007,
                                standByTime=24
                                ),
        'ECO': CyclicModel(name='dishwasher eco',
                            cyclePower=0.26,
                            cycleTime=3.5,
                            standByPower=0.0007,
                            standByTime=24
                            ),
    },
    'BATTERIES':{
        'STANDARD': Battery(capacity=13.5,
                            chargeRate=5.0,
                            dischargeRate=5.0,
                            chargingEfficiency=0.95,
                            dischargingEfficiency=0.95
                            ),
    },
}