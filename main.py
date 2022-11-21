from DataSource import AnalyticsDataSource as DataSource
from Reports.Average.AverageSalesPricesReportGenerator import AverageSalesPricesReportGenerator
from Reports.Average.AverageSalesPricesReportScope import AverageSalesPricesReportScope

from Reports.Sales.SalesReportScope import SalesReportScope
from Reports.Sales.SalesReportGenerator import SalesReportGenerator

from Reports.Average.AverageLifestockPriceGenerator import AverageLifestockPriceGenerator

analytics_data_source = DataSource.AnalyticsDataSource()
dataframe_container = analytics_data_source.provide_data()


average_generator = AverageSalesPricesReportGenerator(dataframe_container.sales, dataframe_container.stores)

wholesale_report = average_generator.generate(AverageSalesPricesReportScope.WHOLESALE)
stores_report = average_generator.generate(AverageSalesPricesReportScope.STORES)

sales_generator = SalesReportGenerator(dataframe_container.sales, dataframe_container.stores)
all_sales_report = sales_generator.generate(SalesReportScope.ALL)

average_lifestock_price_generator = AverageLifestockPriceGenerator(dataframe_container.lifestock)
avg_lifestock_price = average_lifestock_price_generator.provide_avg_lifestock_purchuse_price()


from LifestockPurchusePriceSplit.LifesockPurchusePriceSplitter import LifestockPurchasePriceSplitter

lifestock_purchuse_price_splitter = LifestockPurchasePriceSplitter(dataframe_container.production, average_generator.generate(AverageSalesPricesReportScope.WHOLESALE), avg_lifestock_price)




from CostsCategorizer.CostsCategorizer import CostsCategorizer
costs_categorizer = CostsCategorizer(dataframe_container.costs)

costs_container = costs_categorizer.provide_data()

print(lifestock_purchuse_price_splitter.provide_acquisition_cost_all_products())

# print(dataframe_container.products_yield)


from TreysDepartment.TreysDepartment import *
import pandas as pd
pd.set_option('display.max_columns', 7)

from UnitProductionCostsCalculator.UnitProductionCostsCalculator import UnitProductionCostsCalculator


tkw_df = UnitProductionCostsCalculator().provide_primary_products_UPC()

acquisition_costs = lifestock_purchuse_price_splitter.provide_acquisition_cost_all_products()


treys = TreysDepartment(dataframe_container.sales, wholesale_report, acquisition_costs)

treys_raport = treys.generate_report()

treys_raport.to_excel("raport_tacki_Październik.xlsx",
          sheet_name='Krauzy_Tomasz')

from Reports.Shops.ShopProfitabilityReportGenerator import ShopProfitabilityReportGenerator

shop_raport_generator = ShopProfitabilityReportGenerator(dataframe_container.sales, acquisition_costs)

shops_reports = shop_raport_generator.generate()

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('/Users/tomaszkrauzy/Desktop/RaportyTwist/shops_report', engine='xlsxwriter')

# Write each dataframe to a different worksheet.
shops_reports[0].to_excel(writer, sheet_name='Sheet1')
shops_reports[1].to_excel(writer, sheet_name='Sheet2')

# Close the Pandas Excel writer and output the Excel file.
writer.save()


acq_test = LifestockPurchasePriceSplitter(dataframe_container.production, wholesale_report, avg_lifestock_price).provide_acq_treys_products()

print(acq_test)
