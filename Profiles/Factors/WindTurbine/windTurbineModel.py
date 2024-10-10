class WindTurbineModel:
    """
    Represents a model of a wind turbine to calculate the power output based on wind speed.

    This class encapsulates the characteristics of a wind turbine, including its minimum wind speed, 
    optimal wind speed, and nominal power output. It provides methods to retrieve the turbine's name 
    and to calculate the power produced given a specific wind speed.

    Attributes:
        _minWindVel (float): The minimum wind velocity (in m/s) required for the turbine to generate power.

        _optimalWindVel (float): The optimal wind velocity (in m/s) for maximum efficiency and power generation.

        _nominalPower (float): The nominal power output (in kW) of the turbine at optimal wind speed.
        
        _name (str): The name of the wind turbine model.
    
    Methods:
        get_name() -> str:
            Returns the name of the wind turbine model.
        
        get_power(windVel: float) -> float:
            Calculates and returns the power output (in kW) based on the given wind velocity (in m/s).
    """
    def __init__(self,name:str,minWindVel:float,optimalWindVel:float,nominalPower:float) -> None:
        """
        Initializes the WindTurbineModel with specified characteristics.

        Args:
            name (str): The name of the wind turbine model.
            minWindVel (float): The minimum wind velocity required for power generation (in m/s).
            optimalWindVel (float): The optimal wind velocity for maximum power output (in m/s).
            nominalPower (float): The nominal power output of the turbine (in kW).
        """
        self._minWindVel=minWindVel
        self._optimalWindVel=optimalWindVel
        self._nominalPower=nominalPower
        self._name=name
    
    def get_name(self)->str:
        """
        Returns the name of the wind turbine model.

        Returns:
            str: The name of the wind turbine.
        """
        return self._name
    
    def get_power(self,windVel:float)->float:
        """
        Calculates and returns the power output based on the given wind velocity.

        Args:
            windVel (float): The wind velocity (in m/s).

        Returns:
            float: The power output (in kW) of the wind turbine for the specified wind velocity.
        """
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
            