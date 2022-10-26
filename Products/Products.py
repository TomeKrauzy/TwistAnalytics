from DataSource.AnalyticsDataSource import AnalyticsDataSource


class ProductionParameters():

    products_yelds = AnalyticsDataSource().provide().products_yield
    labor_hour_cost = 50
    avg_lifestock_weight = 3

    # carcass/hour
    confectionery_speed = 2760
    # lifestock/hour
    slaughter_speed = 3720
    # breast line speed, cone/hour
    breast_speed = 2520


# Tuszka
class Carcass(ProductionParameters):

    """
    Class for Carcess used for further confection
    """

    def __init__(self):
        super().__init__()
        # How much people are involved in production process
        self.labour = self.__provide_labour_amount()
        # How much brest is produced in hour
        self.production_efficiency = 42 * 60

    def provide_labour_cost_markup(self):
        pass

    def __provide_labour_amount(self):

        labour_units = {'rozładunek':2,
                        'transport_koszy_zawieszanie':5,
                        'myjka_koszy':2,
                        'noż_ubojowy':1,
                        'skubarka':2,
                        'kontrola_pierza':1,
                        'obrywacz_głów':1,
                        'czyszczenie_łap':1,
                        'kontrola_jakosci':1,
                        'separator_serce_wątroba':3,
                        'zawieszanie_chłodzenie':3,
                        'myjka_pojemnikow':2,
                        'wywóz_palet':2,
                        'brygadzisci':2,
                        }

        return sum(labour_units.values())

class Carcass_sale(Carcass):

    """
    Class for Carcess sold as a whole
    """

    def __init__(self):
        super().__init__()
        self.labour += self.__provide_labour_amount()

    def __provide_labour_amount(self):
        labour_units = {
            'Przenośnik_taśmowy_zawieszanie':2,
            'System wagowy':3,
            'Waga końcowa':1,
            'Spedycja':3,
            'Zamówienia Sklepy': 1,
        }
        return sum(labour_units.values())


# Żołądki
class Gizzards(ProductionParameters):

    def __int__(self):
        super.__init__()
        # How much people are involved in production process
        self.labour = 1
        # How much brest is produced in hour
        self.production_efficiency = 42 * 60

class Liver(ProductionParameters):

    def __int__(self):
        super.__init__()
        # How much people are involved in production process
        self.labour = 2
        # How much brest is produced in hour
        self.production_efficiency = 42 * 60

class Heart(ProductionParameters):

    def __int__(self):
        super.__init__()
        # How much people are involved in production process
        self.labour = 2
        # How much brest is produced in hour
        self.production_efficiency = 42 * 60

class Wing(ProductionParameters):

    def __int__(self):
        super.__init__()
        # How much people are involved in production process
        self.labour = 1
        # How much brest is produced in hour
        self.production_efficiency = 42 * 60


class Quarter(ProductionParameters):

    def __int__(self):
        super.__init__()
        # How much people are involved in production process
        self.labour = 1
        # How much brest is produced in hour
        self.production_efficiency = 42 * 60

class Breast(ProductionParameters):

    def __int__(self):
        super.__init__()
        # How much people are involved in production process
        self.labour = 13
        # How much brest is produced in hour
        self.production_efficiency = 42 * 60


class Portion(ProductionParameters):

    def __int__(self):
        super.__init__()
        # How much people are involved in production process
        self.labour = 1
        # How much brest is produced in hour
        self.production_efficiency = 42 * 60

