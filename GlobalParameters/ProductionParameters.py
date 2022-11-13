from DataSource.AnalyticsDataSource import AnalyticsDataSource
from GlobalParameters.ClassificationData import ClassificationData
import pandas as pd
import json


def provide_yelds():
    with open('/Users/tomaszkrauzy/Desktop/DataForTwistAnalytics/uzyski.txt') as f:
        products_yield = {int(k): v for k, v in json.load(f).items()}

    products_names = ClassificationData.products_labels
    products_yield_dataframe = pd.DataFrame(products_yield.values(), index=products_yield.keys(), columns=['Yield'])
    products_yield_dataframe['TOWAR'] = products_yield_dataframe.index.map(products_names)
    return products_yield_dataframe


class ProductionParameters:

    products_yields = provide_yelds()
    PRODUCTS_YELDS = AnalyticsDataSource().provide_data().products_yield
    LABOUR_HOUR_COST = 50
    AVG_LIFESTOCK_WEIGHT = 3
    # elements/hour
    CONFECIONERY_SPEED = 2760
    # lifestock/hour
    SLAUGHTER_SPEED = 3720
    # breast line speed, cone/hour
    BREAST_SPEED = 2520
    # deboning_efficiency kg/h
    TIGH_DEBONING_EFFICIENCY = 32
    LEG_DEBONING_EFFICIENCY = 32
    # avg monthly lifestock quantity
    AVG_MONTHLY_LIFESTOCK = 2000000

