class Battery:
    def __init__(self,
                capacity: float,#kwh
                chargeRate: float,#kw
                chargingEfficiency: float,
                dischargingEfficiency: float,
                startChargeLevel:float=0):
        self.capacity = capacity
        self.chargeRate = chargeRate
        self.chargingEfficiency = chargingEfficiency
        self.dischargingEfficiency = dischargingEfficiency
        self.chargeLevel=startChargeLevel
    
    def charge(self):
