from UnitProductionCostsCalculator.UnitProductionCostsCalculator import UnitProductionCostsCalculator

class TreysParameters():
    """
    This class represents standard parameters used in departament
    """
# Filet
    trays = {63: [1795, 13887, 13888],#filet
             7437: [10, 13885, 13886],#ćwiartka
             260: [13884],# tuszka
             248: [202, 13891, 13892], # udziec
             240: [356, 13893, 13894], # podudzie
             9859: [271], # udziec T
             12013: [14341], # noga T
             60: [674, 13889, 13890], # noga
             61: [418, 13895, 13896], # skrzydła

             }
    big_tray = ['Tuszka Tacka', 'Filet Tacka Duża', "Noga Tacka Duża", "Podudzie Tacka Duża", "Porcja Tacka Duża",
                  'Skrzydło Tacka Duża', 'Udziec Tacka Duża', 'Ćwiartka Tacka Duża']
    small_tray = ['Filet Tacka Mała', 'Noga Tacka Mała', 'Podudzie Tacka Mała', 'Skrzydło Tacka Mała',
                  'Udziec Tacka Mała', 'Ćwiartka Tacka Mała']
    vac_small = ['Noga T. Vac', 'Noga Vac', 'Podudzie Vac', 'Udziec T. Vac', 'Ćwiartka Vac', 'Skrzydło Vac']
    vac_big = ['Filet Vac']

    trays_products = [10, 202, 271, 356, 418, 674, 1795, 13884, 13885, 13887, 13888, 13889, 13891, 13893, 13895, 14341,
                      13886, 13890, 13892, 13894, 13896, 13897]

    material_costs = {'Tacka Duża': {'Koszt': 0.38, 'Ładowność': 1.2},
                        'Tacka Mała': {'Koszt': 0.20, 'Ładowność': 0.7},
                        'Tuszka Tacka': {'Koszt': 0.25, 'Ładowność': 2}, 'Absorber': {'Koszt': 0.13},
                        'Vac Duży': {'Koszt': 0.66, 'Ładowność': 5},
                        'Vac Mały': {'Koszt': 0.40, 'Ładowność': 2.75}, 'Etykieta': {'Koszt': 0.06},
                        'Karton Duży': {'Koszt': 2.93, 'Ładowność': {'Tacka': 6, 'Vac': 10}},
                        'Karton Mały': {'Koszt': 1.95}}

    # Information about what products are packed in which quantity regarding speific client
    selgros = {'Pakowanie': {8: [63, 185, 260, 7437, 9859, 156, 1580, 1714, 183, 60, 61, 74, 2131, 12013, 240, 248],
                             6: [13888, 13886, 13890, 13892, 13894, 13896, 13885, 13889, 13891, 13893, 13895, 13897],
                             10: [10, 202, 271, 356, 418, 674, 1795, 14341, 13884, 13887]
                             },
               'Karton': {'Maly': [63, 7437],
                          'Duzy': [10, 202, 271, 356, 418, 674, 1795, 14341, 13888, 13886, 13890, 13892, 13894, 13896,
                                   13885, 13887, 13889, 13891, 13893, 13895, 13897, 10, 185, 202, 260, 271, 356, 418,
                                   674, 1795, 9859, 14341, 156, 1580, 1714, 183, 60, 61, 74, 2131, 12013, 240, 248]
                          }
               }

    leclerk = {
        'Pakowanie': {8: [13885, 13887, 13889, 13891, 13893, 13895, 13897, 13888, 13886, 13890, 13892, 13894, 13896],
                      10: [10, 202, 271, 356, 418, 674, 1795, 14341, 10, 63, 185, 202, 260, 271, 356, 418, 674, 1795,
                           7437, 9859, 14341, 156, 1580, 1714, 183, 60, 61, 74, 2131, 12013, 240, 248],
                      5: [74, 183]
                      },
        'Karton': {'Maly': [63],
                   'Duzy': [7437, 10, 202, 271, 356, 418, 674, 1795, 14341, 13888, 13886, 13890, 13892, 13894, 13896,
                            13885, 13887, 13889, 13891, 13893, 13895, 13897, 10, 185, 202, 260, 271, 356, 418, 674,
                            1795, 9859, 14341, 156, 1580, 1714, 183, 60, 61, 74, 2131, 12013, 240, 248]}
        }


class TreysDepartment(TreysParameters):

    def __init__(self, sales_dataframe):
        self.sales = sales_dataframe
        self.trays_sales = self.sales[(self.sales['INDEX_TOW'].isin(self.trays_products)) | (self.sales['KOD_KONTR'].isin([6011, 4859]))]
        self.__provide_materials_lables()
        self.__calculate_packages_boxes()
        self.product_UPC = UnitProductionCostsCalculator().calculate()

    def generate_raport(self):
        # self.__provide_materials_lables()
        return self.trays_sales

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
        """
        This method provides and calculates all data like: quantity of packages used, their price etc.
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
                q_opakowania = ilosc / self.material_costs[opakowanie]['Ładowność']
                k_opakowania = q_opakowania * self.material_costs[opakowanie]['Koszt']
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
                k_karton = ilosc * self.material_costs[karton]['Koszt']

            else:
                k_karton = 0

            koszt_kartonow.append(k_karton)

        self.trays_sales['Q_OPAKOWAN'] = package_quantity
        self.trays_sales['KOSZT_OPAKOWAN'] = packaging_cost

        self.trays_sales['KOSZT_KARTON'] = koszt_kartonow
        self.trays_sales['KOSZT_ETYKIETA'] = self.trays_sales['Q_OPAKOWAN'] * self.material_costs['Etykieta']['Koszt'] + \
                                            self.trays_sales['Q_KARTON'] * self.material_costs['Etykieta']['Koszt']
        self.trays_sales['KOSZT_ABSORBER'] = self.trays_sales['Q_OPAKOWAN'] * self.material_costs['Absorber']['Koszt']

