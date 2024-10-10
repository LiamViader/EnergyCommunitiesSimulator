from typing import Optional
from datetime import datetime
from EnergyPrice.wholesaleMarket import WholesaleMarket
from EnergyPrice.EnergyPlans.baseEnergyPlan import BaseEnergyPlan
from typing import Tuple
import calendar

#https://www.somenergia.coop/ca/tarifes-delectricitat-que-oferim/tarifa-indexada/#tarifa30TD
class SomEnergiaIndexadaIndustria(BaseEnergyPlan):
    """
    Represents the 'Som Energia Tarifa Indexada Per Industries i Empreses (3.0TD)' energy plan.
    https://www.somenergia.coop/ca/tarifes-delectricitat-que-oferim/tarifa-indexada/#tarifa30TD

    This energy plan is designed for industrial and business clients, with energy prices indexed 
    to the wholesale market. It considers multiple contracted power periods and calculates both 
    the selling and buying prices of energy for a given time. It also calculates the flat monthly 
    power cost for the contracted power.

    Attributes:
        _iva (float): The VAT percentage (default 21%).

        _contractedPowerPeriods (Tuple[float, float, float, float, float, float]): The contracted 
        power in kW for six different periods (each period must have an equal or increasing value 
        compared to the previous one).

        _impostElectric (float): The electricity tax percentage (default 5.11%).

        _boSocial (float): A fixed cost per day for social services in energy billing (default 0.038 €/day).

        _lloguerComptador (float): The monthly cost of renting the energy meter (default 0.81 €/month).

    Methods:
        selling_price(instant: datetime) -> float:
            Returns the wholesale market price at the given instant.

        buying_price(instant: datetime) -> float:
            Returns the indexed energy price at the given time, adjusted for wholesale market price, taxes, 
            losses, and other fixed components.

        flat_price_month(instant: Optional[datetime]) -> float:
            Returns the flat monthly price considering the contracted power, taxes, and other fixed costs.
    """
    def __init__(self,contractedPowerPeriods:Tuple[float,float,float,float,float,float]=(50,50,50,50,50,50)) -> None:
        """
        Initializes the SomEnergiaIndexadaIndustria energy plan with default or provided contracted power periods.

        Args:
            contractedPowerPeriods (Tuple[float, float, float, float, float, float]): The contracted power 
            for six different periods, each period should have equal or greater power than the previous one.
        """
        super().__init__('Som Energia Tarifa Indexada Per Industries i Empreses (3.0TD)')
        self._iva=21
        self._contractedPowerPeriods=contractedPowerPeriods 
        self._impostElectric= 5.11
        self._boSocial=0.0384546136986301
        self._lloguerComptador=0.81 


    def selling_price(self,instant:datetime)->float: 
        """
        Returns the selling price of energy at the given time, based on the wholesale market price.

        Args:
            instant (datetime): The specific time for which the selling price is needed.

        Returns:
            float: The selling price in €/kWh, based on the wholesale market price.
        """
        return WholesaleMarket.get_instance().price_at_instant(instant)

    def buying_price(self,instant:datetime)->float:
        """
        Calculates the buying price of energy based on the wholesale market price and several fixed components 
        related to system costs, losses, and regulatory charges. The price is adjusted for taxes and iva.

        Args:
            instant (datetime): The specific time for which the buying price is calculated.

        Returns:
            float: The buying price in €/kWh after applying taxes, losses, and fixed charges.
        """
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
        
        preuDespresImpostos=PH + PH*(self._impostElectric/100)
        preuDespresIva=preuDespresImpostos+preuDespresImpostos*(self._iva/100)
        return preuDespresIva

    def flat_price_month(self,instant:Optional[datetime])->float:
        """
        Calculates the flat monthly price for the contracted power, considering the power contracted 
        for each of the six periods. It also includes taxes, social bonus, and meter rental cost.

        Args:
            instant (Optional[datetime]): The specific time at which the flat price is calculated. 
                If not provided, a default of 30 days is assumed for the month.

        Returns:
            float: The flat price in euros for the month, including taxes and VAT.
        """
        if instant is not None:
            _, totalDays = calendar.monthrange(instant.year, instant.month)
        else:
            totalDays = 30  # Suposant 30 dies si no es proporciona una data
        
        # Cost de la potència mensual
        annualPowerCost = self._contractedPowerPeriods(0)*15.713047+self._contractedPowerPeriods(1)*9.547036+self._contractedPowerPeriods(2)*4.658211+self._contractedPowerPeriods(3)*4.142560+self._contractedPowerPeriods(4)*2.285209+self._contractedPowerPeriods(5)*1.553638
        monthlyPowerCost = annualPowerCost / 12
        
        # Cost total mensual abans d'impost elèctric i IVA
        baseMonthlyCost = monthlyPowerCost + (self._boSocial * totalDays) + self._lloguerComptador
        
        # Càlcul de l'impost elèctric
        electricTaxAmount = baseMonthlyCost * (self._impostElectric / 100)
        
        # Cost total mensual abans d'IVA
        costBeforeIVA = baseMonthlyCost + electricTaxAmount
        
        # Càlcul de l'IVA
        ivaAmount = costBeforeIVA * (self._iva / 100)
        
        # Cost total mensual amb IVA
        totalMonthlyCost = costBeforeIVA + ivaAmount
        
        return totalMonthlyCost