import json
import pandas as pd
from DataSource.DataFrameContainer import DataFrameContainer

class AnalyticsDataSource:

    def provide(self):
        container = DataFrameContainer(
            sales= self.__provide_sales_dataframe(),
            production= self.__provide_production_dataframe(),
            costs= self.__provide_costs_dataframe(),
            production_resource= self.__provide_production_resource_dataframe(),
            products= self.__provide_products_name(),
            stores= self.__provide_stores()
        )
        return container


    def __provide_sales_dataframe(self):
        sales_df = pd.read_csv('/Users/tomaszkrauzy/Desktop/Pandas/TWIST/08.CSV', encoding='latin1', sep=';')
        sales_df[['ILOSC', 'WARTOSC', 'SR_CENA']] = sales_df[['ILOSC', 'WARTOSC', 'SR_CENA']].apply(
            lambda x: x.str.replace(',', '.'))
        sales_df[['ILOSC', 'WARTOSC', 'SR_CENA']] = sales_df[['ILOSC', 'WARTOSC', 'SR_CENA']].astype(float)

        products_names = self.__provide_products_name()
        sales_df['TOWAR'] = sales_df['INDEX_TOW'].map(products_names)

        return sales_df

    def __provide_costs_dataframe(self):
        sales_df = pd.read_csv('/Users/tomaszkrauzy/Desktop/Pandas/TWIST/08.CSV', encoding='latin1', sep=';')
        return sales_df

    def __provide_production_resource_dataframe(self):
        sales_df = pd.read_csv('/Users/tomaszkrauzy/Desktop/Pandas/TWIST/08.CSV', encoding='latin1', sep=';')
        return sales_df

    def __provide_production_dataframe(self):
        sales_df = pd.read_csv('/Users/tomaszkrauzy/Desktop/Pandas/TWIST/08.CSV', encoding='latin1', sep=';')
        return sales_df

    def __provide_products_name(self):
        with open('/Users/tomaszkrauzy/Desktop/Pandas/towary.txt') as f:
            products_names = {int(k): v for k, v in json.load(f).items()}

        return products_names

    def __provide_stores(self):
        with open('/Users/tomaszkrauzy/Desktop/Pandas/indexy_nasze_sklepy.txt') as f:
            stores = {int(k): v for k, v in json.load(f).items()}

        return stores

