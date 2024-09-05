from typing import Optional
from datetime import datetime
from EnergyPrice.wholesaleMarket import WholesaleMarket
from EnergyPrice.EnergyPlans.baseEnergyPlan import BaseEnergyPlan
from typing import Tuple
import calendar

#https://www.somenergia.coop/ca/tarifes-delectricitat-que-oferim/tarifa-indexada/#tarifa30TD
class SomEnergiaIndexadaIndustria(BaseEnergyPlan):
    def __init__(self,contractedPowerPeriods:Tuple[float,float,float,float,float,float]=(50,50,50,50,50,50)) -> None: #sempre ha de: potencia periode n-1<=potencia periode n
        super().__init__('Som Energia Tarifa Indexada Per Industries i Empreses (3.0TD)')
        self.iva=21#en tant per cent
        self.contractedPowerPeriods=contractedPowerPeriods #kw
        self.impostElectric= 5.11 #en tant per cent
        self.boSocial=0.0384546136986301 #euros/dia
        self.lloguerComptador=0.81 #euros/mes


    def selling_price(self,instant:datetime)->float: #returns €/kwh
        return WholesaleMarket.get_instance().price_at_instant(instant)

    def buying_price(self,instant:datetime)->float: #returns €/kwh
        # Obté el preu horari del mercat (PHM) per a l'hora actual
        phm = WholesaleMarket.get_instance().price_at_instant(instant)
        
        #Utilitzo valors fixes, a la realitat varien cada any o més, pero varien molt poc
        Pc = 0.00106  # Pagaments per capacitat
        Sc = 0.0003  # Sobrecostos
        Dsv = 0.0002  # Cost de desviaments
        GdO = 0.001374  # Cost de certificats de Garantia d'Origen Renovable (fix)
        POsOm = 0.0005  # Cost de l'operador del sistema
        Perd = 0.03  # Coeficients de pèrdues
        FE = 0.0001  # Fons d'Eficiència Energètica
        F = 0.016  # Franja de la cooperativa 0.016 per 3.0TD
        PTD = 0.05  # Cost regulat del peatge de transport i distribució
        CA = 0.015  # Cost regulat dels càrrecs del sistema elèctric
        
        # Calcular PH segons la fórmula 
        PH = 1.015 * (
            (phm + Pc + Sc + Dsv + GdO + POsOm) * (1 + Perd) + FE + F
        ) + PTD + CA
        
        preuDespresImpostos=PH + PH*(self.impostElectric/100)
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