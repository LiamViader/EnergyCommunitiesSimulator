class WindTurbineModel:
    def __init__(self,name:str,minWindVel:float,optimalWindVel:float,nominalPower:float) -> None:
        self._minWindVel=minWindVel
        self._optimalWindVel=optimalWindVel
        self._nominalPower=nominalPower
        self._name=name
    
    def get_name(self)->str:
        return self._name
    
    def get_power(self,windVel:float)->float:#retorna la potencia en kw segons la velocitat del vent en m/s
        if windVel<self._minWindVel:
            return 0
        else:
            windVelOffseted=windVel-self._minWindVel
            lengthOfWindVels=self._optimalWindVel-self._minWindVel
            if lengthOfWindVels<=0: return 0
            windVelOffseted=min(windVelOffseted,lengthOfWindVels)
            proportion=windVelOffseted/lengthOfWindVels
            power=proportion*self._nominalPower
            return power
            