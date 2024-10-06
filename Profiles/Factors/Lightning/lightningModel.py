from utils.enums import LightType

class LightningModel:
    def __init__(self,name:str,lightsType:LightType,lightsNumber:int) -> None:
        self._name=name
        self._lightsType=lightsType
        self._lightsNumber=lightsNumber

    def get_name(self)->str:
        return self._name
    
    def get_max_power(self)->float:
        return self.get_power_per_light()*self._lightsNumber

    def get_power_per_light(self)->float:
        if self._lightsType==LightType.Led:
            return 0.012
        elif self._lightsType==LightType.Cfl:
            return 0.017
        elif self._lightsType==LightType.Incandescent:
            return 0.065
        elif self._lightsType==LightType.FluorescentTube:
            return 0.025
        elif self._lightsType==LightType.Halogen:
            return 0.035
        elif self._lightsType==LightType.Neon:
            return 0.040
        