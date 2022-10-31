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
        df['zysk ze sprzedaży kg żywca[zł]'] = df['ŚR_CENA'] * df['Yield']
        df['% udział_w_zysku_ze_sprzedaży'] = df['zysk ze sprzedaży kg żywca[zł]'] / df['zysk ze sprzedaży kg żywca[zł]'].iloc[1:].sum()
        df['Wielkość ceny zakupu [% udział w zysku * cena zakupu]'] = df['% udział_w_zysku_ze_sprzedaży'] * self.avg_lifestock_price

        # Tutaj dla tuszki trzeba zmienić bo jak ją sprzedam to nie moge uzyskac innych elementów
        # Czyli wielkość ceny zakupu to cena żywca - potroby
        x = (self.avg_lifestock_price - df.loc[df.index == 'Wątroba', 'zysk ze sprzedaży kg żywca[zł]'].item())
        y = df.loc[df.index == 'Serce', 'zysk ze sprzedaży kg żywca[zł]'].item()
        z = df.loc[df.index == 'Żołądek', 'zysk ze sprzedaży kg żywca[zł]'].item()
        df.loc[df.index == 'Tuszka', 'Wielkość ceny zakupu [% udział w zysku * cena zakupu]'] = x - y - z

        # Ostateczna kolumna przypsująca kg produktu odpowiednią cene zakupu w oparciu o śr cene żywca
        df['koszt_pozyskania_towaru [zł/kg]'] = df['Wielkość ceny zakupu [% udział w zysku * cena zakupu]'] / df['Yield']

        return df


    def quarter_purchuse_price_splitter(self):
        """
        Distributes lifestock purchuse price of quarter for further elements: noga, podudzie, nogaT..
        :return: DataFrame
        """

        quarter_purchase_price = self.split_lifestock_purchuse_price().filter(items=['Ćwiartka'], axis=0).loc[:,'Wielkość ceny zakupu [% udział w zysku * cena zakupu]'].iat[0]
        quarter_yield = self.products_yield.filter(items = [7437], axis=0)['Yield'].iat[0]

        noga_purchase_price = quarter_yield * 0.71 / (quarter_purchase_price * 0.9)
        grzbiet_purchuse_price = quarter_yield * 0.2874 / (quarter_purchase_price * 0.1)

        udo_purchase_price = quarter_yield * 0.71 * 0.48 / (quarter_purchase_price * 0.9 * 0.5)
        podudzie_purchase_price = quarter_yield * 0.71 * 0.513 / (quarter_purchase_price * 0.9 * 0.48)




        products = [60, 1714, 248, 240, 12013, 9859]
        products_yield = self.products_yield
        products_yield = products_yield[products_yield.index.isin(products)]
        products_yield = products_yield.reset_index().set_index('TOWAR')

        df = products_yield.join(self.avg_sales_prices)

        return quarter_yield