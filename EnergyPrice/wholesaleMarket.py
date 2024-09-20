
from datetime import datetime, date
import pandas as pd

import warnings


#python -m pip install git+https://github.com/acruzgarcia/OMIEData

from OMIEData.DataImport.omie_marginalprice_importer import OMIEMarginalPriceFileImporter
from OMIEData.Enums.all_enums import DataTypeInMarginalPriceFile

from typing import Optional
import numpy as np

from utils.enums import MarketCountry

warnings.simplefilter(action='ignore', category=FutureWarning)

#SINGLETON PER NO COMPLICARME, SI ES NECESITA TENIR MES D'UN MERCAT, FER QUE SIGUI UN ATRIBUT DE LA COMUNITAT I AL CALCULAR PREUS ES PASI ALS ENERGYPLANS I TAL
#price units are euro/MWh
class WholesaleMarket:
    _instance = None
    _maxDate = date(2024, 8, 30)
    
    def __new__(cls, country: MarketCountry = MarketCountry.Spain, start: Optional[date] = None, end: Optional[date] = None) -> 'WholesaleMarket':
        if cls._instance is None:
            cls._instance = super(WholesaleMarket, cls).__new__(cls)
            cls._instance._initialize(country, start, end)
        else:
            if cls._instance.country != country:
                cls._instance._initialize(country, start, end)
        return cls._instance

    def _initialize(self, country: MarketCountry, start: Optional[date], end: Optional[date]) -> None:
        self.country = country
        if self.country == MarketCountry.Spain:
            self.str_price_country = str(DataTypeInMarginalPriceFile.PRICE_SPAIN)
        elif self.country == MarketCountry.Portugal:
            self.str_price_country = str(DataTypeInMarginalPriceFile.PRICE_PORTUGAL)

        if start is None or end is None or start > self._maxDate:
            self.prices = None
        else:
            if end > self._maxDate:
                end = self._maxDate
            self.prices = self._fetch_prices(start, end)

    
    def _fetch_prices(self,start:date,end:date)->pd.DataFrame:
        prices=OMIEMarginalPriceFileImporter(date_ini=start, date_end=end).read_to_dataframe(verbose=True)
        prices.sort_values(by='DATE', axis=0, inplace=True)
        prices = prices[prices.CONCEPT == self.str_price_country]
        prices.fillna(0, inplace=True)#aseguro que no hi hagi nan
        return prices

    
    def _get_example_prices(self)->np.ndarray:
        return np.array([82.19, 63.9, 50.0, 42.5, 
                         39.45, 38.32, 42.5, 54.67, 
                         63.78, 55.0, 33.33, 18.16, 
                         15.49, 15.0, 10.35, 4.16, 
                         4.16, 4.16, 4.16, 17.99, 
                         36.55, 49.01, 37.38, 33.65
                        ])

    def _check_date(self,dateToCheck:date)->date:
        if dateToCheck>self._maxDate:
            warnings.warn("that date exceeds the max date of market historic results, using prices from years before")
            day=dateToCheck.day
            month=dateToCheck.month
            year=self._maxDate.year-1
            if dateToCheck.month==2 and dateToCheck.day==29:
                day=28
            dateToCheck=date(year,month,day)
        return dateToCheck

    def prices_at_date(self,dateToGet:date)->np.ndarray:
        dateToGet=self._check_date(dateToGet)
        if self.prices is None:
            self.prices=self._fetch_prices(dateToGet,dateToGet)
        else:
            pricesdf=self.prices[self.prices['DATE'] == dateToGet]
            if pricesdf.empty:
                self.prices=pd.concat([self.prices, self._fetch_prices(dateToGet,dateToGet)], ignore_index=True)
        pricesdf=self.prices[self.prices['DATE'] == dateToGet]
        if pricesdf.empty: #per si per alguna rao no existís aquell dia
                warnings.warn("Not found prices for that specific day, using example prices")
                result=self._get_example_prices()
        else:
            columns = ['H' + str(i) for i in range(1, 25)]
            missing_columns = [col for col in columns if col not in pricesdf.columns]
            if missing_columns:
                warnings.warn(f"Missing the columns: {missing_columns}, using example prices")
                result=self._get_example_prices()
            else:
                result=pricesdf.iloc[0][columns].values
        return result/1000

    def price_at_instant(self,instant:datetime)->float: #retorna en euros/kwh
        instantDate=self._check_date(instant.date())
        instant = instant.replace(year=instantDate.year, month=instantDate.month, day=instantDate.day)
        if self.prices is None:
            self.prices=self._fetch_prices(instantDate,instantDate)
        else:
            pricesdf=self.prices[self.prices['DATE'] == instantDate]
            if pricesdf.empty:
                self.prices=pd.concat([self.prices, self._fetch_prices(instantDate,instantDate)], ignore_index=True)
        pricesdf=self.prices[self.prices['DATE'] == instantDate]

        if pricesdf.empty: #per si per alguna rao no existís aquell dia
            warnings.warn("Not found prices for that specific day, using example prices")
            result=self._get_example_prices()
        else:
            columns = ['H' + str(i) for i in range(1, 25)]
            missing_columns = [col for col in columns if col not in pricesdf.columns]
            if missing_columns:
                warnings.warn(f"Missing the columns: {missing_columns}, using example prices")
                result=self._get_example_prices()
            else:
                result=pricesdf.iloc[0][columns].values
        return result[instant.hour]/1000
    
    @classmethod
    def get_instance(cls) -> 'WholesaleMarket':
        """Mètode d'accés a la instància singleton"""
        if cls._instance is None:
            raise ValueError("The singleton instance has not been created yet.")
        return cls._instance
        
