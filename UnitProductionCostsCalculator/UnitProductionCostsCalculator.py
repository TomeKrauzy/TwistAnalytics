from Products.Products import *
import pandas as pd
from CostsCategorizer.CostsCategorizer import CostsCategorizer
from DataSource.AnalyticsDataSource import AnalyticsDataSource

class UnitProductionCostsCalculator():

    """
    This class combines labour_markup and costs markup.

    External function: calculate() returns DataFrame with UnitProductionCost for all base elements

    Important information:

        labour_markup is collected from Product classes.

    """

    def __init__(self):

        self.costs_dataframe = CostsCategorizer(AnalyticsDataSource().provide_data().costs).provide_data()
        self.yelds = ProductionParameters().PRODUCTS_YELDS

    def provide_primary_products_UPC(self):
        """
        :return: pd.Series with product id as index and UPC as value
        """
        df = pd.concat([self.__provide_carcass_UPC(), self.__provide_quarter_UPC(), self.__provide_breast_UPC(),
                        self.__provide_portion_UPC(), self.__provide_wing_UPC(), self.__provide_liver_UPC(),
                        self.__provide_gizzard_UPC(), self.__provide_heart_UPC(), self.__provide_leg_UPC(),
                        self.__provide_tigh_UPC(), self.__provide_shank_UPC(), self.__provide_leg_deboned_UPC(),
                        self.__provide_tigh_deboned_UPC()])
        df = df.rename('UPC')

        return df

    def provide_treys_products_UPC(self):
        primary_products_upc_df = self.provide_primary_products_UPC()
        trays_upc = {}

        for base_product_index, trays_product in self.product_map.items():
            for product in trays_product:
                trays_upc[product] = upc.loc[base_product_index]
        df = pd.concat([pd.Series(trays_upc), upc])

        return df

    def __provide_carcass_costs_markup(self):
        slaughter_speed = ProductionParameters().SLAUGHTER_SPEED
        avg_lifestock_monthly = ProductionParameters().AVG_MONTHLY_LIFESTOCK
        carcass_yeld = self.yelds[self.yelds['TOWAR'] == 'Tuszka']['Yield']

        # Slaughter markup
        slaughter_costs = self.costs_dataframe.slaughter
        slaughter_costs_markup = (slaughter_costs.total - slaughter_costs.labour) / (avg_lifestock_monthly * carcass_yeld)

        # Invoicing markup
        invoicing_costs = self.costs_dataframe.invoicing
        invoicing_costs_markup = (invoicing_costs.total - invoicing_costs.labour) / (avg_lifestock_monthly * carcass_yeld)

        # Washing markup
        washing_costs = self.costs_dataframe.washing
        washing_costs_markup = (washing_costs.total - washing_costs.labour) / (
                    avg_lifestock_monthly * carcass_yeld)

        # Workshop markup
        workshop_costs = self.costs_dataframe.workshop
        workshop_costs_markup = (workshop_costs.total - workshop_costs.labour) / (
                avg_lifestock_monthly * carcass_yeld)

        # Administration markup
        administration_costs = self.costs_dataframe.administration
        administration_costs_markup = (administration_costs.total - administration_costs.labour) / (
                avg_lifestock_monthly * carcass_yeld)

        # General costs markup
        general_costs = self.costs_dataframe.general_costs
        general_costs_markup = (general_costs.total - general_costs.labour) / (
                avg_lifestock_monthly * carcass_yeld)

        result = general_costs_markup + administration_costs_markup + washing_costs_markup + invoicing_costs_markup + slaughter_costs_markup

        return result




    def __provide_carcass_UPC(self):
        carcass = Carcass()
        upc = carcass.labour_markup + self.__provide_carcass_costs_markup()

        return upc

    def __provide_carcass_sale_UPC(self):
        """
        Here we add costs of selling the carcass as a whole
        :return: Carcass_sale_upc
        """
        carcass_sale = Carcass_sale()
        upc = carcass_sale.labour_markup + self.__provide_carcass_costs_markup()

        return upc

    def __provide_gizzard_UPC(self):
        gizzard = Gizzard()
        upc = gizzard.labour_markup

        return upc

    def __provide_liver_UPC(self):
        liver = Liver()
        upc = liver.labour_markup

        return upc

    def __provide_heart_UPC(self):
        heart = Heart()
        upc = heart.labour_markup

        return upc

    def __provide_breast_UPC(self):
        breast = Breast()
        # .iat[0] accesses the value from Series
        upc = self.__provide_carcass_costs_markup().iat[0]/3 + breast.labour_markup

        return upc

    def __provide_wing_UPC(self):
        wing = Wing()
        upc = self.__provide_carcass_costs_markup().iat[0]/3 + wing.labour_markup

        return upc

    def __provide_quarter_UPC(self):
        quarter = Quarter()
        upc = self.__provide_carcass_costs_markup().iat[0]/3 + quarter.labour_markup

        return upc

    def __provide_portion_UPC(self):
        portion = Portion()
        upc = portion.labour_markup

        return upc

# ------------------------------------- Elements from Quarter ------------------------------------------------------
    def __provide_leg_UPC(self):
        leg = Leg()
        upc = leg.labour_markup

        return upc
    def __provide_tigh_UPC(self):
        tigh = Thigh()
        upc = tigh.labour_markup

        return upc
    def __provide_shank_UPC(self):
        shank = Shank()
        upc = shank.labour_markup

        return upc

    def __provide_leg_deboned_UPC(self):
        leg_deboned = Leg_deboned()
        upc = leg_deboned.labour_markup

        return upc

    def __provide_tigh_deboned_UPC(self):
        tigh_deboned = Tigh_deboned()
        upc = tigh_deboned.labour_markup

        return upc