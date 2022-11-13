import json
import pandas as pd
from DataSource.DataFrameContainer import DataFrameContainer
from GlobalParameters.ClassificationData import ClassificationData


class AnalyticsDataSource:
    def provide_data(self):
        """Gets all data and returns it in DataFrameContainer

        :return: DataFrameContainer with dataframes for: sales, production, costs, lifestock, products, stores,
        products_yield
        """

        container = DataFrameContainer(
            sales=self.__provide_sales_dataframe(),
            production=self.__provide_production_dataframe(),
            costs=self.__provide_costs_dataframe(),
            lifestock=self.__provide_lifestock_dataframe(),
            products=ClassificationData.products_labels,
            stores=ClassificationData.stores_labels,
            products_yield=self.__provide_yelds()
        )
        return container

    def __provide_sales_dataframe(self):
        """Gets sale data from file and returns pandas dataframe

        :return: dataframe with firm sales data
        """

        sales_df = pd.read_csv('/Users/tomaszkrauzy/Desktop/DataForTwistAnalytics/10.CSV', encoding='latin1', sep=';')
        sales_df[['ILOSC', 'WARTOSC', 'SR_CENA']] = sales_df[['ILOSC', 'WARTOSC', 'SR_CENA']].apply(
            lambda x: x.str.replace(',', '.'))
        sales_df[['ILOSC', 'WARTOSC', 'SR_CENA']] = sales_df[['ILOSC', 'WARTOSC', 'SR_CENA']].astype(float)

        # Maps products names
        products_names = ClassificationData.products_labels
        sales_df['TOWAR'] = sales_df['INDEX_TOW'].map(products_names)

        return sales_df

    def __provide_costs_dataframe(self):
        """Gets costs data from file and returns pandas dataframe

        :return: dataframe with firm costs data
        """

        costs_df = pd.read_csv('/Users/tomaszkrauzy/Desktop/DataForTwistAnalytics/costs_5.CSV', encoding='latin1',
                               sep=';')
        costs_df.columns.values[0] = 'KONTO'
        costs_df.columns.values[1] = "KATEGORIA"
        costs_df.columns.values[
            4] = "WINIEN_MSC"  # co jeśli wezme za okres 2msc, czy ta kolumna będzie przestawiała te 2 msc?
        costs_df.columns.values[6] = "WINIEN_NARASTAJĄCO"
        costs_df[['WINIEN_MSC', 'WINIEN_NARASTAJĄCO']] = costs_df[['WINIEN_MSC', 'WINIEN_NARASTAJĄCO']].apply(
            lambda x: x.str.replace(' ', ''))

        costs_df[['WINIEN_MSC']] = costs_df[['WINIEN_MSC']].astype(float)
        costs_df = costs_df.iloc[:, [0, 1, 4, 6]]
        zmiana = {'£': 'ł', '¯': 'ż'}
        costs_df = costs_df.replace(zmiana, regex=True)
        return costs_df

    def __provide_lifestock_dataframe(self):
        """Gets lifestock purchuse data and returns pandas dataframe

        :return: dataframe with firm costs data
        """

        lifestock_df = pd.read_csv('/Users/tomaszkrauzy/Desktop/DataForTwistAnalytics/żywiec1.CSV', encoding='latin1',
                                   sep=';')
        lifestock_df[['WARTOSC']] = lifestock_df[['WARTOSC']].apply(
            lambda x: x.str.replace(',', '.'))
        lifestock_df[['ILOSC', 'WARTOSC']] = lifestock_df[['ILOSC', 'WARTOSC']].astype(float)
        return lifestock_df

    def __provide_production_dataframe(self):
        """Gets production data and returns pandas dataframe

        :return: dataframe with firm production amounts
        """

        sales_df = pd.read_csv('/Users/tomaszkrauzy/Desktop/DataForTwistAnalytics/10.CSV', encoding='latin1', sep=';')
        return sales_df

    def __provide_yelds(self):
        with open('/Users/tomaszkrauzy/Desktop/DataForTwistAnalytics/uzyski.txt') as f:
            products_yield = {int(k): v for k, v in json.load(f).items()}

        products_names = ClassificationData.products_labels
        products_yield_dataframe = pd.DataFrame(products_yield.values(), index=products_yield.keys(), columns=['Yield'])
        products_yield_dataframe['TOWAR'] = products_yield_dataframe.index.map(products_names)
        return products_yield_dataframe
