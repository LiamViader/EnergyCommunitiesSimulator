import random

class CyclicModel():
    def __init__(self,name:str,
                 cycleLoad:float, 
                 cycleTime:int, 
                 standByPower:float,
                 standByTime:float
                 ):
        self.name=name
        self.cycleLoad=cycleLoad #consum del cicle en kwh
        self.cycleTime=cycleTime #temps que dura el cicle en hores
        self.standByPower=standByPower #potencia que consumeix en standby en kw
        self.standByTime=standByTime #temps que sol esta en standby al dia, en hores

    def get_cycle_load(self):
        return self.cycleLoad

    def get_cycle_time(self): #retorna el temps de rentat en minuts
        return self.cycleTime*60

    def get_stand_by_load(self,hours):#returns load in kwh of standby power during hours
        probability=self.standByTime/24
        number=random.random()
        if number<probability:
            return self.standByPower*hours
        else:
            return 0
    
    def get_name(self):
        return self.name