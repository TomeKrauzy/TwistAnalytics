import pandas as pd
from GlobalParameters.ProductionParameters import ProductionParameters


class LifestockPurchasePriceSplitter():

    def __init__(self, production_resource_dataframe, avg_wholesales_prices, products_yield, avg_lifestock_price):
        self.production_resource_dataframe = production_resource_dataframe
        self.avg_wholesales_prices = avg_wholesales_prices
        self.products_yield = products_yield
        self.avg_lifestock_price = avg_lifestock_price

    def provide_acquisition_cost_all_products(self):
        """Combines 2 methods and returns DataFrame with acquisition cost for all products

        :return: DataFrame that contains acquisition cost for all products e.i Carcass, wing, deboned thigh ...
        """

        result_df = pd.concat([self.__split_quarter_acquisition_price()['koszt_pozyskania_towaru [zł/kg]'],
                               self.__provide_acquisition_cost_primary_products()['koszt_pozyskania_towaru [zł/kg]']])
        return result_df

    def __provide_acquisition_cost_primary_products(self):
        """Distributes lifestock price among elements according to specific methodology, for further understanding
        ask Tomasz Krauzy or deduce from code ;)

        :return: DataFrame with acquisition cost for primary products
        """

        primary_products = [260, 7437, 63, 156, 61, 185, 183, 74]

        products_yield = ProductionParameters.products_yields
        products_yield = products_yield[products_yield.index.isin(primary_products)]
        products_yield = products_yield.set_index('TOWAR')

        # Here we calculate revenue from products yielded from 1kg lifestock
        df = products_yield.join(self.avg_wholesales_prices)
        df['zysk ze sprzedaży kg żywca[zł]'] = df['ŚR_CENA'] * df['Yield']

        # Here we calculate 'weights' for each elements that we will use to split lifestock price accordingly
        # Important: We can sell products in 2 options: carcass and elements. Each scenario has different total_revenue
        # from selling original products from lifestock

        # Elements
        total_revenue_from_products_of_1kg_lifestock = df['zysk ze sprzedaży kg żywca[zł]'].iloc[1:].sum()
        revenue_from_products_of_1kg_lifestock = df['zysk ze sprzedaży kg żywca[zł]']

        df['% udział_w_zysku_ze_sprzedaży'] = revenue_from_products_of_1kg_lifestock\
                                              / total_revenue_from_products_of_1kg_lifestock
        df['Wielkość ceny zakupu [% udział w zysku * cena zakupu]'] = df['% udział_w_zysku_ze_sprzedaży']\
                                                                      * self.avg_lifestock_price

        # Carcass scenario
        # We calculate carcass_acquisition_price =
        #                                         lifestock_price - liver_acqusition_price -
        #                                         heart_acquisition_price - gizzard_acquisition_price
        lifestock_price = self.avg_lifestock_price
        liver_acquisition_price = df.loc[df.index == 'Wątroba', 'zysk ze sprzedaży kg żywca[zł]'].item()
        heart_acquisition_price = df.loc[df.index == 'Serce', 'zysk ze sprzedaży kg żywca[zł]'].item()
        gizzard_acquisition_price = df.loc[df.index == 'Żołądek', 'zysk ze sprzedaży kg żywca[zł]'].item()
        df.loc[
            df.index == 'Tuszka', 'Wielkość ceny zakupu [% udział w zysku * cena zakupu]'] = lifestock_price\
                                                                                             - liver_acquisition_price\
                                                                                             - heart_acquisition_price \
                                                                                             - gizzard_acquisition_price

        # Here we calculate final zł/kg for every product
        df['koszt_pozyskania_towaru [zł/kg]'] = df['Wielkość ceny zakupu [% udział w zysku * cena zakupu]'] \
                                                / df['Yield']

        return df

    def __split_quarter_acquisition_price(self):
        """Distributes quarter acquisition cost for further elements: leg, shank, deboned leg e.c.

        :return: DataFrame with acquisition cost for products after quarter processing
        """

        quarter_purchase_price = self.__provide_acquisition_cost_primary_products().filter(items=['Ćwiartka'], axis=0).loc[:,
                                 'Wielkość ceny zakupu [% udział w zysku * cena zakupu]'].iat[0]
        quarter_yield = self.products_yield.filter(items=[7437], axis=0)['Yield'].iat[0]

        # We split quarter_purchase price for leg and back with proportion 0.9 and 0.1
        leg_purchase_price = quarter_purchase_price * 0.9 / (quarter_yield * 0.71)
        back_purchase_price = quarter_purchase_price * 0.1 / (quarter_yield * 0.2874)

        # Further purchase_price_split according to assumed weight: thigh-0.52, shank-0.48
        thigh_purchase_price = (quarter_purchase_price * 0.9 * 0.52) / (quarter_yield * 0.71 * 0.48)
        shank_purchase_price = quarter_purchase_price * 0.9 * 0.48 / (quarter_yield * 0.71 * 0.513)

        # purchase_price_split for deboned products, according to: material_cost / product_weigh.
        leg_t = quarter_purchase_price * 0.9 / (quarter_yield * 0.71 * 0.6825)
        tigh_t = (quarter_purchase_price * 0.9 * 0.52) / (quarter_yield * 0.71 * 0.48 * 0.7357)

        #  creates dicts with results
        quarter_split = {'Noga': leg_purchase_price, 'Grzbiet': back_purchase_price, 'Udziec': thigh_purchase_price,
                         'Podudzie': shank_purchase_price, 'Noga T.': leg_t, 'Udziec T.': tigh_t}

        products = [60, 1714, 248, 240, 12013, 9859]
        products_yield = self.products_yield
        products_yield = products_yield[products_yield.index.isin(products)]
        products_yield = products_yield.reset_index().set_index('TOWAR')

        df = products_yield.join(self.avg_wholesales_prices)
        df['koszt_pozyskania_towaru [zł/kg]'] = df.index.map(quarter_split)

        return df


