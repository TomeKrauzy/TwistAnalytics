from Products.Products import *
import pandas as pd

class UnitProductionCostsCalculator():

    def __init__(self):

        self.yelds = ProductionParameters().products_yelds

    def calculate(self):
        """
        :return: pd.Series with product id as index and UPC as value
        """
        df = pd.concat([self.__provide_carcass_UPC(), self.__provide_quarter_UPC()])

        return df

    def __provide_carcass_UPC(self):
        carcass = Carcass()
        labour_markup = carcass.labour_markup

        # Here we calculate other costs for carcass

        return UPC

    def __provide_carcass_sale_UPC(self):
        """
        Here we add costs of selling the carcass as a whole
        :return: Carcass_sale_upc
        """

        return UPC

    def __provide_gizzard_UPC(self):
        gizzard = Gizzards()

        return UPC

    def __provide_liver_UPC(self):
        liver = Liver()


        return UPC

    def __provide_heart_UPC(self):
        heart = Heart()


        return UPC

    def __provide_breast_UPC(self):
        breast = Breast()


        return UPC

    def __provide_wing_UPC(self):
        wing = Wing()

        return UPC

    def __provide_quarter_UPC(self):
        quarter = Quarter()

        return UPC

    def __provide_portion_UPC(self):
        portion = Portion()


        return UPC



