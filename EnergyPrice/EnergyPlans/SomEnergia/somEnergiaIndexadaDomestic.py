from typing import Optional
from datetime import datetime
from EnergyPrice.wholesaleMarket import WholesaleMarket
from EnergyPrice.EnergyPlans.baseEnergyPlan import BaseEnergyPlan
import calendar

#https://www.somenergia.coop/ca/tarifes-delectricitat-que-oferim/tarifa-indexada/#tarifa20TD
class SomEnergiaIndexadaDomestic(BaseEnergyPlan):
    """
    Represents the 'Som Energia Tarifa Indexada Per Domestic (2.0TD)' energy plan for domestic consumers.
    https://www.somenergia.coop/ca/tarifes-delectricitat-que-oferim/tarifa-indexada/#tarifa20TD

    This energy plan indexes prices based on the wholesale market while considering contracted power, 
    various regulatory costs, and taxes. It also calculates a flat monthly price for domestic customers.

    Attributes:
        _iva (float): The VAT percentage (default is 21%, can be 10%).

        _potenciaContractada (float): The contracted power in kW (default is 12 kW, capped at 15 kW).

        _impostElectric (float): The electricity tax percentage (default is 5.11%).

        _boSocial (float): The daily social bonus cost (default is 0.038 €/day).

        _lloguerComptador (float): The monthly cost for renting the energy meter (default is 0.81 €/month).

        _potenciaPuntaPla (float): Power cost for peak and flat periods (default is 27.474 €/kW per year).
        
        _potenciaVall (float): Power cost for valley periods (default is 3.059 €/kW per year).

    Methods:
        selling_price(instant: datetime) -> float:
            Returns the wholesale market price at the given instant.

        buying_price(instant: datetime) -> float:
            Returns the indexed energy price at the given time, adjusted for the wholesale market price, taxes, 
            losses, and other fixed components.

        flat_price_month(instant: Optional[datetime]) -> float:
            Returns the flat monthly price considering contracted power, taxes, and other fixed costs.
    """
    def __init__(self,contractedPower:float=12,iva:float=21) -> None:
        """
        Initializes the SomEnergiaIndexadaDomestic energy plan with default or provided contracted power and VAT.

        Args:
            contractedPower (float): Contracted power in kW (default is 12 kW, maximum is 15 kW).
            iva (float): VAT percentage (default is 21%, can be set to 10%).
        """
        super().__init__('Som Energia Tarifa Indexada Per Domestic (2.0TD)')
        self._iva=iva
        self._potenciaContractada=min(contractedPower,15)
        self._impostElectric= 5.11
        self._boSocial=0.0384546136986301 
        self._lloguerComptador=0.81
        self._potenciaPuntaPla=27.474 
        self._potenciaVall=3.059 


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
        related to system costs, losses, and regulatory charges. The price is adjusted for taxes and VAT.

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
        F = 0.02  # Franja de la cooperativa 0.020 per 2.0TD
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
        for both peak/flat and valley periods. It also includes taxes, social bonus, and meter rental cost.

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
        annualPowerCost = (self._potenciaPuntaPla + self._potenciaVall) * self._potenciaContractada
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