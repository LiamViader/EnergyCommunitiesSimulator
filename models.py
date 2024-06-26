from Profiles.LoadFactors.Cyclic.cyclicModel import CyclicModel

MODELS ={
    'DISHWASHERS': {
        'STANDARD': CyclicModel(name='dishwasher standard',
                                cycleLoad=1.655,
                                cycleTime=2,
                                standByPower=0.0007,
                                standByTime=24
                                ),
        'ECO': CyclicModel(name='dishwasher eco',
                        cycleLoad=0.9,
                        cycleTime=3.5,
                        standByPower=0.0007,
                        standByTime=24
                        )
    }
}