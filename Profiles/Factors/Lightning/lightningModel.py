from utils.enums import LightType

class LightningModel:
    """
    Represents a lighting model that defines the type and number of lights, and their power characteristics.

    This class provides methods to calculate the maximum power consumption based on the type of lights used.

    Attributes:
        _name (str): The name of the lighting model.

        _lightsType (LightType): The type of lights (e.g., LED, CFL, Incandescent).
        
        _lightsNumber (int): The number of lights in the model.

    Methods:
        get_name() -> str:
            Returns the name of the lighting model.

        get_max_power() -> float:
            Calculates the total maximum power consumption for all lights.

        get_power_per_light() -> float:
            Returns the power consumption per individual light based on its type.
    """
    def __init__(self,name:str,lightsType:LightType,lightsNumber:int) -> None:
        """
        Initializes a LightningModel instance with the specified name, light type, and number of lights.

        Args:
            name (str): The name of the lighting model.
            lightsType (LightType): The type of lights to be used.
            lightsNumber (int): The total number of lights.
        """
        self._name=name
        self._lightsType=lightsType
        self._lightsNumber=lightsNumber

    def get_name(self)->str:
        """
        Returns the name of the lighting model.

        Returns:
            str: The name of the lighting model.
        """
        return self._name
    
    def get_max_power(self)->float:
        """
        Calculates the total maximum power consumption for all lights in the model.

        Returns:
            float: The total maximum power consumption in kilowatts.
        """
        return self.get_power_per_light()*self._lightsNumber

    def get_power_per_light(self)->float:
        """
        Returns the power consumption per individual light based on its type.

        Returns:
            float: The power consumption of a single light in kilowatts.
        """
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
        