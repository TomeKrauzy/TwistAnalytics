from Reports.Sales.SalesReportScope import SalesReportScope as Scope

class SalesReportGenerator():

    def __init__(self, sales_dataframe, stores_dataframe):
        self.sales_dataframe = sales_dataframe
        self.stores_dataframe = stores_dataframe

    def generate(self, enum):
        if enum == Scope.ALL:
            return self.__create_all_report()
        elif enum == Scope.STORES:
            return self.__create_shops_report()
        else:
            raise ValueError('Unknown scope')

    def __create_all_report(self):
        df = self.sales_dataframe
        all_sales = df.groupby('TOWAR').agg({'ILOSC': 'sum'}).sort_values('ILOSC', ascending=False)
        return all_sales

    def __create_shops_report(self):
        df = self.sales_dataframe
        print(df.columns
              )

        stores_sales = df[df['KOD_KONTR'].isin(self.stores_dataframe)]
        stores_sales = stores_sales.groupby('NAZ_KONTR').agg({'ILOSC': 'sum'})
        stores_sales['ŚR_CENA'] = stores_sales['WARTOSC'] / stores_sales['ILOSC']
        stores_sales = stores_sales.sort_values('ŚR_CENA', ascending=False)[['ILOSC', 'ŚR_CENA']]

        return stores_sales