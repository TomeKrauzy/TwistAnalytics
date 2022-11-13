import json


def provide_products_name():
    with open('/Users/tomaszkrauzy/Desktop/DataForTwistAnalytics/towary.txt') as f:
        products_names = {int(k): v for k, v in json.load(f).items()}
    return products_names


def provide_stores():
    with open('/Users/tomaszkrauzy/Desktop/DataForTwistAnalytics/indexy_nasze_sklepy.txt') as f:
        stores = {int(k): v for k, v in json.load(f).items()}
    return stores


class ClassificationData:
    products_labels = provide_products_name()
    stores_labels = provide_stores()