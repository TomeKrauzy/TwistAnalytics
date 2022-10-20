import pandas as pd


class LifestockPurchusePriceSplitter():

    def __init__(self, production_resource_dataframe, avg_sales_prices):

        self.production_resource_dataframe = production_resource_dataframe
        self.avg_sales_prices = avg_sales_prices


    def split_lifestock_purchuse_price(self):
        # Rozbijemy cene i zwracamy tablie z % wagami produktów
        # zrobić assert czy % z df sumują się do 100%
        pass


