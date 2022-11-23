import json


def provide_products_name():
    with open('/Users/tomaszkrauzy/Desktop/DataForTwistAnalytics/GeneralData/products_labels.txt') as f:
        products_names = {int(k): v for k, v in json.load(f).items()}
    return products_names


def provide_stores():
    with open('/Users/tomaszkrauzy/Desktop/DataForTwistAnalytics/GeneralData/shops_indexes.txt') as f:
        stores = {int(k): v for k, v in json.load(f).items()}
    return stores


class ClassificationData:
    products_labels = provide_products_name()
    stores_labels = provide_stores()

    product_map = {63: [1795, 13887, 13888],  # filet
                   7437: [10, 13885, 13886],  # ćwiartka
                   260: [13884],  # tuszka
                   248: [202, 13891, 13892],  # udziec
                   240: [356, 13893, 13894],  # podudzie
                   9859: [271],  # udziec T
                   12013: [14341],  # noga T
                   60: [674, 13889, 13890],  # noga
                   61: [418, 13895, 13896],  # skrzydła
                   156: [13897],  # porcja
                   74: [],  # serce
                   183: [],  # żołądek
                   }