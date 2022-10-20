import pandas as pd


class LifestockPurchusePriceSplitter():

    def __init__(self, production_resource_dataframe, avg_sales_prices, products_yield, avg_lifestock_price):

        self.production_resource_dataframe = production_resource_dataframe
        self.avg_sales_prices = avg_sales_prices
        self.products_yield = products_yield
        self.avg_lifestock_price = avg_lifestock_price


    def split_lifestock_purchuse_price(self):

        primary_products = [260, 7437, 63, 156, 61, 185, 183, 74]

        products_yield = self.products_yield
        products_yield = products_yield[products_yield.index.isin(primary_products)]
        products_yield = products_yield.set_index('TOWAR')

        df = products_yield.join(self.avg_sales_prices)
        df['dochód_ze_sprzedaży_kg_żywca'] = df['ŚR_CENA'] * df['Yield']
        df['% udział_w_zysku_ze_sprzedaży'] = df['dochód_ze_sprzedaży_kg_żywca'] / df['dochód_ze_sprzedaży_kg_żywca'].iloc[1:].sum()
        df['Udział_ceny_zakupu'] = df['% udział_w_zysku_ze_sprzedaży'] * self.avg_lifestock_price

        return df





