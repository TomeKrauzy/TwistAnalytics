from DataSource import AnalyticsDataSource as DataSource
from Reports.Average.AverageSalesPricesReportGenerator import AverageSalesPricesReportGenerator
from Reports.Average.AverageSalesPricesReportScope import AverageSalesPricesReportScope
from Reports.Sales.SalesReportScope import SalesReportScope
from Reports.Sales.SalesReportGenerator import SalesReportGenerator
from Reports.Average.AverageLifestockPriceGenerator import AverageLifestockPriceGenerator
from LifestockPurchusePriceSplit.LifesockPurchusePriceSplitter import LifestockPurchasePriceSplitter
from CostsCategorizer.CostsCategorizer import CostsCategorizer
from TreysDepartment.TreysDepartment import *
import pandas as pd
from UnitProductionCostsCalculator.UnitProductionCostsCalculator import UnitProductionCostsCalculator
from Reports.Shops.ShopProfitabilityReportGenerator import ShopProfitabilityReportGenerator

analytics_data_source = DataSource.AnalyticsDataSource()
dataframe_container = analytics_data_source.provide_data()

average_generator = AverageSalesPricesReportGenerator(dataframe_container.sales, dataframe_container.stores)
average_lifestock_price_generator = AverageLifestockPriceGenerator(dataframe_container.lifestock)
sales_generator = SalesReportGenerator(dataframe_container.sales, dataframe_container.stores)

# Basic data for further analysis
avg_wholesale_prices = average_generator.generate(AverageSalesPricesReportScope.WHOLESALE)
avg_stores_prices = average_generator.generate(AverageSalesPricesReportScope.STORES)
all_sales_report = sales_generator.generate(SalesReportScope.ALL)
avg_lifestock_price = average_lifestock_price_generator.provide_avg_lifestock_purchuse_price()

lifestock_purchase_price_splitter = LifestockPurchasePriceSplitter(dataframe_container.production,
                                                                   avg_wholesale_prices
                                                                   , avg_lifestock_price)
costs_categorizer = CostsCategorizer(dataframe_container.costs)
costs_container = costs_categorizer.provide_data()

upc_calculator = UnitProductionCostsCalculator()

product_upc_df = upc_calculator.provide_primary_products_UPC()
product_acquisition_cost_df = lifestock_purchase_price_splitter.provide_acquisition_cost_all_products()
treys_product_acquisition_costs_df = lifestock_purchase_price_splitter.provide_acq_treys_products()

# Treys departament
treys_department = TreysDepartment(dataframe_container.sales, avg_wholesale_prices, treys_product_acquisition_costs_df)
shop_raport_generator = ShopProfitabilityReportGenerator(dataframe_container.sales, product_acquisition_cost_df)


# Shop reports
shops_reports = shop_raport_generator.generate()
writer = pd.ExcelWriter('/Users/tomaszkrauzy/Desktop/TwistRaports/10.2022/shops', engine='xlsxwriter')
shops_reports[0].to_excel(writer, sheet_name='Podsumowanie')
shops_reports[1].to_excel(writer, sheet_name='Detale')
writer.save()

# Treys reports
treys_reports = treys_department.generate_reports()
writer = pd.ExcelWriter('/Users/tomaszkrauzy/Desktop/TwistRaports/10.2022/treys', engine='xlsxwriter')
treys_reports[0].to_excel(writer, sheet_name='Podsumowanie')
treys_reports[1].to_excel(writer, sheet_name='Detale')
writer.save()
