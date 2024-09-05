from typing import Optional
from datetime import datetime
from EnergyPrice.wholesaleMarket import WholesaleMarket
from EnergyPrice.EnergyPlans.baseEnergyPlan import BaseEnergyPlan
import calendar
from typing import Tuple

#https://www.somenergia.coop/ca/tarifes-delectricitat-que-oferim/tarifa-periodes/#tarifa30TD
class SomEnergiaPeriodesIndustria(BaseEnergyPlan):
    def __init__(self,contractedPowerPeriods:Tuple[float,float,float,float,float,float]=(50,50,50,50,50,50)) -> None:
        super().__init__('Som Energia Tarifa Periodes Per Industria (3.0TD periodes)')
        self.iva=21#en tant per cent
        self.contractedPowerPeriods=contractedPowerPeriods #kw
        self.impostElectric= 5.11 #en tant per cent
        self.boSocial=0.0384546136986301 #euros/dia
        self.lloguerComptador=0.81 #euros/mes
        self.potenciaPuntaPla=27.474 #euros/kW any
        self.potenciaVall=3.059 #euros/kW any
        self.periodesEnergia=(0.176,0.150,0.134,0.122,0.105,0.108) #en €/kwh


    def selling_price(self,instant:datetime)->float: #returns €/kwh
        return 0.060


    def _january_price_at(self,instant:datetime)->float:
        if 0 <= instant.hour < 8:
            return self.periodesEnergia(5)
        if 8 <= instant.hour < 9:
            return self.periodesEnergia(1)
        if 9 <= instant.hour < 14:
            return self.periodesEnergia(0)
        if 14 <= instant.hour < 18:
            return self.periodesEnergia(1)
        if 18 <= instant.hour < 22:
            return self.periodesEnergia(0)
        return self.periodesEnergia(1)
    
    def _february_price_at(self,instant:datetime)->float:
        return self._january_price_at(instant)
    
    def _march_price_at(self,instant:datetime)->float:
        if 0 <= instant.hour < 8:
            return self.periodesEnergia(5)
        if 8 <= instant.hour < 9:
            return self.periodesEnergia(2)
        if 9 <= instant.hour < 14:
            return self.periodesEnergia(1)
        if 14 <= instant.hour < 18:
            return self.periodesEnergia(2)
        if 18 <= instant.hour < 22:
            return self.periodesEnergia(1)
        return self.periodesEnergia(2)
    
    def _april_price_at(self,instant:datetime)->float:
        if 0 <= instant.hour < 8:
            return self.periodesEnergia(5)
        if 8 <= instant.hour < 9:
            return self.periodesEnergia(4)
        if 9 <= instant.hour < 14:
            return self.periodesEnergia(3)
        if 14 <= instant.hour < 18:
            return self.periodesEnergia(4)
        if 18 <= instant.hour < 22:
            return self.periodesEnergia(3)
        return self.periodesEnergia(4)

    def _may_price_at(self,instant:datetime)->float:
        return self._april_price_at(instant)
    
    def _june_price_at(self,instant:datetime)->float:
        if 0 <= instant.hour < 8:
            return self.periodesEnergia(5)
        if 8 <= instant.hour < 9:
            return self.periodesEnergia(3)
        if 9 <= instant.hour < 14:
            return self.periodesEnergia(2)
        if 14 <= instant.hour < 18:
            return self.periodesEnergia(3)
        if 18 <= instant.hour < 22:
            return self.periodesEnergia(2)
        return self.periodesEnergia(3)

    def _july_price_at(self,instant:datetime)->float:
        return self._january_price_at(instant)
    
    def _august_price_at(self,instant:datetime)->float:
        return self._june_price_at(instant)

    def _september_price_at(self,instant:datetime)->float:
        return self._june_price_at(instant)
    
    def _october_price_at(self,instant:datetime)->float:
        return self._april_price_at(instant)
        
    def _november_price_at(self,instant:datetime)->float:
        return self._march_price_at(instant)

    def _desember_price_at(self,instant:datetime)->float:
        return self._january_price_at(instant)


    def buying_price(self,instant:datetime)->float: #returns €/kwh
        preuBase=self.periodesEnergia(5)
        if instant.weekday() in (5,6):#dissabte o diumenge
            preuBase=self.periodesEnergia(5)
        else:
            if  instant.month==1:
                preuBase=self._january_price_at(instant)
            elif  instant.month==2:
                preuBase=self._february_price_at(instant)
            elif  instant.month==3:
                preuBase=self._march_price_at(instant)
            elif  instant.month==4:
                preuBase=self._april_price_at(instant)
            elif  instant.month==5:
                preuBase=self._may_price_at(instant)
            elif  instant.month==6:
                preuBase=self._june_price_at(instant)
            elif  instant.month==7:
                preuBase=self._july_price_at(instant)
            elif  instant.month==8:
                preuBase=self._august_price_at(instant)
            elif  instant.month==9:
                preuBase=self._september_price_at(instant)
            elif  instant.month==10:
                preuBase=self._october_price_at(instant)
            elif  instant.month==11:
                preuBase=self._november_price_at(instant)
            elif  instant.month==12:
                preuBase=self._desember_price_at(instant)

        
        
        preuDespresImpostos=preuBase + preuBase*(self.impostElectric/100)
        preuDespresIva=preuDespresImpostos+preuDespresImpostos*(self.iva/100)
        return preuDespresIva

    def flat_price_month(self,instant:Optional[datetime])->float: #returns €
        if instant is not None:
            _, totalDays = calendar.monthrange(instant.year, instant.month)
        else:
            totalDays = 30  # Suposant 30 dies si no es proporciona una data
        
        # Cost de la potència mensual
        annualPowerCost = self.contractedPowerPeriods(0)*15.713047+self.contractedPowerPeriods(1)*9.547036+self.contractedPowerPeriods(2)*4.658211+self.contractedPowerPeriods(3)*4.142560+self.contractedPowerPeriods(4)*2.285209+self.contractedPowerPeriods(5)*1.553638
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