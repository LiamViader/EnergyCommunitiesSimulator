
class Battery:
    """
    Represents a battery that can charge and discharge energy.

    This class manages the battery's state, including its capacity, charge rate,
    discharge rate, and efficiency. It allows for charging and discharging operations
    based on the specified energy and time parameters.

    Attributes:
        _capacity (float): The total energy capacity of the battery in kWh.

        _chargeRate (float): The maximum charging rate of the battery in kW.

        _dischargeRate (float): The maximum discharging rate of the battery in kW.

        _chargingEfficiency (float): The efficiency of the charging process (0-1).

        _dischargingEfficiency (float): The efficiency of the discharging process (0-1).
        
        _chargeLevel (float): The current charge level of the battery in kWh.

    Methods:
        charge(energy: float, timeElapsed: float) -> float:
            Charges the battery with the specified energy over the given time period.
        
        discharge(energy: float, timeElapsed: float) -> float:
            Discharges the battery with the specified energy over the given time period.
    """
    def __init__(self,
                capacity: float,
                chargeRate: float,
                dischargeRate: float,
                chargingEfficiency: float,
                dischargingEfficiency: float,
                startChargeLevel:float=0):
        """
        Initializes the Battery instance with specified parameters.

        Args:
            capacity (float): The total energy capacity of the battery in kWh.
            chargeRate (float): The maximum charging rate of the battery in kW.
            dischargeRate (float): The maximum discharging rate of the battery in kW.
            chargingEfficiency (float): Efficiency of the charging process (0-1).
            dischargingEfficiency (float): Efficiency of the discharging process (0-1).
            startChargeLevel (float): Initial charge level of the battery in kWh (default is 0).
        """
        self._capacity = capacity
        self._chargeRate = chargeRate
        self._dischargeRate = dischargeRate
        self._chargingEfficiency = chargingEfficiency
        self._dischargingEfficiency = dischargingEfficiency
        self._chargeLevel=startChargeLevel
    
    def charge(self,energy:float,timeElapsed:float)->float:
        """
        Charges the battery with the specified energy over the given time period.

        Args:
            energy (float): The amount of energy to charge the battery in kWh.
            timeElapsed (float): The time duration for charging in minutes.

        Returns:
            float: The actual amount of energy charged to the battery in kWh.
        """
        timeElapsedHours=timeElapsed/60
        averagePower=energy/timeElapsedHours
        rate=min(averagePower,self._chargeRate)
        energyToCharge=rate*timeElapsedHours*self._chargingEfficiency
        if energyToCharge+self._chargeLevel<self._capacity:
            energyUsed=energyToCharge/self._chargingEfficiency
            self._chargeLevel+=energyToCharge
        else:
            energyUsed=(self._capacity-self._chargeLevel)/self._chargingEfficiency
            self._chargeLevel=self._capacity

        return energyUsed
        
    def discharge(self,energy:float,timeElapsed:float)->float:
        """
        Discharges the battery with the specified energy over the given time period.

        Args:
            energy (float): The amount of energy to discharge from the battery in kWh.
            timeElapsed (float): The time duration for discharging in minutes.

        Returns:
            float: The actual amount of energy produced by the battery in kWh.
        """
        timeElapsedHours=timeElapsed/60
        realEnergy=energy/self._dischargingEfficiency
        averagePower=realEnergy/timeElapsedHours
        rate=min(averagePower,self._dischargeRate)
        energyToDischarge=rate*timeElapsedHours
        if self._chargeLevel-energyToDischarge>0:
            producedEnergy=energyToDischarge*self._dischargingEfficiency
            self._chargeLevel-=energyToDischarge
        else:
            producedEnergy=self._chargeLevel*self._dischargingEfficiency
            self._chargeLevel=0
        return producedEnergy