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

