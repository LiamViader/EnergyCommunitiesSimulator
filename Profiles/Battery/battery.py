
class Battery:
    def __init__(self,
                capacity: float,#kwh
                chargeRate: float,#kw
                dischargeRate: float,#kw
                chargingEfficiency: float,
                dischargingEfficiency: float,
                startChargeLevel:float=0):
        self.capacity = capacity
        self.chargeRate = chargeRate
        self.dischargeRate = dischargeRate
        self.chargingEfficiency = chargingEfficiency
        self.dischargingEfficiency = dischargingEfficiency
        self.chargeLevel=startChargeLevel
    
    def charge(self,energy:float,timeElapsed:float)->float:#parametres son l'energia a carregar en kwh i el temps durant el que es carrega en minuts. Retorna energia carregada 
        timeElapsedHours=timeElapsed/60
        averagePower=energy/timeElapsedHours
        rate=min(averagePower,self.chargeRate)
        energyToCharge=rate*timeElapsed*self.chargingEfficiency
        if energyToCharge+self.chargeLevel<self.capacity:
            energyUsed=energyToCharge/self.chargingEfficiency
            self.chargeLevel+=energyToCharge
        else:
            energyUsed=(self.capacity-self.chargeLevel)/self.chargingEfficiency
            self.chargeLevel=self.capacity

        return energyUsed
        
    def discharge(self,energy:float,timeElapsed:float)->float:#parametres son l'energia a descarregar en kwh i el temps durant el que es descarrega en minuts. Retorna energia descarregada 
        timeElapsedHours=timeElapsed/60
        realEnergy=energy/self.dischargingEfficiency
        averagePower=realEnergy/timeElapsedHours
        rate=min(averagePower,self.dischargeRate)
        energyToDischarge=rate*timeElapsed
        if self.chargeLevel-energyToDischarge>0:
            energyDischarged=energyToDischarge*self.dischargingEfficiency
            self.chargeLevel-=energyToDischarge
        else:
            energyDischarged=self.capacity*self.dischargingEfficiency
            self.chargeLevel=0
        return energyDischarged