import pandas as pd
import json
import numpy as np
from TreysDepartment.TreysParameters import TreysParameters
from GlobalParameters.ClassificationData import ClassificationData

pd.set_option('display.float_format', lambda x: '%.3f' % x)


class TreysDepartment(TreysParameters):

    def __init__(self, sales_dataframe, avg_wholesale_prices):
        super().__init__()
        self.sales = sales_dataframe
        self.avg_wholesale_prices = avg_wholesale_prices
        self.trays_sales = self.sales[
            (self.sales['INDEX_TOW'].isin(self.trays_products)) | (self.sales['KOD_KONTR'].isin([6011, 4859]))]
        self.__provide_materials_lables()
        self.__calculate_packages_boxes()
        self.__map_costs_of_production()
        self.product_names = ClassificationData.products_labels

    def generate_raport(self):
        """ Generates report for trays departament

        :return: DataFrame with columns: ['ILOSC', 'KOSZT_OPAKOWAN_ALL', 'SR_CENA', 'ŚR_CENA_HURT', 'ZYSK', 'WYNIK']
        """

        sr_cena_filet_vac_slowacja = 4.4 * 4.0
        # Updatujemy śr cene dla TWIST SK
        self.trays_sales['SR_CENA'] = np.where(
            (self.trays_sales['KOD_KONTR'] == 4674) & (self.trays_sales['INDEX_TOW'] == 1795),
            sr_cena_filet_vac_slowacja,
            self.trays_sales['SR_CENA'])
        # Updatujemy WARTOSC
        self.trays_sales['WARTOSC'] = np.where(
            (self.trays_sales['KOD_KONTR'] == 4674) & (self.trays_sales['INDEX_TOW'] == 1795),
            self.trays_sales['ILOSC'] * self.trays_sales['SR_CENA'],
            self.trays_sales['WARTOSC'])

        # Summary data_frame
        summary_df = self.trays_sales.groupby('TOWAR').sum()

        # dodajemy_index
        d_swap = {v: k for k, v in self.product_names.items()}
        self.avg_wholesale_prices['INDEX_TOW'] = self.avg_wholesale_prices.index.map(d_swap)
        summary_df['INDEX_TOW'] = summary_df.index.map(d_swap)

        # We add avg price which we will charge for products as if sold as primary products
        avg_prices_for_primary_products = []
        for index, row in summary_df.iterrows():
            index_row = row['INDEX_TOW']
            for key, value in self.product_map.items():
                if index_row in value:
                    avg_prices_for_primary_products.append(
                        self.avg_wholesale_prices[self.avg_wholesale_prices['INDEX_TOW'] == key]['ŚR_CENA'].iat[0])
                elif index_row == key:
                    avg_prices_for_primary_products.append(
                        self.avg_wholesale_prices[self.avg_wholesale_prices['INDEX_TOW'] == key]['ŚR_CENA'].iat[0])
        summary_df['ŚR_CENA_HURT'] = avg_prices_for_primary_products

        # Performing calculations on df
        summary_df['KOSZT_OPAKOWAN_ALL'] = summary_df['KOSZT_OPAKOWAN'] + summary_df['KOSZT_KARTON'] \
                                           + summary_df['KOSZT_ETYKIETA'] + summary_df['KOSZT_ABSORBER']

        summary_df['SR_CENA'] = summary_df['WARTOSC'] / summary_df['ILOSC']
        summary_df['ZYSK'] = (summary_df['SR_CENA'] - summary_df['ŚR_CENA_HURT']) * summary_df['ILOSC']
        summary_df['WYNIK'] = summary_df['ZYSK'] - summary_df['KOSZT_OPAKOWAN_ALL']

        # Tutaj wartość dodatnia, jaką wygenerował dział, bez kosztów pracy
        real_income = summary_df['WARTOSC'].sum() - summary_df['KOSZT_OPAKOWAN_ALL'].sum()
        added_value = summary_df['WYNIK'].sum()
        robocizna = 1050 * 50

        wynik_działu = added_value - robocizna

        output_df = summary_df[['ILOSC', 'KOSZT_OPAKOWAN_ALL', 'SR_CENA', 'ŚR_CENA_HURT', 'ZYSK', 'WYNIK']]

        return output_df

    def __provide_materials_lables(self):
        # Adds what material was used during production
        package = []

        for index, row in self.trays_sales.iterrows():
            product = row['TOWAR']
            if product in self.big_tray:
                package.append('Tacka Duża')
            elif product in self.small_tray:
                package.append('Tacka Mała')
            elif product in self.vac_small:
                package.append('Vac Mały')
            elif product in self.vac_big:
                package.append('Vac Duży')
            elif row['KOD_KONTR'] not in (6011, 4859):
                package.append('')
            else:
                package.append('Luz Karton')

        self.trays_sales['OPAKOWANIE'] = package

    def __calculate_packages_boxes(self):
        """Provides and calculates all data like: quantity of packages used, their price etc.

        :return:
        """

        box_quantity = []
        package_quantity = []

        packaging_cost = []
        box_type = []

        for index, row in self.trays_sales.iterrows():
            klient = row['KOD_KONTR']
            towar = row['INDEX_TOW']
            opakowanie = row['OPAKOWANIE']
            ilosc = row['ILOSC']

            # 1. Liczym ilosc i koszty opakowan
            try:
                q_opakowania = ilosc / self.material_parameters[opakowanie]['Ładowność']
                k_opakowania = q_opakowania * self.material_parameters[opakowanie]['Koszt']
            except:
                q_opakowania = 0
                k_opakowania = 0

            package_quantity.append(q_opakowania)
            packaging_cost.append(k_opakowania)

            # 2. Info jaki karton w zleżności od klienta

            # Selgros
            if klient == 6011:
                if towar in self.selgros['Karton']['Maly']:
                    box_type.append('Karton Mały')
                else:
                    box_type.append('Karton Duży')

            # E.Leclerk
            elif klient == 4859:
                if towar in self.leclerk['Karton']['Maly']:
                    box_type.append('Karton Mały')
                else:
                    box_type.append('Karton Duży')
            else:
                box_type.append('')

            # 3. Dodajemy ilosc kartonow

            # Selgros
            if klient == 6011:
                if towar in self.selgros['Pakowanie'][8]:
                    q_karton = ilosc / 8
                elif towar in self.selgros['Pakowanie'][6]:
                    q_karton = ilosc / 6
                elif towar in self.selgros['Pakowanie'][10]:
                    q_karton = ilosc / 10


            # E.Leclerk
            elif klient == 4859:
                if towar in self.leclerk['Pakowanie'][8]:
                    q_karton = ilosc / 8
                elif towar in self.leclerk['Pakowanie'][5]:
                    q_karton = ilosc / 5
                else:
                    q_karton = ilosc / 10
            else:
                q_karton = 0

            box_quantity.append(q_karton)
        #####

        # Dodajemy koszty kartonów

        self.trays_sales['KARTON'] = box_type
        self.trays_sales['Q_KARTON'] = box_quantity
        koszt_kartonow = []

        for index, row in self.trays_sales.iterrows():
            karton = row['KARTON']
            ilosc = row['Q_KARTON']

            if karton != '':
                k_karton = ilosc * self.material_parameters[karton]['Koszt']

            else:
                k_karton = 0

            koszt_kartonow.append(k_karton)

        self.trays_sales['Q_OPAKOWAN'] = package_quantity
        self.trays_sales['KOSZT_OPAKOWAN'] = packaging_cost

        self.trays_sales['KOSZT_KARTON'] = koszt_kartonow
        self.trays_sales['KOSZT_ETYKIETA'] = self.trays_sales['Q_OPAKOWAN'] * self.material_parameters['Etykieta'][
            'Koszt'] + \
                                             self.trays_sales['Q_KARTON'] * self.material_parameters['Etykieta'][
                                                 'Koszt']
        self.trays_sales['KOSZT_ABSORBER'] = self.trays_sales['Q_OPAKOWAN'] * self.material_parameters['Absorber'][
            'Koszt']

    def __map_costs_of_production(self):
        self.trays_sales['PRODUCT_COST'] = self.trays_sales['INDEX_TOW'].map(self.upc_all_products) * self.trays_sales[
            'ILOSC']

