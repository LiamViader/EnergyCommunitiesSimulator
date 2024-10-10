
class ElectricCarModel():
    """
    A model representing the characteristics and energy consumption of an electric car.

    This class encapsulates the properties of an electric vehicle in terms of its energy consumption per kilometer,
    charging power, battery capacity, and charging efficiency. It provides methods to retrieve these values.

    Attributes:
        _name (str): The name of the electric car model.

        _consumptionPerKm (float): Average energy consumption per kilometer in kilowatt-hours (kWh/km).

        _chargePower (float): Charging power in kilowatts (kW).

        _batteryCapacity (float): Battery capacity in kilowatt-hours (kWh).
        
        _chargeEfficiency (float): Charging efficiency as a decimal (0 to 1).
    
    Methods:
        get_charge_power() -> float:
            Returns the charging power of the electric car.
        get_battery_capacity() -> float:
            Returns the battery capacity of the electric car.
        get_charge_efficiency() -> float:
            Returns the charging efficiency of the electric car.
        get_name() -> str:
            Returns the name of the electric car model.
        get_consumption_per_km() -> float:
            Returns the energy consumption per kilometer of the electric car (in kWh/km).
    """
    def __init__(self, name: str, chargePower: float, consumptionPerKm:float, batteryCapacity: float, chargeEfficiency: float):
        """
        Initializes the ElectricCarModel with the given parameters.

        Args:
            name (str): The name of the electric car model.
            chargePower (float): The power at which the car charges (in kW).
            consumptionPerKm (float): The energy consumption per kilometer (in kWh/km).
            batteryCapacity (float): The capacity of the car's battery (in kWh).
            chargeEfficiency (float): The efficiency of charging, expressed as a decimal (0 to 1).
        """
        self._name = name
        self._consumptionPerKm = consumptionPerKm
        self._chargePower = chargePower 
        self._batteryCapacity = batteryCapacity
        self._chargeEfficiency = chargeEfficiency 

    def get_charge_power(self):
        """
        Returns the charging power of the electric car.

        The charging power defines how fast the car can be charged, measured in kilowatts (kW).

        Returns:
            float: Charging power in kW.
        """
        return self._chargePower

    def get_battery_capacity(self):
        """
        Returns the battery capacity of the electric car.

        The battery capacity defines how much energy the battery can store, measured in kilowatt-hours (kWh).

        Returns:
            float: Battery capacity in kWh.
        """
        return self._batteryCapacity

    def get_charge_efficiency(self):
        """
        Returns the charging efficiency of the electric car.

        Charging efficiency is the percentage of energy that is effectively stored in the battery during charging,
        with the rest lost as heat or other inefficiencies.

        Returns:
            float: Charging efficiency as a decimal (0 to 1).
        """
        return self._chargeEfficiency

    def get_name(self):
        """
        Returns the name of the electric car model.

        Returns:
            str: The name of the electric car.
        """
        return self._name
    
    def get_consumption_per_km(self): #en kwh
        """
        Returns the energy consumption per kilometer of the electric car.

        This value represents the average energy consumption needed to drive 1 kilometer, measured in kilowatt-hours.

        Returns:
            float: Energy consumption per kilometer (kWh/km).
        """
        return self._consumptionPerKm