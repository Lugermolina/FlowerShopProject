# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Oct 10, 2026
Algorithm:
Class: Python Teams online class
Inputs: order_id, customer_id, staff_id, order_date, delivery_date, order_type,
delivery_address, order_status, payment_status, product_code, product_name, quantity,
unit_price, extra_charge
Processing: getter and setter methods, calculateLineTotal() for each item,
calculateSubtotal() over the list of items of the order
Outputs: printed order information through printOrderInfo() and printItemInfo()
"""

# the steps an order goes through
ORDER_PICKUP = 'Pickup'
ORDER_DELIVERY = 'Delivery'

STATUS_NEW = 'New'
STATUS_READY = 'Ready'
STATUS_COMPLETED = 'Completed'

PAYMENT_UNPAID = 'Unpaid'
PAYMENT_PAID = 'Paid'


class Order:
    def __init__(self, order_id=None, customer_id=None, staff_id=None, order_date=None,
                 delivery_date=None, order_type=ORDER_PICKUP, delivery_address='',
                 order_status=STATUS_NEW, payment_status=PAYMENT_UNPAID):
        self.__order_id = order_id
        self.__customer_id = customer_id
        self.__staff_id = staff_id
        self.__order_date = order_date
        self.__delivery_date = delivery_date
        self.__order_type = order_type
        # the order keeps its own copy of the address, so a customer who moves
        # later does not change where a past order was delivered
        self.__delivery_address = delivery_address
        self.__order_status = order_status
        self.__payment_status = payment_status
        # the lines of the order, stored apart in order_items.txt
        self.__item_list = []

    def getOrderId(self):
        return self.__order_id

    def getCustomerId(self):
        return self.__customer_id

    def getStaffId(self):
        return self.__staff_id

    def getOrderDate(self):
        return self.__order_date

    def getDeliveryDate(self):
        return self.__delivery_date

    def getOrderType(self):
        return self.__order_type

    def getDeliveryAddress(self):
        return self.__delivery_address

    def getOrderStatus(self):
        return self.__order_status

    def getPaymentStatus(self):
        return self.__payment_status

    def getItemList(self):
        return self.__item_list

    def setOrderId(self, order_id):
        self.__order_id = order_id

    def setCustomerId(self, customer_id):
        self.__customer_id = customer_id

    def setStaffId(self, staff_id):
        self.__staff_id = staff_id

    def setOrderDate(self, order_date):
        self.__order_date = order_date

    def setDeliveryDate(self, delivery_date):
        self.__delivery_date = delivery_date

    def setOrderType(self, order_type):
        self.__order_type = order_type

    def setDeliveryAddress(self, delivery_address):
        self.__delivery_address = delivery_address

    def setOrderStatus(self, order_status):
        self.__order_status = order_status

    def setPaymentStatus(self, payment_status):
        self.__payment_status = payment_status

    def setItemList(self, item_list):
        self.__item_list = item_list

    def addItem(self, myItem):
        self.__item_list.append(myItem)

    def isDelivery(self):
        return self.getOrderType() == ORDER_DELIVERY

    # an order stays active until it is completed and paid; a customer
    # with an active order cannot be deleted
    def isActive(self):
        return not (self.getOrderStatus() == STATUS_COMPLETED
                    and self.getPaymentStatus() == PAYMENT_PAID)

    def calculateSubtotal(self):
        subtotal = 0.0
        for myItem in self.getItemList():
            subtotal = subtotal + myItem.calculateLineTotal()
        return subtotal

    def printOrderInfo(self):
        print(self.getOrderId(), '//', self.getCustomerId(), '//', self.getStaffId(), '//',
              self.getOrderDate(), '//', self.getDeliveryDate(), '//', self.getOrderType(),
              '//', self.getDeliveryAddress(), '//', self.getOrderStatus(), '//',
              self.getPaymentStatus())


# one line of an order, one line in order_items.txt
class OrderItem:
    def __init__(self, order_id=None, product_code=None, product_name=None, quantity=None,
                 unit_price=None, extra_charge=None):
        self.__order_id = order_id
        self.__product_code = product_code
        # the name and the prices are copied at the moment of the sale, so a later
        # change in the catalog does not rewrite an old order or its bill
        self.__product_name = product_name
        self.__quantity = quantity
        self.__unit_price = unit_price
        self.__extra_charge = extra_charge

    def getOrderId(self):
        return self.__order_id

    def getProductCode(self):
        return self.__product_code

    def getProductName(self):
        return self.__product_name

    def getQuantity(self):
        return self.__quantity

    def getUnitPrice(self):
        return self.__unit_price

    def getExtraCharge(self):
        return self.__extra_charge

    def setOrderId(self, order_id):
        self.__order_id = order_id

    def setProductCode(self, product_code):
        self.__product_code = product_code

    def setProductName(self, product_name):
        self.__product_name = product_name

    def setQuantity(self, quantity):
        self.__quantity = quantity

    def setUnitPrice(self, unit_price):
        self.__unit_price = unit_price

    def setExtraCharge(self, extra_charge):
        self.__extra_charge = extra_charge

    def calculatePriceToPay(self):
        return self.getUnitPrice() + self.getExtraCharge()

    def calculateLineTotal(self):
        return self.getQuantity() * self.calculatePriceToPay()

    def printItemInfo(self):
        print(self.getOrderId(), '//', self.getProductCode(), '//', self.getProductName(),
              '//', self.getQuantity(), '//', format(self.calculatePriceToPay(), '.2f'), '//',
              format(self.calculateLineTotal(), '.2f'))
