import pandas as pd

class LifestockPurchusePriceSplitter():

    def __init__(self, production_resource_dataframe, avg_wholesales_prices, products_yield, avg_lifestock_price):

        self.production_resource_dataframe = production_resource_dataframe
        self.avg_wholesales_prices = avg_wholesales_prices
        self.products_yield = products_yield
        self.avg_lifestock_price = avg_lifestock_price


    def __split_lifestock_purchuse_price(self):

        """
        Distributes lifestock price among elements according to specific assumptions
        :return: DataFrame with acquisition cost for primary products
        """

        primary_products = [260, 7437, 63, 156, 61, 185, 183, 74]

        products_yield = self.products_yield
        products_yield = products_yield[products_yield.index.isin(primary_products)]
        products_yield = products_yield.set_index('TOWAR')

        # Here we calculate revenue from products yielded from 1kg lifestock
        df = products_yield.join(self.avg_wholesales_prices)
        df['zysk ze sprzedaży kg żywca[zł]'] = df['ŚR_CENA'] * df['Yield']

# Here we calculate 'weights' for each elements that we will use to split lifestock price accordingly
# Important: We can sell products in 2 options: carcass and elements. Each scenario has different total_revenue from selling original products from lifestock

    # Elements
        total_revenue_from_products_of_1kg_lifestock = df['zysk ze sprzedaży kg żywca[zł]'].iloc[1:].sum()
        revenue_from_products_of_1kg_lifestock = df['zysk ze sprzedaży kg żywca[zł]']

        df['% udział_w_zysku_ze_sprzedaży'] = revenue_from_products_of_1kg_lifestock / total_revenue_from_products_of_1kg_lifestock
        df['Wielkość ceny zakupu [% udział w zysku * cena zakupu]'] = df['% udział_w_zysku_ze_sprzedaży'] * self.avg_lifestock_price

    # Carcass scenario
        # We calculate carcass_acqusition_price = lifestock_price - liver_acqusition_price - heart_acqusition_price - gizard_acqusition_price_
        lifestock_price = self.avg_lifestock_price
        liver_acqusition_price = df.loc[df.index == 'Wątroba', 'zysk ze sprzedaży kg żywca[zł]'].item()
        heart_acqusition_price = df.loc[df.index == 'Serce', 'zysk ze sprzedaży kg żywca[zł]'].item()
        gizzard_acqusition_price = df.loc[df.index == 'Żołądek', 'zysk ze sprzedaży kg żywca[zł]'].item()
        df.loc[df.index == 'Tuszka', 'Wielkość ceny zakupu [% udział w zysku * cena zakupu]'] = lifestock_price - liver_acqusition_price - heart_acqusition_price - gizzard_acqusition_price

        # Here we calculate final zł/kg for every product
        df['koszt_pozyskania_towaru [zł/kg]'] = df['Wielkość ceny zakupu [% udział w zysku * cena zakupu]'] / df['Yield']

        return df


    def __quarter_purchuse_price_splitter(self):
        """
        Distributes quarter acquisition cost for further elements: noga, podudzie, nogaT..
        :return: DataFrame
        """

        quarter_purchase_price = self.__split_lifestock_purchuse_price().filter(items=['Ćwiartka'], axis=0).loc[:, 'Wielkość ceny zakupu [% udział w zysku * cena zakupu]'].iat[0]
        quarter_yield = self.products_yield.filter(items = [7437], axis=0)['Yield'].iat[0]

        # We split quarter_purchase price for leg and back with proportion 0.9 and 0.1
        noga_purchase_price = quarter_purchase_price * 0.9 / (quarter_yield * 0.71)
        grzbiet_purchuse_price = quarter_purchase_price * 0.1 / (quarter_yield * 0.2874)

        # Further purchase_price_split according to assumed weight: thigh-0.52, shank-0.48
        tigh_purchase_price = (quarter_purchase_price * 0.9 * 0.52) / (quarter_yield * 0.71 * 0.48)
        shank_purchase_price = quarter_purchase_price * 0.9 * 0.48 / (quarter_yield * 0.71 * 0.513)

        # purchase_price_split for deboned products, according to: material_cost / product_weigh.
        noga_t = quarter_purchase_price * 0.9 / (quarter_yield * 0.71 * 0.6825)
        udo_t = (quarter_purchase_price * 0.9 * 0.52) / (quarter_yield * 0.71 * 0.48 * 0.7357)

        #  creates dicts with results
        quarter_split = {'Noga': noga_purchase_price, 'Grzbiet': grzbiet_purchuse_price, 'Udziec': tigh_purchase_price,
                      'Podudzie': shank_purchase_price, 'Noga T.': noga_t, 'Udziec T.': udo_t}

        products = [60, 1714, 248, 240, 12013, 9859]
        products_yield = self.products_yield
        products_yield = products_yield[products_yield.index.isin(products)]
        products_yield = products_yield.reset_index().set_index('TOWAR')

        df = products_yield.join(self.avg_wholesales_prices)
        df['koszt_pozyskania_towaru [zł/kg]'] = df.index.map(quarter_split)

        return df

    def all_products_purchuse_price_splitted(self):
        """
        Combines 2 class functions and returns DataFrame with acquisiton cost for all products
        :return:
        """

        result_df = pd.concat([self.__quarter_purchuse_price_splitter()['koszt_pozyskania_towaru [zł/kg]'],
                               self.__split_lifestock_purchuse_price()['koszt_pozyskania_towaru [zł/kg]']])
        return result_df

