from DataSource import AnalyticsDataSource as DataSource
from Reports.Average.AverageSalesPricesReportGenerator import AverageSalesPricesReportGenerator
from Reports.Average.AverageSalesPricesReportScope import AverageSalesPricesReportScope

from Reports.Sales.SalesReportScope import SalesReportScope
from Reports.Sales.SalesReportGenerator import SalesReportGenerator

# tworze instancje analyticsDataSource i wywołuje metode provide, która dostarcza
# dataframe_container(zawiera wszystkie potrzebne do obliczeń dataframy)
analytics_data_source = DataSource.AnalyticsDataSource()
dataframe_container = analytics_data_source.provide()

# tworze instancje AverageSalesPricesReportGenerator, zeby móc odwoływać się do metody
# generate, gdzie wybieram zakres raportu
average_generator = AverageSalesPricesReportGenerator(dataframe_container.sales, dataframe_container.stores)

wholesale_report = average_generator.generate(AverageSalesPricesReportScope.WHOLESALE)
stores_report = average_generator.generate(AverageSalesPricesReportScope.STORES)

# tworze instancje SalesReportGenerator, zeby móc odwoływać się do metody
# generate, gdzie wybieram zakres raportu dla sprzedaży
sales_generator = SalesReportGenerator(dataframe_container.sales, dataframe_container.stores)

all_sales_report = sales_generator.generate(SalesReportScope.ALL)

print(all_sales_report)
print(wholesale_report)
print(stores_report)

print('Test commit')

