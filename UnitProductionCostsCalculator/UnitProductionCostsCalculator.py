from Products.Products import *

class UnitProductionCostsCalculator():

    def __init__(self):
        self.yelds = ProductionParameters().products_yelds
        self.carcass = Carcass()
        self.carcass_sale = Carcass_sale()
        self.gizzards = Gizzards()
        self.liver = Liver()
        self.heart = Heart()
        self.breast = Breast()
        self.wing = Wing()
        self.quarter = Quarter()
        self.portion = Portion()


    def calculate(self):
        print(yelds)


