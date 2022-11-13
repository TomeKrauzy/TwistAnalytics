import pandas as pd
from GlobalParameters.ProductionParameters import ProductionParameters


class Carcass(ProductionParameters):
    """Class for Carcass used for further confection
    """

    def __init__(self):
        super().__init__()
        # How many people are involved in production process
        self.labour = self.__provide_labour_amount()
        self.labour_markup = self.__provide_labour_markup()

    def __provide_labour_markup(self):
        yeld = self.PRODUCTS_YELDS[self.PRODUCTS_YELDS['TOWAR'] == 'Tuszka']['Yield']

        production_in_kg_per_hour = self.SLAUGHTER_SPEED * self.AVG_LIFESTOCK_WEIGHT * yeld
        labour_costs_per_hour = self.labour * self.LABOUR_HOUR_COST
        labour_costs_markup = labour_costs_per_hour / production_in_kg_per_hour
        return labour_costs_markup

    def __provide_labour_amount(self):
        labour_units = {'rozładunek': 2,
                        'transport_koszy_zawieszanie': 5,
                        'myjka_koszy': 2,
                        'noż_ubojowy': 1,
                        'skubarka': 2,
                        'kontrola_pierza': 1,
                        'obrywacz_głów': 1,
                        'czyszczenie_łap': 1,
                        'kontrola_jakosci': 1,
                        'separator_serce_wątroba': 3,
                        'zawieszanie_chłodzenie': 3,
                        'myjka_pojemnikow': 2,
                        'wywóz_palet': 2,
                        'brygadzisci': 2,
                        }
        return sum(labour_units.values())


class Carcass_sale(Carcass):
    """
    Class for Carcass sold as a whole
    """

    def __init__(self):
        super().__init__()
        # We add extra costs of spedition to base Carcass
        self.labour += self.__provide_labour_amount()
        self.labour_markup = self.__provide_labour_markup()

    def __provide_labour_amount(self):
        """
        Here we do add extra labour_units on top of the Carcass class
        :return:
        """
        labour_units = {
            'Przenośnik_taśmowy_zawieszanie': 2,
            'System wagowy': 3,
            'Waga końcowa': 1,
            'Spedycja': 3,
            'Zamówienia Sklepy': 1,
        }
        return sum(labour_units.values())

    def __provide_labour_markup(self):
        yeld = self.PRODUCTS_YELDS[self.PRODUCTS_YELDS['TOWAR'] == 'Tuszka']['Yield']

        production_in_kg_per_hour = self.SLAUGHTER_SPEED * self.AVG_LIFESTOCK_WEIGHT * yeld
        labour_costs_per_hour = self.labour * self.LABOUR_HOUR_COST
        labour_costs_markup = labour_costs_per_hour / production_in_kg_per_hour
        return labour_costs_markup


class Gizzard(ProductionParameters):
    def __init__(self):
        super().__init__()
        self.labour = 1
        self.labour_markup = self.__provide_labour_markup()

    def __provide_labour_markup(self):
        yeld = self.PRODUCTS_YELDS[self.PRODUCTS_YELDS['TOWAR'] == 'Żołądek']['Yield']

        production_in_kg_per_hour = self.SLAUGHTER_SPEED * self.AVG_LIFESTOCK_WEIGHT * yeld
        labour_costs_per_hour = self.labour * self.LABOUR_HOUR_COST
        labour_costs_markup = labour_costs_per_hour / production_in_kg_per_hour
        return labour_costs_markup


class Liver(ProductionParameters):
    def __init__(self):
        super().__init__()
        self.labour = 1
        self.labour_markup = self.__provide_labour_markup()

    def __provide_labour_markup(self):
        yeld = self.PRODUCTS_YELDS[self.PRODUCTS_YELDS['TOWAR'] == 'Wątroba']['Yield']

        production_in_kg_per_hour = self.SLAUGHTER_SPEED * self.AVG_LIFESTOCK_WEIGHT * yeld
        labour_costs_per_hour = self.labour * self.LABOUR_HOUR_COST
        labour_costs_markup = labour_costs_per_hour / production_in_kg_per_hour
        return labour_costs_markup


