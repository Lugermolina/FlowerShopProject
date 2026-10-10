# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Oct 10, 2026
Algorithm:
Class: Python Teams online class
Inputs: charge_no, charge_title, charge_rate, charge_kind, order_id, base, rate, amount,
month, year
Processing: getter and setter methods, calculateAmount() applies the rate of a charge
to a base amount
Outputs: printed billing information through printChargeInfo() and printBillInfo()
"""

CHARGE_PERCENT = 'Percent'
CHARGE_FIXED = 'Fixed'

# the numbers of the charges the billing form looks for in charges.txt
CHARGE_SUBTOTAL = 100
CHARGE_TOTAL = 101
CHARGE_GST = 200
CHARGE_QST = 201
CHARGE_DELIVERY = 300


# one charge of the bill, one line in charges.txt
class Charge:
    def __init__(self, charge_no=None, charge_title=None, charge_rate=None,
                 charge_kind=CHARGE_PERCENT):
        self.__charge_no = charge_no
        self.__charge_title = charge_title
        self.__charge_rate = charge_rate
        self.__charge_kind = charge_kind

    def getChargeNo(self):
        return self.__charge_no

    def getChargeTitle(self):
        return self.__charge_title

    def getChargeRate(self):
        return self.__charge_rate

    def getChargeKind(self):
        return self.__charge_kind

    def setChargeNo(self, charge_no):
        self.__charge_no = charge_no

    def setChargeTitle(self, charge_title):
        self.__charge_title = charge_title

    def setChargeRate(self, charge_rate):
        self.__charge_rate = charge_rate

    def setChargeKind(self, charge_kind):
        self.__charge_kind = charge_kind

    def isPercent(self):
        return self.getChargeKind() == CHARGE_PERCENT

    # calculate what the charge adds to the bill: a percentage of the
    # base, or the fixed amount itself, rounded to the cent
    def calculateAmount(self, base):
        if self.isPercent():
            return round(base * self.getChargeRate() / 100, 2)
        return round(self.getChargeRate(), 2)

    def printChargeInfo(self):
        print(self.getChargeNo(), '//', self.getChargeTitle(), '//', self.getChargeRate(),
              '//', self.getChargeKind())


# one charge applied to one order, one line in bill_details.txt
class BillDetail:
    def __init__(self, order_id=None, charge_no=None, base=None, rate=None, amount=None,
                 month=None, year=None):
        self.__order_id = order_id
        self.__charge_no = charge_no
        # the base, the rate and the amount are kept as they were on the day of
        # the payment, so a later change in charges.txt does not rewrite a paid bill
        self.__base = base
        self.__rate = rate
        self.__amount = amount
        self.__month = month
        self.__year = year

    def getOrderId(self):
        return self.__order_id

    def getChargeNo(self):
        return self.__charge_no

    def getBase(self):
        return self.__base

    def getRate(self):
        return self.__rate

    def getAmount(self):
        return self.__amount

    def getMonth(self):
        return self.__month

    def getYear(self):
        return self.__year

    def setOrderId(self, order_id):
        self.__order_id = order_id

    def setChargeNo(self, charge_no):
        self.__charge_no = charge_no

    def setBase(self, base):
        self.__base = base

    def setRate(self, rate):
        self.__rate = rate

    def setAmount(self, amount):
        self.__amount = amount

    def setMonth(self, month):
        self.__month = month

    def setYear(self, year):
        self.__year = year

    def printBillInfo(self):
        print(self.getOrderId(), '//', self.getChargeNo(), '//', format(self.getBase(), '.2f'),
              '//', self.getRate(), '//', format(self.getAmount(), '.2f'), '//',
              self.getMonth(), '//', self.getYear())
