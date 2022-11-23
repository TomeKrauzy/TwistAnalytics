from UnitProductionCostsCalculator.UnitProductionCostsCalculator import UnitProductionCostsCalculator
from GlobalParameters.ProductionParameters import ProductionParameters
from GlobalParameters.ClassificationData import ClassificationData
from LifestockPurchusePriceSplit.LifesockPurchusePriceSplitter import LifestockPurchasePriceSplitter
import pandas as pd

class ShopProfitabilityReportGenerator:

    def __init__(self, sales_df, acquisition_cost_df):
        self.sales_df = sales_df
        self.upc_costs = UnitProductionCostsCalculator().provide_primary_products_UPC()
        self.shops_id = ClassificationData.stores_labels
        self.item_id = ClassificationData.products_labels
        self.acquisition_cost = acquisition_cost_df
        self.shop_rents = pd.read_excel('/Users/tomaszkrauzy/Desktop/DataForTwistAnalytics/GeneralData/shop_rents.xlsx')

    def generate(self):
        """Generates dataframes for shops

        :return: (df_groupby(shop), df_groupby(product))
        """
        df = self.__prepare_data()
        # more detailed summary
        df_summary = df.groupby(['NAZ_KONTR', 'TOWAR']).sum()[['ILOSC', 'WARTOSC', 'PROD_COST']]

        df_result = df.groupby(['NAZ_KONTR']).sum()[['ILOSC', 'WARTOSC', 'PROD_COST']]
        # adding rent column
        df_result = df_result.merge(self.shop_rents, on='NAZ_KONTR')
        df_result['WYNIK_SKLEPU'] = df_result['WARTOSC'] - df_result['RENT'] - df_result['PROD_COST']
        df_result = df_result.set_index('NAZ_KONTR')

        return (df_result, df_summary)

    def __prepare_data(self):
        sales_df = self.sales_df
        sales_df = sales_df[sales_df['KOD_KONTR'].isin(self.shops_id)]

        # filter for primary products
        shop_sales_df = sales_df[sales_df['INDEX_TOW'].isin(self.item_id.keys())]

        # maps products upc
        shop_sales_df['UPC'] = shop_sales_df['INDEX_TOW'].map(self.upc_costs)

        # maps stores names
        shop_sales_df['NAZ_KONTR'] = shop_sales_df['KOD_KONTR'].map(self.shops_id)

        # adds acquisition cost
        shop_sales_df['ACQ_COST'] = shop_sales_df['TOWAR'].map(self.acquisition_cost)

        # adds costs of products
        shop_sales_df['PROD_COST'] = (shop_sales_df['UPC'] + shop_sales_df['ACQ_COST']) \
                                     * shop_sales_df['ILOSC']

        return shop_sales_df