class Heart(ProductionParameters):
    def __init__(self):
        super().__init__()
        self.labour = 1
        self.labour_markup = self.__provide_labour_markup()

    def __provide_labour_markup(self):
        yeld = self.PRODUCTS_YELDS[self.PRODUCTS_YELDS['TOWAR'] == 'Serce']['Yield']

        production_in_kg_per_hour = self.SLAUGHTER_SPEED * self.AVG_LIFESTOCK_WEIGHT * yeld
        labour_costs_per_hour = self.labour * self.LABOUR_HOUR_COST
        labour_costs_markup = labour_costs_per_hour / production_in_kg_per_hour
        return labour_costs_markup


class Wing(ProductionParameters):
    def __init__(self):
        super().__init__()
        self.labour = 1
        self.labour_markup = self.__provide_labour_markup()

    def __provide_labour_markup(self):
        yeld = self.PRODUCTS_YELDS[self.PRODUCTS_YELDS['TOWAR'] == 'Skrzydło']['Yield']

        production_in_kg_per_hour = self.CONFECIONERY_SPEED * self.AVG_LIFESTOCK_WEIGHT * yeld
        labour_costs_per_hour = self.labour * self.LABOUR_HOUR_COST
        labour_costs_markup = labour_costs_per_hour / production_in_kg_per_hour

        # Here we add 1/3 of carcass upc, because we need to markup it's costs on further products
        # that carcass is processed into. (breast, quarter, wing)
        labour_costs_markup += Carcass().labour_markup.values[0] / 3
        return labour_costs_markup


class Quarter(ProductionParameters):
    def __init__(self):
        super().__init__()
        self.labour = 1
        self.labour_markup = self.__provide_labour_markup()

    def __provide_labour_markup(self):
        yeld = self.PRODUCTS_YELDS[self.PRODUCTS_YELDS['TOWAR'] == 'Ćwiartka']['Yield']

        production_in_kg_per_hour = self.CONFECIONERY_SPEED * self.AVG_LIFESTOCK_WEIGHT * yeld
        labour_costs_per_hour = self.labour * self.LABOUR_HOUR_COST
        labour_costs_markup = labour_costs_per_hour / production_in_kg_per_hour

        # Here we add 1/3 of carcass upc, because we need to markup it's costs on further products
        # that carcass is processed into. (breast, quarter, wing)
        labour_costs_markup += Carcass().labour_markup.values[0] / 3
        return labour_costs_markup


class Breast(ProductionParameters):
    def __init__(self):
        super().__init__()
        self.labour = 1
        self.labour_markup = self.__provide_labour_markup()

    def __provide_labour_markup(self):
        yeld = self.PRODUCTS_YELDS[self.PRODUCTS_YELDS['TOWAR'] == 'Filet']['Yield']

        production_in_kg_per_hour = self.BREAST_SPEED * self.AVG_LIFESTOCK_WEIGHT * yeld
        labour_costs_per_hour = self.labour * self.LABOUR_HOUR_COST
        labour_costs_markup = labour_costs_per_hour / production_in_kg_per_hour

        # Here we add 1/3 of carcass upc, because we need to markup it's costs on further products
        # that carcass is processed into. (breast, quarter, wing)
        labour_costs_markup += Carcass().labour_markup.values[0] / 3
        return labour_costs_markup


