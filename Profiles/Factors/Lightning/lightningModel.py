from utils.enums import LightType

class LightningModel:
    def __init__(self,name:str,lightsType:LightType,lightsNumber:int) -> None:
        self.name=name
        self.lightsType=lightsType
        self.lightsNumber=lightsNumber

    def get_name(self)->str:
        return self.name
    
    def get_max_power(self)->float:
        return self.get_power_per_light()*self.lightsNumber

    def get_power_per_light(self)->float:
        if self.lightsType==LightType.Led:
            return 0.012
        elif self.lightsType==LightType.Cfl:
            return 0.017
        elif self.lightsType==LightType.Incandescent:
            return 0.065
        elif self.lightsType==LightType.FluorescentTube:
            return 0.025
        elif self.lightsType==LightType.Halogen:
            return 0.035
        elif self.lightsType==LightType.Neon:
            return 0.040
        