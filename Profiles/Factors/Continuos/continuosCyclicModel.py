import random
import numpy as np
from utils.RandomNumbers.baseNumberDistribution import BaseNumberDistribution

class ContinuosCyclicModel():
    """
    A model representing a continuous cyclic process or device that alternates between active and idle states.

    This class encapsulates the behavior of devices or systems that operate in cycles, with defined power consumption
    during both active and idle phases. The model also defines the duration of these phases and the time between cycles.

    Attributes:
        _name (str): The name of the cyclic model, representing the device or process.
        _idlePower (BaseNumberDistribution): The power consumption (in kW) when the device is idle.
        _activePower (BaseNumberDistribution): The power consumption (in kW) when the device is active.
        _timeBetweenCycles (BaseNumberDistribution): The time (in hours) between the end of one cycle and the start of the next.
        _cycleDuration (BaseNumberDistribution): The duration of the active cycle (in hours).

    Methods:
        get_active_power() -> float:
            Returns the power consumption during the active phase.
        get_idle_power() -> float:
            Returns the power consumption during the idle phase.
        get_name() -> str:
            Returns the name of the cyclic model.
        get_time_between_next_cycle() -> float:
            Returns the time between the current and next cycle (in hours).
        get_cycle_duration() -> float:
            Returns the duration of the active cycle (in hours).
    """
    def __init__(self, name: str, idlePower: BaseNumberDistribution, activePower: BaseNumberDistribution, timeBetweenCycles:BaseNumberDistribution, cycleDuration:BaseNumberDistribution):
        """
        Initializes the ContinuosCyclicModel with the given parameters.

        Args:
            name (str): The name of the cyclic process or device.
            idlePower (BaseNumberDistribution): The power consumption during idle times (in kW).
            activePower (BaseNumberDistribution): The power consumption during active times (in kW).
            timeBetweenCycles (BaseNumberDistribution): The time between cycles (in hours).
            cycleDuration (BaseNumberDistribution): The duration of each active cycle (in hours).
        """
        self._name=name
        self._idlePower = idlePower #potencia quan no està en el cicle actiu en kw
        self._activePower = activePower
        self._timeBetweenCycles = timeBetweenCycles
        self._cycleDuration = cycleDuration



    def get_active_power(self)->float:
        """
        Returns the power consumption during the active phase of the cycle.

        The power is generated randomly based on the defined distribution for active power.

        Returns:
            float: The power consumption during the active phase (in kW).
        """
        return self._activePower.generate_random()

    def get_idle_power(self)->float:
        """
        Returns the power consumption during the idle phase of the cycle.

        The power is generated randomly based on the defined distribution for idle power.

        Returns:
            float: The power consumption during the idle phase (in kW).
        """
        return self._idlePower.generate_random()

    def get_name(self)->str:
        """
        Returns the name of the cyclic model.

        Returns:
            str: The name of the model.
        """
        return self._name
    
    def get_time_between_next_cycle(self)->float:
        """
        Returns the time (in hours) between the current cycle and the next cycle.

        The time is generated randomly based on the defined distribution for the time between cycles.

        Returns:
            float: The time between the current and next cycle (in hours).
        """
        return self._timeBetweenCycles.generate_random()
    
    def get_cycle_duration(self)->float:
        """
        Returns the duration (in hours) of the active cycle.

        The duration is generated randomly based on the defined distribution for the cycle duration.

        Returns:
            float: The duration of the active cycle (in hours).
        """
        return self._cycleDuration.generate_random()
