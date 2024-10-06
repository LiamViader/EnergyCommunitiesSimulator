
class ElectricCarModel():
    def __init__(self, name: str, chargePower: float, consumptionPerKm:float, batteryCapacity: float, chargeEfficiency: float):
        self._name = name
        self._consumptionPerKm = consumptionPerKm #consum mig per km del cotxe en kwh
        self._chargePower = chargePower  #Potencia de carrega en kW
        self._batteryCapacity = batteryCapacity  #Capacitat de la batería en kWh
        self._chargeEfficiency = chargeEfficiency  #Eficiencia de la carrega

    def get_charge_power(self):
        return self._chargePower

    def get_battery_capacity(self):
        return self._batteryCapacity

    def get_charge_efficiency(self):
        return self._chargeEfficiency

    def get_name(self):
        return self._name
    
    def get_consumption_per_km(self): #en kwh
        return self._consumptionPerKm