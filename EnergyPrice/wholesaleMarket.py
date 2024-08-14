
from datetime import datetime, date
import pandas as pd

import warnings


from OMIEData.DataImport.omie_marginalprice_importer import OMIEMarginalPriceFileImporter
from OMIEData.Enums.all_enums import DataTypeInMarginalPriceFile

from typing import Optional
import numpy as np

from utils.enums import MarketCountry

warnings.simplefilter(action='ignore', category=FutureWarning)

#price units are euro/MWh
class WholesaleMarket:
    def __init__(self,country:MarketCountry=MarketCountry.Spain,start:Optional[date]=None,end:Optional[date]=None) -> None:

        self.maxDate=date(2024,7,31)

        self.country=country
        if self.country==MarketCountry.Spain:
            self.str_price_country = str(DataTypeInMarginalPriceFile.PRICE_SPAIN)
        elif self.country==MarketCountry.Portugal:
            self.str_price_country = str(DataTypeInMarginalPriceFile.PRICE_PORTUGAL)

    
        if start is None or end is None or start>self.maxDate:
            self.prices=None
        else:
            if end>self.maxDate:
                end=self.maxDate
            self.prices=self.__fetch_prices(start,end)
    
    def __fetch_prices(self,start:date,end:date)->pd.DataFrame:
        prices=OMIEMarginalPriceFileImporter(date_ini=start, date_end=end).read_to_dataframe(verbose=True)
        prices.sort_values(by='DATE', axis=0, inplace=True)
        prices = prices[prices.CONCEPT == self.str_price_country]
        return prices

    
    def __get_example_prices(self)->np.ndarray:
        return np.array([82.19, 63.9, 50.0, 42.5, 
                         39.45, 38.32, 42.5, 54.67, 
                         63.78, 55.0, 33.33, 18.16, 
                         15.49, 15.0, 10.35, 4.16, 
                         4.16, 4.16, 4.16, 17.99, 
                         36.55, 49.01, 37.38, 33.65
                        ])

    def __check_date(self,dateToCheck:date)->date:
        if dateToCheck>self.maxDate:
            warnings.warn("that date exceeds the max date of market historic results, using prices from years before")
            day=dateToCheck.day
            month=dateToCheck.month
            year=self.maxDate.year-1
            if dateToCheck.month==2 and dateToCheck.day==29:
                day=28
            dateToCheck=date(year,month,day)
        return dateToCheck

    def prices_at_date(self,dateToGet:date)->np.ndarray:
        dateToGet=self.__check_date(dateToGet)
        if self.prices is None:
            self.prices=self.__fetch_prices(dateToGet,dateToGet)
        else:
            pricesdf=self.prices[self.prices['DATE'] == dateToGet]
            if pricesdf.empty:
                self.prices=pd.concat([self.prices, self.__fetch_prices(dateToGet,dateToGet)], ignore_index=True)
        pricesdf=self.prices[self.prices['DATE'] == dateToGet]
        if pricesdf.empty: #per si per alguna rao no existís aquell dia
                warnings.warn("Not found prices for that specific day, using example prices")
                result=self.__get_example_prices()
        else:
            columns = ['H' + str(i) for i in range(1, 25)]
            missing_columns = [col for col in columns if col not in pricesdf.columns]
            if missing_columns:
                warnings.warn(f"Missing the columns: {missing_columns}, using example prices")
                result=self.__get_example_prices()
            else:
                result=pricesdf.iloc[0][columns].values
        return result

    def price_at_instant(self,instant:datetime)->float:
        instantDate=self.__check_date(instant.date())
        instant = instant.replace(year=instantDate.year, month=instantDate.month, day=instantDate.day)
        if self.prices is None:
            self.prices=self.__fetch_prices(instantDate,instantDate)
        else:
            pricesdf=self.prices[self.prices['DATE'] == instantDate]
            if pricesdf.empty:
                self.prices=pd.concat([self.prices, self.__fetch_prices(instantDate,instantDate)], ignore_index=True)
        pricesdf=self.prices[self.prices['DATE'] == instantDate]

        if pricesdf.empty: #per si per alguna rao no existís aquell dia
            warnings.warn("Not found prices for that specific day, using example prices")
            result=self.__get_example_prices()
        else:
            columns = ['H' + str(i) for i in range(1, 25)]
            missing_columns = [col for col in columns if col not in pricesdf.columns]
            if missing_columns:
                warnings.warn(f"Missing the columns: {missing_columns}, using example prices")
                result=self.__get_example_prices()
            else:
                result=pricesdf.iloc[0][columns].values
        return result[instant.hour]
        
