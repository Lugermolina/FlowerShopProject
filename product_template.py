# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Sep 20, 2026
Algorithm:
Class: Python Teams online class
Inputs: product_code, product_name, category, unit_price, stock_qty, flower_count, pot_size
Processing: getter and setter methods, getExtraCharge() overridden in the child classes
and called by calculateDisplayPrice(), isAvailable() and calculateStockValue()
Outputs: printed catalog information through printProductInfo()
"""

WRAPPING_FEE = 5.00
POT_FEE = 3.50


# Super/parent class
class Product:
    def __init__(self, product_code=None, product_name=None, category=None,
                 unit_price=None, stock_qty=None):
        self.__product_code = product_code
        self.__product_name = product_name
        self.__category = category
        self.__unit_price = unit_price
        self.__stock_qty = stock_qty

    # accessor (getter) methods
    def getProductCode(self):
        return self.__product_code

    def getProductName(self):
        return self.__product_name

    def getCategory(self):
        return self.__category

    def getUnitPrice(self):
        return self.__unit_price

    def getStockQty(self):
        return self.__stock_qty

    # mutator (setter) methods
    def setProductCode(self, product_code):
        self.__product_code = product_code

    def setProductName(self, product_name):
        self.__product_name = product_name

    def setCategory(self, category):
        self.__category = category

    def setUnitPrice(self, unit_price):
        self.__unit_price = unit_price

    def setStockQty(self, stock_qty):
        self.__stock_qty = stock_qty

    # concrete methods
    def calculateDisplayPrice(self):
        return self.getUnitPrice() + self.getExtraCharge()

    def getExtraCharge(self):
        return 0.0

    def calculateStockValue(self):
        return self.getUnitPrice() * self.getStockQty()

    def isAvailable(self):
        return self.getStockQty() > 0

    def getProductType(self):
        return 'Product'

    def getExtraInfo(self):
        return '0'

    def printProductInfo(self):
        print(self.getProductCode(), '//', self.getProductName(), '//', self.getCategory(),
              '//', self.getUnitPrice(), '//', self.getStockQty())


# Sub/child class
class Bouquet(Product):
    def __init__(self, product_code=None, product_name=None, category=None,
                 unit_price=None, stock_qty=None, flower_count=None):
        super().__init__(product_code, product_name, category, unit_price, stock_qty)
        self.__flower_count = flower_count

    def getFlowerCount(self):
        return self.__flower_count

    def setFlowerCount(self, flower_count):
        self.__flower_count = flower_count

    # the wrapping of an arrangement is charged on top of the unit price
    def getExtraCharge(self):
        return WRAPPING_FEE

    def getProductType(self):
        return 'Bouquet'

    def getExtraInfo(self):
        return str(self.getFlowerCount())


# Sub/child class
class PottedPlant(Product):
    def __init__(self, product_code=None, product_name=None, category=None,
                 unit_price=None, stock_qty=None, pot_size=None):
        super().__init__(product_code, product_name, category, unit_price, stock_qty)
        self.__pot_size = pot_size

    def getPotSize(self):
        return self.__pot_size

    def setPotSize(self, pot_size):
        self.__pot_size = pot_size

    # the pot is charged on top of the unit price
    def getExtraCharge(self):
        return POT_FEE

    def getProductType(self):
        return 'PottedPlant'

    def getExtraInfo(self):
        return str(self.getPotSize())

