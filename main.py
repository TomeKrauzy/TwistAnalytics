from DataSource import AnalyticsDataSource as DataSource
from Reports.Average.AverageSalesPricesReportGenerator import AverageSalesPricesReportGenerator
from Reports.Average.AverageSalesPricesReportScope import AverageSalesPricesReportScope

from Reports.Sales.SalesReportScope import SalesReportScope
from Reports.Sales.SalesReportGenerator import SalesReportGenerator

from Reports.Average.AverageLifestockPriceGenerator import AverageLifestockPriceGenerator

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


average_lifestock_price_generator = AverageLifestockPriceGenerator(dataframe_container.lifestock)
avg_lifestock_price = average_lifestock_price_generator.provide_avg_lifestock_purchuse_price()


from LifestockPurchusePriceSplit.LifesockPurchusePriceSplitter import LifestockPurchusePriceSplitter

lifestock_purchuse_price_splitter = LifestockPurchusePriceSplitter(dataframe_container.production, average_generator.generate(AverageSalesPricesReportScope.WHOLESALE), dataframe_container.products_yield, avg_lifestock_price)

print(lifestock_purchuse_price_splitter.split_lifestock_purchuse_price().columns)


from CostsCategorizer.CostsCategorizer import CostsCategorizer
costs_categorizer = CostsCategorizer(dataframe_container.costs)

costs_container = costs_categorizer.provide_data()

print(lifestock_purchuse_price_splitter.quarter_purchuse_price_splitter())

print(lifestock_purchuse_price_splitter.split_lifestock_purchuse_price())


