from Reports.Average.AverageSalesPricesReportScope import AverageSalesPricesReportScope as Scope

class AverageSalesPricesReportGenerator():

    def __init__(self, sales_dataframe, stores_dataframe):
        self.sales_dataframe = sales_dataframe
        self.stores_dataframe = stores_dataframe

    def generate(self, enum):
        if enum == Scope.ALL:
            return self.__create_all_report()
        elif enum == Scope.WHOLESALE:
            return self.__create_wholesales_report()
        elif enum == Scope.STORES:
            return self.__create_shops_report()
        else:
            raise ValueError('Unknown scope')

    def __create_wholesales_report(self):
        df = self.sales_dataframe

        # bez naszych sklepów i TWIST SK(4674), TWIST CZ (4570)
        wholesale = df[~df['KOD_KONTR'].isin([self.stores_dataframe, 4674, 4570])]
        wholesale = wholesale.groupby('TOWAR').agg({'ILOSC': 'sum', 'WARTOSC': 'sum'})
        wholesale['ŚR_CENA'] = wholesale['WARTOSC'] / wholesale['ILOSC']
        wholesale = wholesale.sort_values('ŚR_CENA', ascending=False)[['ILOSC', 'ŚR_CENA']]

        return wholesale

    def __create_all_report(self):
        df = self.sales_dataframe
        sales_valume = df.groupby('TOWAR').agg({'ILOSC': 'sum'}).sort_values('ILOSC', ascending=False)
        return sales_valume

    def __create_shops_report(self):
        df = self.sales_dataframe
        stores_sales = df[df['KOD_KONTR'].isin(self.stores_dataframe)]
        stores_sales = stores_sales.groupby('TOWAR').agg({'ILOSC': 'sum', 'WARTOSC': 'sum'})

        print(stores_sales['ILOSC'])
        stores_sales['ŚR_CENA'] = stores_sales['WARTOSC'] / stores_sales['ILOSC']
        stores_sales = stores_sales.sort_values('ŚR_CENA', ascending=False)[['ILOSC', 'ŚR_CENA']]

        return stores_sales
