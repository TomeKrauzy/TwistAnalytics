
class AverageLifestockPriceGenerator:

    def __init__(self, lifestock_dataframe):
        self.lifestock_dataframe = lifestock_dataframe


    def provide_avg_lifestock_purchuse_price(self):
        return self.__create_average_lifestock_price()

    def __create_average_lifestock_price(self):
        df = self.lifestock_dataframe
        avg_price = df['WARTOSC'].sum() / df['ILOSC'].sum()
        return avg_price






