# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Oct 24, 2026 for iteration 3
Algorithm:
Class: Python Teams online class
Inputs: supplier_id, supplier_name, contact_name, phone, email, address, restock_id,
product_code, restock_date, quantity, unit_cost
Processing: getter and setter methods, format_phone() of the person_template module
applied by the constructor and by setPhone(), calculateCost() of a restock
Outputs: printed supplier and restock information through printSupplierInfo() and
printRestockInfo()
"""
from person_template import format_phone


class Supplier:
    def __init__(self, supplier_id=None, supplier_name=None, contact_name=None, phone=None,
                 email=None, address=None):
        self.__supplier_id = supplier_id
        self.__supplier_name = supplier_name
        self.__contact_name = contact_name
        self.__phone = format_phone(phone)
        self.__email = email
        self.__address = address

    # accessor (getter) methods
    def getSupplierId(self):
        return self.__supplier_id

    def getSupplierName(self):
        return self.__supplier_name

    def getContactName(self):
        return self.__contact_name

    def getPhone(self):
        return self.__phone

    def getEmail(self):
        return self.__email

    def getAddress(self):
        return self.__address

    # mutator (setter) methods
    def setSupplierId(self, supplier_id):
        self.__supplier_id = supplier_id

    def setSupplierName(self, supplier_name):
        self.__supplier_name = supplier_name

    def setContactName(self, contact_name):
        self.__contact_name = contact_name

    def setPhone(self, phone):
        self.__phone = format_phone(phone)

    def setEmail(self, email):
        self.__email = email

    def setAddress(self, address):
        self.__address = address

    def printSupplierInfo(self):
        print(self.getSupplierId(), '//', self.getSupplierName(), '//', self.getContactName(),
              '//', self.getPhone(), '//', self.getEmail(), '//', self.getAddress())


# one delivery of a product received from a supplier; the stock of the product goes up
# by the quantity received
class Restock:
    def __init__(self, restock_id=None, product_code=None, supplier_id=None,
                 restock_date=None, quantity=None, unit_cost=None):
        self.__restock_id = restock_id
        self.__product_code = product_code
        self.__supplier_id = supplier_id
        self.__restock_date = restock_date
        self.__quantity = quantity
        self.__unit_cost = unit_cost

    # accessor (getter) methods
    def getRestockId(self):
        return self.__restock_id

    def getProductCode(self):
        return self.__product_code

    def getSupplierId(self):
        return self.__supplier_id

    def getRestockDate(self):
        return self.__restock_date

    def getQuantity(self):
        return self.__quantity

    def getUnitCost(self):
        return self.__unit_cost

    # mutator (setter) methods
    def setRestockId(self, restock_id):
        self.__restock_id = restock_id

    def setProductCode(self, product_code):
        self.__product_code = product_code

    def setSupplierId(self, supplier_id):
        self.__supplier_id = supplier_id

    def setRestockDate(self, restock_date):
        self.__restock_date = restock_date

    def setQuantity(self, quantity):
        self.__quantity = quantity

    def setUnitCost(self, unit_cost):
        self.__unit_cost = unit_cost

    # concrete method
    def calculateCost(self):
        return self.getQuantity() * self.getUnitCost()

    def printRestockInfo(self):
        print(self.getRestockId(), '//', self.getProductCode(), '//', self.getSupplierId(),
              '//', self.getRestockDate(), '//', self.getQuantity(), '//',
              format(self.getUnitCost(), '.2f'), '//', format(self.calculateCost(), '.2f'))
