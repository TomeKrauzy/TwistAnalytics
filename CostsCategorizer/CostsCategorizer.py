from CostsCategorizer.CostsContainer import CostsContainer
from CostsCategorizer.CostsUnitsContainers.Ubój import Ubój

class CostsCategorizer():
    """
    This class is responsible for categorizing all costs from accounts for more precise and specific categories
    that are used for farther unit production cost calculations.

    This class returns cost amount that occured in specific period for specific business areas like: Transport.
    """
    # cmd + p podpowiada parametry

    def __init__(self, cost_dataframe):
        self.cost_dataframe = cost_dataframe

    def provide_data(self):
        container = CostsContainer(self.__provide_ubój(), self.__provide_rozbiór(), self.__provide_mycie(),
                                    self.__provide_warsztat(), self.__provide_sklepy(), self.__provide_transport_costs(),
                                   self.__provide_fakturowanie(), self.__provide_administracja(), self.__provide_tacki(),
                                   self.__provide_koszty_ogólne(), self.__provide_zakład_karny())
        return container


    def __provide_ubój(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['UBÓJ']
        stoping_index = indexes['ROZBIÓR']

        # Wycinamy tylko część dla uboju
        df = self.cost_dataframe.iloc[starting_index:stoping_index,]

        koszty_całe = df.iloc[0, 2]
        koszty_pracy = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:,2]

        slaugter_costs = Ubój(koszty_całe, koszty_pracy)

        return slaugter_costs


    def __provide_rozbiór(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['ROZBIÓR']
        stoping_index = indexes['MYCIE ZAKłADU']

        # Wycinamy tylko część dla uboju
        df = self.cost_dataframe.iloc[starting_index:stoping_index, ]
        koszty_całe = df.iloc[0, 2]
        koszty_pracy = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:, 2]
        print(indexes)

        return koszty_pracy

    def __provide_mycie(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['MYCIE ZAKłADU']
        stoping_index = indexes['WARSZTAT']

        # Wycinamy tylko część dla uboju
        df = self.cost_dataframe.iloc[starting_index:stoping_index, ]
        koszty_całe = df.iloc[0, 2]
        koszty_pracy = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:, 2]

        return koszty_pracy

    def __provide_warsztat(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['WARSZTAT']
        stoping_index = indexes['PUNKTY SPRZEDAżY']

        # Wycinamy tylko część dla uboju
        df = self.cost_dataframe.iloc[starting_index:stoping_index, ]
        koszty_całe = df.iloc[0, 2]
        koszty_pracy = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:, 2]

        return koszty_pracy

    def __provide_sklepy(self):
        pass

    def __provide_fakturowanie(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['FAKTUROWANIE']
        stoping_index = indexes['ADMINISTRACJA']

        # Wycinamy tylko część dla uboju
        df = self.cost_dataframe.iloc[starting_index:stoping_index, ]
        koszty_całe = df.iloc[0, 2]
        koszty_pracy = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:, 2]

        return koszty_pracy

    def __provide_administracja(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['ADMINISTRACJA']
        stoping_index = indexes['KOSZTY SPRZEDAżY']

        # Wycinamy tylko część dla uboju
        df = self.cost_dataframe.iloc[starting_index:stoping_index, ]
        koszty_całe = df.iloc[0, 2]
        koszty_pracy = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:, 2]

        return koszty_pracy


    def __provide_tacki(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['KOSZTY SPRZEDAżY']
        stoping_index = indexes['KOSZTY OGÓLNE']

        # Wycinamy tylko część dla uboju
        df = self.cost_dataframe.iloc[starting_index:stoping_index, ]
        koszty_całe = df.iloc[0, 2]
        koszty_pracy = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:, 2]

        return koszty_pracy

    def __provide_koszty_ogólne(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['KOSZTY OGÓLNE']
        stoping_index = indexes['ZAKłAD KARNY']

        # Wycinamy tylko część dla uboju
        df = self.cost_dataframe.iloc[starting_index:stoping_index, ]
        koszty_całe = df.iloc[0, 2]
        koszty_pracy = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:, 2]

        return koszty_pracy

    def __provide_zakład_karny(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['ZAKłAD KARNY']

        # Wycinamy tylko część dla uboju
        df = self.cost_dataframe.iloc[starting_index: , ]
        koszty_całe = df.iloc[0, 2]
        koszty_pracy = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:, 2]

        return koszty_pracy


    def __provide_transport_costs(self):
        pass


    def __provide_costs_categories_indexes(self):
        """
        Provides starting indexes of diffrent cost categories in df
        :return: dictionary {Category: Index}
        """

        df = self.cost_dataframe
        costs_categories_indexes = {df.iloc[i, 1]: i for i in
                                    df[df['KONTO'] > 500].index}


        return costs_categories_indexes
