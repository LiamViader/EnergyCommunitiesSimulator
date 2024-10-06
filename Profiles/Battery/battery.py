
class Battery:
    def __init__(self,
                capacity: float,#kwh
                chargeRate: float,#kw
                dischargeRate: float,#kw
                chargingEfficiency: float,
                dischargingEfficiency: float,
                startChargeLevel:float=0):
        self._capacity = capacity
        self._chargeRate = chargeRate
        self._dischargeRate = dischargeRate
        self._chargingEfficiency = chargingEfficiency
        self._dischargingEfficiency = dischargingEfficiency
        self._chargeLevel=startChargeLevel
    
    def charge(self,energy:float,timeElapsed:float)->float:#parametres son l'energia a carregar en kwh i el temps durant el que es carrega en minuts. Retorna energia carregada 
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
        
    def discharge(self,energy:float,timeElapsed:float)->float:#parametres son l'energia a descarregar en kwh i el temps durant el que es descarrega en minuts. Retorna energia produida 
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