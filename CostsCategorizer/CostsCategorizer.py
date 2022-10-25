from CostsCategorizer.CostsContainer import CostsContainer
from CostsCategorizer.CostsUnitContainer import CostsUnitContainer


# cmd + p podpowiada parametry

class CostsCategorizer():
    """
    This class is responsible for categorizing all costs from accounts for more precise and specific categories
    that are used for farther unit production cost calculations.

    This class returns cost amount that occured in specific period for specific business areas like: Transport.
    """

    def __init__(self, cost_dataframe):
        self.cost_dataframe = cost_dataframe

    def provide_data(self):
        container = CostsContainer(self.__provide_slaughter(), self.__provide_confectionery(), self.__provide_washing(),
                                   self.__provide_workshop(), self.__provide_shops(), self.__provide_transport_costs(),
                                   self.__provide_invoicing(), self.__provide_administration(),
                                   self.__provide_trays(),
                                   self.__provide_general_costs(), self.__provide_jail())
        return container

    def __provide_slaughter(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['UBÓJ']
        stoping_index = indexes['ROZBIÓR']

        df = self.cost_dataframe.iloc[starting_index:stoping_index, ]
        total_costs = df.iloc[0, 2]
        labour_costs = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[0, 2]

        slaughter = CostsUnitContainer('Ubój', labour=labour_costs, total=total_costs)
        return slaughter

    def __provide_confectionery(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['ROZBIÓR']
        stoping_index = indexes['MYCIE ZAKłADU']

        df = self.cost_dataframe.iloc[starting_index:stoping_index, ]
        total_costs = df.iloc[0, 2]
        labour_costs = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:, 2]

        confectionery = CostsUnitContainer('Rozbiór', total=total_costs, labour=labour_costs)
        return confectionery

    def __provide_washing(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['MYCIE ZAKłADU']
        stoping_index = indexes['WARSZTAT']

        df = self.cost_dataframe.iloc[starting_index:stoping_index, ]
        total_costs = df.iloc[0, 2]
        labour_costs = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:, 2]
        washing = CostsUnitContainer('Rozbiór', total=total_costs, labour=labour_costs)

        return washing

    def __provide_workshop(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['WARSZTAT']
        stoping_index = indexes['PUNKTY SPRZEDAżY']

        df = self.cost_dataframe.iloc[starting_index:stoping_index, ]
        total_costs = df.iloc[0, 2]
        labour_costs = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:, 2]

        workshop = CostsUnitContainer('Warsztat', total=total_costs, labour=labour_costs)

        return workshop

    def __provide_shops(self):
        pass

    def __provide_transport_costs(self):
        pass

    def __provide_invoicing(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['FAKTUROWANIE']
        stoping_index = indexes['ADMINISTRACJA']

        df = self.cost_dataframe.iloc[starting_index:stoping_index, ]
        total_costs = df.iloc[0, 2]
        labour_costs = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:, 2]
        invoicing = CostsUnitContainer('Fakturowanie', total = total_costs, labour = labour_costs)

        return invoicing

    def __provide_administration(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['ADMINISTRACJA']
        stoping_index = indexes['KOSZTY SPRZEDAżY']

        df = self.cost_dataframe.iloc[starting_index:stoping_index, ]
        total_costs = df.iloc[0, 2]
        labour_costs = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:, 2]
        administration = CostsUnitContainer('Administracja', total = total_costs, labour = labour_costs)

        return administration

    def __provide_trays(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['KOSZTY SPRZEDAżY']
        stoping_index = indexes['KOSZTY OGÓLNE']

        df = self.cost_dataframe.iloc[starting_index:stoping_index, ]
        total_costs = df.iloc[0, 2]
        labour_costs = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:, 2]
        trays = CostsUnitContainer('Tacki', total=total_costs, labour=labour_costs)

        return trays

    def __provide_general_costs(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['KOSZTY OGÓLNE']
        stoping_index = indexes['ZAKłAD KARNY']

        df = self.cost_dataframe.iloc[starting_index:stoping_index, ]
        total_costs = df.iloc[0, 2]
        labour_costs = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:, 2]
        general_costs = CostsUnitContainer('Koszty ogólne', total=total_costs, labour=labour_costs)

        return general_costs

    def __provide_jail(self):
        indexes = self.__provide_costs_categories_indexes()
        starting_index = indexes['ZAKłAD KARNY']

        df = self.cost_dataframe.iloc[starting_index:, ]
        total_costs = df.iloc[0, 2]
        labour_costs = df[df['KATEGORIA'] == 'KOSZTY PRACY'].iloc[:, 2]
        jail = CostsUnitContainer('Jail', total=total_costs, labour=labour_costs)

        return jail

    def __provide_costs_categories_indexes(self):
        """
        Provides starting indexes of diffrent cost categories in df
        :return: dictionary {Category: Index}
        """

        df = self.cost_dataframe
        costs_categories_indexes = {df.iloc[i, 1]: i for i in
                                    df[df['KONTO'] > 500].index}

        return costs_categories_indexes
