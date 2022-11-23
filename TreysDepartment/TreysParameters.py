import pandas as pd
from UnitProductionCostsCalculator.UnitProductionCostsCalculator import UnitProductionCostsCalculator

product_map = {63: [1795, 13887, 13888],  # filet
                   7437: [10, 13885, 13886],  # ćwiartka
                   260: [13884],  # tuszka
                   248: [202, 13891, 13892],  # udziec
                   240: [356, 13893, 13894],  # podudzie
                   9859: [271],  # udziec T
                   12013: [14341],  # noga T
                   60: [674, 13889, 13890],  # noga
                   61: [418, 13895, 13896],  # skrzydła
                   156: [13897],  # porcja
                   74: [],  # serce
                   183: [],  # żołądek
                   }

class TreysParameters:
    """ This class represents standard parameters used in departament
    """

    def __init__(self):
        self.upc_all_products = self.__provide_upc_all_products()

    primary_products = [260, 7437, 63, 156, 61, 185, 183, 74]

    product_map = {63: [1795, 13887, 13888],  # filet
                   7437: [10, 13885, 13886],  # ćwiartka
                   260: [13884],  # tuszka
                   248: [202, 13891, 13892],  # udziec
                   240: [356, 13893, 13894],  # podudzie
                   9859: [271],  # udziec T
                   12013: [14341],  # noga T
                   60: [674, 13889, 13890],  # noga
                   61: [418, 13895, 13896],  # skrzydła
                   156: [13897],  # porcja
                   74: [],  # serce
                   183: [],  # żołądek
                   }

    big_tray = ['Tuszka Tacka', 'Filet Tacka Duża', "Noga Tacka Duża", "Podudzie Tacka Duża", "Porcja Tacka Duża",
                'Skrzydło Tacka Duża', 'Udziec Tacka Duża', 'Ćwiartka Tacka Duża']
    small_tray = ['Filet Tacka Mała', 'Noga Tacka Mała', 'Podudzie Tacka Mała', 'Skrzydło Tacka Mała',
                  'Udziec Tacka Mała', 'Ćwiartka Tacka Mała']
    vac_small = ['Noga T. Vac', 'Noga Vac', 'Podudzie Vac', 'Udziec T. Vac', 'Ćwiartka Vac', 'Skrzydło Vac']
    vac_big = ['Filet Vac']

    trays_products = [10, 202, 271, 356, 418, 674, 1795, 13884, 13885, 13887, 13888, 13889, 13891, 13893, 13895, 14341,
                      13886, 13890, 13892, 13894, 13896, 13897]

    material_parameters = {'Tacka Duża': {'Koszt': 0.38, 'Ładowność': 1.2},
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

    def __provide_upc_all_products(self):
        """Adds upc for treys products, which is same as for base products equivalent

        :return: DataFrame with all upc for all products
        """
        upc = UnitProductionCostsCalculator().provide_primary_products_UPC()

        trays_upc = {}
        for base_product_index, trays_product in self.product_map.items():
            for product in trays_product:
                trays_upc[product] = upc.loc[base_product_index]
        df = pd.concat([pd.Series(trays_upc), upc])
        return df