class Portion(ProductionParameters):
    def __init__(self):
        super().__init__()
        self.labour = 1
        self.labour_markup = self.__provide_labour_markup()

    def __provide_labour_markup(self):
        yeld = self.PRODUCTS_YELDS[self.PRODUCTS_YELDS['TOWAR'] == 'Porcja']['Yield']

        production_in_kg_per_hour = self.BREAST_SPEED * self.AVG_LIFESTOCK_WEIGHT * yeld
        labour_costs_per_hour = self.labour * self.LABOUR_HOUR_COST
        labour_costs_markup = labour_costs_per_hour / production_in_kg_per_hour

        # Here we add 1/3 of carcass upc, because we need to markup it's costs on further products
        # that carcass is processed into. (breast, quarter, wing)
        labour_costs_markup += Carcass().labour_markup.values[0] / 3
        return labour_costs_markup


# ------------------------------------- Elements from Quarter ------------------------------------------------------
class Leg(ProductionParameters):
    def __init__(self):
        super().__init__()
        self.labour = 1
        self.labour_markup = self.__provide_labour_markup()

    def __provide_labour_markup(self):
        yeld = self.PRODUCTS_YELDS[self.PRODUCTS_YELDS['TOWAR'] == 'Noga']['Yield']

        production_in_kg_per_hour = self.CONFECIONERY_SPEED * self.AVG_LIFESTOCK_WEIGHT * yeld
        labour_costs_per_hour = self.labour * self.LABOUR_HOUR_COST
        labour_costs_markup = labour_costs_per_hour / production_in_kg_per_hour
        return labour_costs_markup


class Thigh(ProductionParameters):
    def __init__(self):
        super().__init__()
        self.labour = 1
        self.labour_markup = self.__provide_labour_markup()

    def __provide_labour_markup(self):
        yeld = self.PRODUCTS_YELDS[self.PRODUCTS_YELDS['TOWAR'] == 'Udziec']['Yield']

        production_in_kg_per_hour = self.CONFECIONERY_SPEED * self.AVG_LIFESTOCK_WEIGHT * yeld
        labour_costs_per_hour = self.labour * self.LABOUR_HOUR_COST
        labour_costs_markup = labour_costs_per_hour / production_in_kg_per_hour
        labour_costs_markup = pd.Series(labour_costs_markup, index=[248])
        return labour_costs_markup


class Shank(ProductionParameters):
    def __init__(self):
        super().__init__()
        # How much people are involved in production process
        self.labour = 1
        self.labour_markup = self.__provide_labour_markup()

    def __provide_labour_markup(self):
        yeld = self.PRODUCTS_YELDS[self.PRODUCTS_YELDS['TOWAR'] == 'Podudzie']['Yield']

        production_in_kg_per_hour = self.CONFECIONERY_SPEED * self.AVG_LIFESTOCK_WEIGHT * yeld
        labour_costs_per_hour = self.labour * self.LABOUR_HOUR_COST
        labour_costs_markup = labour_costs_per_hour / production_in_kg_per_hour
        labour_costs_markup = pd.Series(labour_costs_markup, index=[240])
        return labour_costs_markup


class Leg_deboned(ProductionParameters):
    def __init__(self):
        super().__init__()
        self.labour = 8
        self.labour_markup = self.__provide_labour_markup()

    def __provide_labour_markup(self):
        production_in_kg_per_hour = self.LEG_DEBONING_EFFICIENCY * self.labour
        labour_costs_per_hour = self.labour * self.LABOUR_HOUR_COST
        labour_costs_markup = labour_costs_per_hour / production_in_kg_per_hour
        labour_costs_markup = pd.Series(labour_costs_markup, index=[12013])
        return labour_costs_markup


class Tigh_deboned(ProductionParameters):
    def __init__(self):
        super().__init__()
        # How much people are involved in production process
        self.labour = 8
        self.labour_markup = self.__provide_labour_markup()

    def __provide_labour_markup(self):
        production_in_kg_per_hour = self.TIGH_DEBONING_EFFICIENCY * self.labour
        labour_costs_per_hour = self.labour * self.LABOUR_HOUR_COST
        labour_costs_markup = labour_costs_per_hour / production_in_kg_per_hour
        labour_costs_markup = pd.Series(labour_costs_markup, index=[9859])

        return labour_costs_markup
