from typing import Optional
from datetime import datetime
from EnergyPrice.wholesaleMarket import WholesaleMarket
from EnergyPrice.EnergyPlans.baseEnergyPlan import BaseEnergyPlan
import calendar

#https://www.somenergia.coop/ca/tarifes-delectricitat-que-oferim/tarifa-periodes/#tarifa20TD
class SomEnergiaPeriodesDomestic(BaseEnergyPlan):
    def __init__(self,contractedPower:float=12,iva:float=21) -> None: #iva pot ser 10 o 21
        super().__init__('Som Energia Tarifa Periodes Per Domestic (2.0TD periodes)')
        self.iva=iva#en tant per cent
        self.potenciaContractada=min(contractedPower,15) #kw
        self.impostElectric= 5.11 #en tant per cent
        self.boSocial=0.0384546136986301 #euros/dia
        self.lloguerComptador=0.81 #euros/mes
        self.potenciaPuntaPla=27.474 #euros/kW any
        self.potenciaVall=3.059 #euros/kW any
        self.energiaPunta=0.212 #€/kwh
        self.energiaPla=0.154 #€/kwh
        self.energiaVall=0.118 #€/kwh


    def selling_price(self,instant:datetime)->float: #returns €/kwh
        return 0.060

    def buying_price(self,instant:datetime)->float: #returns €/kwh
        preuBase=self.energiaVall
        if instant.weekday() in (5,6):#dissabte o diumenge
            preuBase=self.energiaVall
        else:
            if  0 <= instant.hour < 8:
                preuBase=self.energiaVall
            elif 8 <= instant.hour < 10:
                preuBase=self.energiaPla
            elif 10 <= instant.hour < 14:
                preuBase=self.energiaPunta
            elif 14 <= instant.hour < 18:
                preuBase=self.energiaPla
            elif 18 <= instant.hour < 22:
                preuBase=self.energiaPunta
            elif 22 <= instant.hour < 24:
                preuBase=self.energiaPla

        
        
        preuDespresImpostos=preuBase + preuBase*(self.impostElectric/100)
        preuDespresIva=preuDespresImpostos+preuDespresImpostos*(self.iva/100)
        return preuDespresIva

    def flat_price_month(self,instant:Optional[datetime])->float: #returns €
        if instant is not None:
            _, totalDays = calendar.monthrange(instant.year, instant.month)
        else:
            totalDays = 30  # Suposant 30 dies si no es proporciona una data
        
        # Cost de la potència mensual
        annualPowerCost = (self.potenciaPuntaPla + self.potenciaVall) * self.potenciaContractada
        monthlyPowerCost = annualPowerCost / 12
        
        # Cost total mensual abans d'impost elèctric i IVA
        baseMonthlyCost = monthlyPowerCost + (self.boSocial * totalDays) + self.lloguerComptador
        
        # Càlcul de l'impost elèctric
        electricTaxAmount = baseMonthlyCost * (self.impostElectric / 100)
        
        # Cost total mensual abans d'IVA
        costBeforeIVA = baseMonthlyCost + electricTaxAmount
        
        # Càlcul de l'IVA
        ivaAmount = costBeforeIVA * (self.iva / 100)
        
        # Cost total mensual amb IVA
        totalMonthlyCost = costBeforeIVA + ivaAmount
        
        return totalMonthlyCost