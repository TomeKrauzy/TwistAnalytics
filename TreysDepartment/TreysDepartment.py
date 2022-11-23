import numpy as np
from TreysDepartment.TreysParameters import TreysParameters
from GlobalParameters.ClassificationData import ClassificationData


class TreysDepartment(TreysParameters):

    def __init__(self, sales_dataframe, avg_wholesale_prices, acqusition_cost_df):
        super().__init__()
        self.sales = sales_dataframe
        self.product_names = ClassificationData.products_labels
        self.avg_wholesale_prices = avg_wholesale_prices
        self.trays_sales = self.sales[(self.sales['INDEX_TOW'].isin(self.trays_products))
                                      | (self.sales['KOD_KONTR'].isin([6011, 4859]))]
        self.acquisition_cost = acqusition_cost_df

        self.__provide_package_lables()
        self.__calculate_packages_boxes()
        self.__map_costs_of_production()
        self.__update_prices_for_TwistSK()
        self.summary_df = self.__provide_summary_df()

    def generate_reports(self):
        """ Generates report for trays departament

        :return: DataFrame with columns: ['ILOSC', 'KOSZT_OPAKOWAN_ALL',
         'SR_CENA', 'ŚR_CENA_HURT', 'MARŻA', 'WYNIK']
        """
        # DataFrame with detailed info for treys departament
        detailed_df = self.trays_sales[['NAZ_KONTR', 'TOWAR', 'ILOSC', 'SR_CENA', 'WARTOSC',
                                        'OPAKOWANIE', 'KARTON', 'Q_KARTON',
                                        'Q_OPAKOWAN',
                                        'KOSZT_OPAKOWAN',
                                        'KOSZT_KARTON', 'KOSZT_ETYKIETA', 'KOSZT_ABSORBER']]

        # Summary df
        summary_df = self.summary_df
        summary_df['KOSZT_OPAKOWAN_ALL'] = summary_df['KOSZT_OPAKOWAN'] + summary_df['KOSZT_KARTON'] \
                                           + summary_df['KOSZT_ETYKIETA'] + summary_df['KOSZT_ABSORBER']
        summary_df['SR_CENA'] = summary_df['WARTOSC'] / summary_df['ILOSC']
        summary_df['JK.PAKOWANIA'] = summary_df['KOSZT_OPAKOWAN_ALL'] / summary_df['ILOSC']
        summary_df['JKW'] = summary_df['UPC'] + summary_df['ACQ_COST'] + summary_df['JK.PAKOWANIA']
        summary_df['MARŻA % TACKI'] = summary_df['SR_CENA'] / summary_df['JKW']
        summary_df['ZYSK/STRATA'] = (summary_df['SR_CENA'] - summary_df['JKW']) * summary_df['ILOSC']
        summary_df['MARŻA % HURT'] = summary_df['ŚR_CENA_HURT'] / (summary_df['UPC'] + summary_df['ACQ_COST'])

        output_df = summary_df[['ILOSC', 'WARTOSC',
                                'SR_CENA', 'ŚR_CENA_HURT',
                                'UPC', 'ACQ_COST', 'JK.PAKOWANIA', 'JKW',
                                'MARŻA % TACKI',
                                'MARŻA % HURT',
                                'KOSZT_OPAKOWAN_ALL',
                                'ZYSK/STRATA'
                                ]
        ]
        return (output_df, detailed_df)

    # region Methods used for preparing data for raports

    def __provide_package_lables(self):
        """Adds to sales_df column OPAKOWANIE, which represents what package was the product put in
        e.i:
        Tacka Duża,
        Tacka Mała
        Vac Mały
        Vac Duży
        Luz Karton

        :return: DataFrame + [OPAKOWANIE]
        """

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

        packages: treys, vac etc.
        boxes: containers for packages e.g. 7 treys in one box

        :return:
        """

        box_quantity = []
        box_type = []
        package_quantity = []
        packaging_cost = []

        # maps box quantity, box_type, package_quantity, package_cost
        for index, row in self.trays_sales.iterrows():
            customer_id = row['KOD_KONTR']
            product = row['INDEX_TOW']
            package = row['OPAKOWANIE']
            product_quantity = row['ILOSC']

            # 1. calculates costs and quantity of package used
            try:
                package_q = product_quantity / self.material_parameters[package]['Ładowność']
                package_cost = package_q * self.material_parameters[package]['Koszt']
            except:
                package_q = 0
                package_cost = 0

            package_quantity.append(package_q)
            packaging_cost.append(package_cost)

            # 2. maps box used for specific client and product e.g. Filet Vac -> Karton Duży
            # Selgros case
            if customer_id == 6011:
                if product in self.selgros['Karton']['Maly']:
                    box_type.append('Karton Mały')
                else:
                    box_type.append('Karton Duży')

            # E.Leclerk case
            elif customer_id == 4859:
                if product in self.leclerk['Karton']['Maly']:
                    box_type.append('Karton Mały')
                else:
                    box_type.append('Karton Duży')
            else:
                box_type.append('')

            # 3. adds boxes quantity
            # Selgros case
            if customer_id == 6011:
                if product in self.selgros['Pakowanie'][8]:
                    q_karton = product_quantity / 8
                elif product in self.selgros['Pakowanie'][6]:
                    q_karton = product_quantity / 6
                elif product in self.selgros['Pakowanie'][10]:
                    q_karton = product_quantity / 10

            # E.Leclerk case
            elif customer_id == 4859:
                if product in self.leclerk['Pakowanie'][8]:
                    q_karton = product_quantity / 8
                elif product in self.leclerk['Pakowanie'][5]:
                    q_karton = product_quantity / 5
                else:
                    q_karton = product_quantity / 10
            else:
                q_karton = 0
            box_quantity.append(q_karton)
        self.trays_sales['KARTON'] = box_type
        self.trays_sales['Q_KARTON'] = box_quantity
        self.trays_sales['Q_OPAKOWAN'] = package_quantity
        self.trays_sales['KOSZT_OPAKOWAN'] = packaging_cost

        # maps boxes costs
        box_costs = []
        for index, row in self.trays_sales.iterrows():
            box = row['KARTON']
            product_quantity = row['Q_KARTON']

            # case when products are packed inside box
            if box != '':
                box_cost = product_quantity * self.material_parameters[box]['Koszt']
            else:
                box_cost = 0
            box_costs.append(box_cost)
        self.trays_sales['KOSZT_KARTON'] = box_costs

        # performs calculation
        self.trays_sales['KOSZT_ETYKIETA'] = self.trays_sales['Q_OPAKOWAN'] \
                                             * self.material_parameters['Etykieta']['Koszt'] \
                                             + self.trays_sales['Q_KARTON'] \
                                             * self.material_parameters['Etykieta']['Koszt']

        self.trays_sales['KOSZT_ABSORBER'] = self.trays_sales['Q_OPAKOWAN'] \
                                             * self.material_parameters['Absorber']['Koszt']

    def __map_costs_of_production(self):
        self.trays_sales['PRODUCT_COST'] = self.trays_sales['INDEX_TOW'].map(self.upc_all_products) \
                                           * self.trays_sales['ILOSC']

    def __update_prices_for_TwistSK(self):
        # We have to change price manually for VAC-Breast sold for TWIST-SK with production price
        avg_vac_breast_sk_price = 4.4 * 3.8
        self.trays_sales['SR_CENA'] = np.where((self.trays_sales['KOD_KONTR'] == 4674)
                                               & (self.trays_sales['INDEX_TOW'] == 1795),
                                               avg_vac_breast_sk_price,
                                               self.trays_sales['SR_CENA'])

        # New price, so we update WARTOSC = (new_price * quantity)
        self.trays_sales['WARTOSC'] = np.where((self.trays_sales['KOD_KONTR'] == 4674)
                                               & (self.trays_sales['INDEX_TOW'] == 1795),
                                               self.trays_sales['ILOSC'] * self.trays_sales['SR_CENA'],
                                               self.trays_sales['WARTOSC'])

    def __provide_summary_df(self):
        """Provides summary DataFrame grouped by TOWAR with columns
        ['KOD_KONTR', 'INDEX_TOW', 'ILOSC', 'SR_CENA', 'WARTOSC', 'Q_KARTON',
        'Q_OPAKOWAN', 'KOSZT_OPAKOWAN', 'KOSZT_KARTON', 'KOSZT_ETYKIETA',
        'KOSZT_ABSORBER', 'PRODUCT_COST', 'ŚR_CENA_HURT']

        :return: DataFrame
        """

        summary_df = self.trays_sales.groupby('TOWAR').sum()

        # We add product index to summary_df and wholesale_prices df
        d_swap = {v: k for k, v in self.product_names.items()}

        self.avg_wholesale_prices['INDEX_TOW'] = self.avg_wholesale_prices.index.map(d_swap)
        summary_df['INDEX_TOW'] = summary_df.index.map(d_swap)

        # We add avg price that we would charge for products as if were sold as primary products
        # e.g. price_Noga_Vac = price_Noga
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

        summary_df['UPC'] = summary_df['INDEX_TOW'].map(self.upc_all_products)
        # adds acquisition cost
        summary_df['ACQ_COST'] = summary_df['INDEX_TOW'].map(self.acquisition_cost['koszt_pozyskania_towaru [zł/kg]'])
        return summary_df

    # endregion
