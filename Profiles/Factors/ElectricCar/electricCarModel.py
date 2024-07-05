
class ElectricCarModel():
    def __init__(self, name: str, chargePower: float, consumptionPerKm:float, batteryCapacity: float, chargeEfficiency: float):
        self.name = name
        self.consumptionPerKm = consumptionPerKm #consum mig per km del cotxe en kwh
        self.chargePower = chargePower  #Potencia de carrega en kW
        self.batteryCapacity = batteryCapacity  #Capacitat de la batería en kWh
        self.chargeEfficiency = chargeEfficiency  #Eficiencia de la carrega

    def get_charge_power(self):
        return self.chargePower

    def get_battery_capacity(self):
        return self.batteryCapacity

    def get_charge_efficiency(self):
        return self.chargeEfficiency

    def get_name(self):
        return self.name
    
    def get_consumption_per_km(self): #en kwh
        return self.consumptionPerKm