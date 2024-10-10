from typing import Optional
from datetime import datetime
from EnergyPrice.wholesaleMarket import WholesaleMarket
from EnergyPrice.EnergyPlans.baseEnergyPlan import BaseEnergyPlan
import calendar

#https://www.somenergia.coop/ca/tarifes-delectricitat-que-oferim/tarifa-periodes/#tarifa20TD
class SomEnergiaPeriodesDomestic(BaseEnergyPlan):
    """
    Represents the 'Som Energia Tarifa Periodes Per Domestic (2.0TD periodes)' energy plan.
    https://www.somenergia.coop/ca/tarifes-delectricitat-que-oferim/tarifa-periodes/#tarifa20TD

    This energy plan is designed for domestic clients, considering contracted power and time-of-day
    energy rates divided into valley, flat, and peak periods. The class calculates both the selling 
    and buying prices of energy for a given time, as well as the flat price charged per month.

    Attributes:
        _iva (float): The VAT percentage (either 10% or 21%).

        _potenciaContractada (float): The contracted power in kW (capped at 15 kW).

        _impostElectric (float): The electricity tax in percentage.

        _boSocial (float): A fixed cost per day for social services in energy billing.

        _lloguerComptador (float): The monthly cost of renting the energy meter.

        _potenciaPuntaPla (float): The annual cost per kW during peak periods.

        _potenciaVall (float): The annual cost per kW during valley periods.

        _energiaPunta (float): The energy cost per kWh during peak hours.

        _energiaPla (float): The energy cost per kWh during flat hours.
        
        _energiaVall (float): The energy cost per kWh during valley hours.

    Methods:
        selling_price(instant: datetime) -> float:
            Returns the fixed selling price of energy (€/kWh) at the given time.

        buying_price(instant: datetime) -> float:
            Returns the buying price of energy (€/kWh) at the given time, adjusted for taxes and VAT.

        flat_price_month(instant: Optional[datetime]) -> float:
            Returns the flat monthly cost for the energy plan, considering the contracted power, 
            taxes, and other fixed costs.
    """
    def __init__(self,contractedPower:float=12,iva:float=21) -> None: 
        """
        Initializes the SomEnergiaPeriodesDomestic energy plan with default or provided contracted power and VAT rate.
        
        Args:
            contractedPower (float): The contracted power in kW (default is 12 kW, capped at 15 kW).
            iva (float): The VAT percentage applied to prices (default is 21%, can be 10%).
        """
        super().__init__('Som Energia Tarifa Periodes Per Domestic (2.0TD periodes)')
        self._iva=iva
        self._potenciaContractada=min(contractedPower,15)
        self._impostElectric= 5.11 
        self._boSocial=0.0384546136986301 
        self._lloguerComptador=0.81 
        self._potenciaPuntaPla=27.474 
        self._potenciaVall=3.059 
        self._energiaPunta=0.212 
        self._energiaPla=0.154 
        self._energiaVall=0.118 


    def selling_price(self,instant:datetime)->float:
        """
        Returns the fixed selling price of energy for this energy plan.

        Args:
            instant (datetime): The specific time for which the selling price is needed.

        Returns:
            float: The selling price in €/kWh (fixed at 0.060 €/kWh).
        """
        return 0.060

    def buying_price(self,instant:datetime)->float:
        """
        Calculates the buying price of energy based on the time of day and day of the week.
        The price varies according to whether it's a weekday or weekend, and the time of day 
        (peak, flat, or valley hours). The price is adjusted with taxes and VAT.

        Args:
            instant (datetime): The time for which the buying price is calculated.

        Returns:
            float: The buying price in €/kWh after applying taxes and VAT.
        """
        preuBase=self._energiaVall
        if instant.weekday() in (5,6):#dissabte o diumenge
            preuBase=self._energiaVall
        else:
            if  0 <= instant.hour < 8:
                preuBase=self._energiaVall
            elif 8 <= instant.hour < 10:
                preuBase=self._energiaPla
            elif 10 <= instant.hour < 14:
                preuBase=self._energiaPunta
            elif 14 <= instant.hour < 18:
                preuBase=self._energiaPla
            elif 18 <= instant.hour < 22:
                preuBase=self._energiaPunta
            elif 22 <= instant.hour < 24:
                preuBase=self._energiaPla

        
        
        preuDespresImpostos=preuBase + preuBase*(self._impostElectric/100)
        preuDespresIva=preuDespresImpostos+preuDespresImpostos*(self._iva/100)
        return preuDespresIva

    def flat_price_month(self,instant:Optional[datetime])->float: 
        """
        Calculates the flat monthly price for the contracted power, taxes, and additional fixed costs.

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