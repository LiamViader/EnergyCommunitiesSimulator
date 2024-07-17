class WindTurbineModel:
    def __init__(self,name:str,minWindVel:float,optimalWindVel:float,nominalPower:float) -> None:
        self.minWindVel=minWindVel
        self.optimalWindVel=optimalWindVel
        self.nominalPower=nominalPower
        self.name=name
    
    def get_name(self)->str:
        return self.name
    
    def get_power(self,windVel:float)->float:#retorna la potencia en kw segons la velocitat del vent en m/s
        if windVel<self.minWindVel:
            return 0
        else:
            windVelOffseted=windVel-self.minWindVel
            lengthOfWindVels=self.optimalWindVel-self.minWindVel
            if lengthOfWindVels<=0: return 0
            windVelOffseted=min(windVelOffseted,lengthOfWindVels)
            proportion=windVelOffseted/lengthOfWindVels
            power=proportion*self.nominalPower
            return power
            