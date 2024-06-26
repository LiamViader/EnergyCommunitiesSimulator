import random

class CyclicModel():
    def __init__(self,name:str,
                 cyclePower:float, 
                 cycleTime:int, 
                 standByPower:float,
                 standByTime:float
                 ):
        self.name=name
        self.cyclePower=cyclePower #potencia mitja durant el cicle (en un futur es podria usar dades de com es la potencia al llarg del temps durant un cicle)
        self.cycleTime=cycleTime #temps que dura el cicle en hores
        self.standByPower=standByPower #potencia que consumeix en standby en kw
        self.standByTime=standByTime #temps que sol esta en standby al dia, en hores

    def get_cycle_power(self):
        return self.cyclePower

    def get_cycle_time(self): #retorna el temps de rentat en minuts
        return self.cycleTime*60

    def get_stand_by_power(self):#returns load in kwh of standby power during hours
        probability=self.standByTime/24
        number=random.random()
        if number<probability:
            return self.standByPower
        else:
            return 0
    
    def get_name(self):
        return self.name