# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Sep 20, 2026, updating started on Oct 10, 2026 for iteration 2
Algorithm:
Class: Python Teams online class
Inputs: Customer, Staff, Product, Order, OrderItem, Charge and BillDetail objects,
the names of the text files
Processing: writing one record per line with the tab character as separator,
reading the records back and instantiating the objects again, searching one record
by its identifier, replacing a whole file after an update or a delete
Outputs: customers.txt, staff.txt, products.txt, orders.txt, order_items.txt,
charges.txt, bill_details.txt, lists of objects of the seven classes
"""
import os

from person_template import Customer, Staff, ACCESS_ADMIN
from product_template import Product, Bouquet, PottedPlant
from order_template import Order, OrderItem
from billing_template import (Charge, BillDetail, CHARGE_PERCENT, CHARGE_FIXED,
                              CHARGE_SUBTOTAL, CHARGE_TOTAL, CHARGE_GST, CHARGE_QST,
                              CHARGE_DELIVERY)

CUSTOMER_FILE = 'customers.txt'
PRODUCT_FILE = 'products.txt'
STAFF_FILE = 'staff.txt'
ORDER_FILE = 'orders.txt'
ORDER_ITEM_FILE = 'order_items.txt'
CHARGE_FILE = 'charges.txt'
BILL_DETAIL_FILE = 'bill_details.txt'

DEFAULT_ADMIN_USERNAME = 'admin'
DEFAULT_ADMIN_PASSWORD = 'admin123'
DEFAULT_DELIVERY_FEE = 11.00


# new function to replace a whole file after an update or a delete: the records go
# to a temporary file first, so the original stays intact if the writing fails
def write_records(file_name, line_list):
    temp_name = file_name + '.tmp'
    temp_file = open(temp_name, 'w')
    for line in line_list:
        temp_file.write(line + '\n')
    temp_file.close()
    os.replace(temp_name, file_name)


def read_records(file_name):
    record_list = []
    try:
        record_file = open(file_name, 'r')
    except FileNotFoundError:
        return record_list

    for line in record_file:
        record_list.append(line.rstrip('\n').split('\t'))
    record_file.close()
    return record_list


# updated: the customer record gains an eighth field, the status
def customer_record(myCustomer):
    return (str(myCustomer.getPersonId()) + '\t' + myCustomer.getLastName() + '\t'
            + myCustomer.getFirstName() + '\t' + myCustomer.getAddress() + '\t'
            + myCustomer.getPhone() + '\t' + myCustomer.getEmail() + '\t'
            + myCustomer.getDeliveryAddress() + '\t' + myCustomer.getStatus())


# one customer at the end of the file
def save_customer(myCustomer, file_name=CUSTOMER_FILE):
    customer_file = open(file_name, 'a')
    customer_file.write(customer_record(myCustomer) + '\n')
    customer_file.close()
    return True


# to write the whole list and to replace the file
def save_customers(customer_list, file_name=CUSTOMER_FILE):
    line_list = []
    for myCustomer in customer_list:
        line_list.append(customer_record(myCustomer))
    write_records(file_name, line_list)
    return len(customer_list)


# reading the file and instantiating one Customer object per record
def load_customers(file_name=CUSTOMER_FILE):
    customer_list = []
    try:
        customer_file = open(file_name, 'r')
    except FileNotFoundError:
        return customer_list

    for line in customer_file:
        record = line.rstrip('\n').split('\t')
        # updated: a record of iteration 1 has seven fields and is read as an active customer
        if len(record) == 7:
            myCustomer = Customer(int(record[0]), record[1], record[2], record[3],
                                  record[4], record[5], record[6])
            customer_list.append(myCustomer)
        elif len(record) == 8:
            myCustomer = Customer(int(record[0]), record[1], record[2], record[3],
                                  record[4], record[5], record[6], record[7])
            customer_list.append(myCustomer)
    customer_file.close()
    return customer_list


# the identifier of the next customer to register
def next_customer_id(customer_list):
    if len(customer_list) == 0:
        return 1001
    last_id = 0
    for myCustomer in customer_list:
        if myCustomer.getPersonId() > last_id:
            last_id = myCustomer.getPersonId()
    return last_id + 1


def find_customer(person_id, file_name=CUSTOMER_FILE):
    for myCustomer in load_customers(file_name):
        if myCustomer.getPersonId() == person_id:
            return myCustomer
    return None


# new function for the duplicate email check of the customer form
def find_customer_by_email(email, file_name=CUSTOMER_FILE):
    for myCustomer in load_customers(file_name):
        if myCustomer.getEmail().lower() == email.lower():
            return myCustomer
    return None


def product_record(myProduct):
    # getProductType() and getExtraInfo() are overridden in the child classes
    return (myProduct.getProductCode() + '\t' + myProduct.getProductName() + '\t'
            + myProduct.getCategory() + '\t' + str(myProduct.getUnitPrice()) + '\t'
            + str(myProduct.getStockQty()) + '\t' + myProduct.getProductType() + '\t'
            + myProduct.getExtraInfo())


def save_product(myProduct, file_name=PRODUCT_FILE):
    product_file = open(file_name, 'a')
    product_file.write(product_record(myProduct) + '\n')
    product_file.close()
    return True


# writing the catalog and replacing the file
def save_products(product_list, file_name=PRODUCT_FILE):
    line_list = []
    for myProduct in product_list:
        line_list.append(product_record(myProduct))
    write_records(file_name, line_list)
    return len(product_list)


# reading the catalog and instantiates the matching child class
def load_products(file_name=PRODUCT_FILE):
    product_list = []
    try:
        product_file = open(file_name, 'r')
    except FileNotFoundError:
        return product_list

    for line in product_file:
        record = line.rstrip('\n').split('\t')
        if len(record) == 7:
            if record[5] == 'Bouquet':
                myProduct = Bouquet(record[0], record[1], record[2],
                                    float(record[3]), int(record[4]), int(record[6]))
            elif record[5] == 'PottedPlant':
                myProduct = PottedPlant(record[0], record[1], record[2],
                                        float(record[3]), int(record[4]), record[6])
            else:
                myProduct = Product(record[0], record[1], record[2],
                                    float(record[3]), int(record[4]))
            product_list.append(myProduct)
    product_file.close()
    return product_list


def find_product(product_code, file_name=PRODUCT_FILE):
    for myProduct in load_products(file_name):
        if myProduct.getProductCode() == product_code:
            return myProduct
    return None


# new function to generate the code of a new catalog item: the letter of its type
# followed by the next number of that letter, for example B003 after B002
def next_product_code(product_list, code_letter):
    last_number = 0
    for myProduct in product_list:
        product_code = myProduct.getProductCode()
        if product_code[0] == code_letter and product_code[1:].isdigit():
            if int(product_code[1:]) > last_number:
                last_number = int(product_code[1:])
    return code_letter + format(last_number + 1, '03d')


def staff_record(myStaff):
    return (str(myStaff.getPersonId()) + '\t' + myStaff.getLastName() + '\t'
            + myStaff.getFirstName() + '\t' + myStaff.getAddress() + '\t'
            + myStaff.getPhone() + '\t' + myStaff.getEmail() + '\t'
            + myStaff.getPosition() + '\t' + myStaff.getUsername() + '\t'
            + myStaff.getPasswordHash() + '\t' + myStaff.getAccessLevel())


def save_staff(myStaff, file_name=STAFF_FILE):
    staff_file = open(file_name, 'a')
    staff_file.write(staff_record(myStaff) + '\n')
    staff_file.close()
    return True


def save_staff_list(staff_list, file_name=STAFF_FILE):
    line_list = []
    for myStaff in staff_list:
        line_list.append(staff_record(myStaff))
    write_records(file_name, line_list)
    return len(staff_list)


def load_staff(file_name=STAFF_FILE):
    staff_list = []
    for record in read_records(file_name):
        if len(record) == 10:
            myStaff = Staff(int(record[0]), record[1], record[2], record[3], record[4],
                            record[5], record[6], record[7], record[8], record[9])
            staff_list.append(myStaff)
    return staff_list


def next_staff_id(staff_list):
    if len(staff_list) == 0:
        return 2001
    last_id = 0
    for myStaff in staff_list:
        if myStaff.getPersonId() > last_id:
            last_id = myStaff.getPersonId()
    return last_id + 1


def find_staff(person_id, file_name=STAFF_FILE):
    for myStaff in load_staff(file_name):
        if myStaff.getPersonId() == person_id:
            return myStaff
    return None


# new function for the login form: the account that owns a username, or None
def find_staff_by_username(username, file_name=STAFF_FILE):
    for myStaff in load_staff(file_name):
        if myStaff.getUsername() == username:
            return myStaff
    return None


# new: an order taken at the counter without a customer record has an empty customer field
def order_record(myOrder):
    customer_text = ''
    if myOrder.getCustomerId() is not None:
        customer_text = str(myOrder.getCustomerId())
    return (str(myOrder.getOrderId()) + '\t' + customer_text + '\t'
            + str(myOrder.getStaffId()) + '\t' + myOrder.getOrderDate() + '\t'
            + myOrder.getDeliveryDate() + '\t' + myOrder.getOrderType() + '\t'
            + myOrder.getDeliveryAddress() + '\t' + myOrder.getOrderStatus() + '\t'
            + myOrder.getPaymentStatus())


def order_item_record(myItem):
    return (str(myItem.getOrderId()) + '\t' + myItem.getProductCode() + '\t'
            + myItem.getProductName() + '\t' + str(myItem.getQuantity()) + '\t'
            + str(myItem.getUnitPrice()) + '\t' + str(myItem.getExtraCharge()))


# new function to add one order: its record goes to orders.txt and its lines to order_items.txt
def save_order(myOrder, order_file_name=ORDER_FILE, item_file_name=ORDER_ITEM_FILE):
    order_file = open(order_file_name, 'a')
    order_file.write(order_record(myOrder) + '\n')
    order_file.close()

    item_file = open(item_file_name, 'a')
    for myItem in myOrder.getItemList():
        item_file.write(order_item_record(myItem) + '\n')
    item_file.close()
    return True


# new function to replace both files after an order is updated or deleted
def save_orders(order_list, order_file_name=ORDER_FILE, item_file_name=ORDER_ITEM_FILE):
    order_line_list = []
    item_line_list = []
    for myOrder in order_list:
        order_line_list.append(order_record(myOrder))
        for myItem in myOrder.getItemList():
            item_line_list.append(order_item_record(myItem))
    write_records(order_file_name, order_line_list)
    write_records(item_file_name, item_line_list)
    return len(order_list)


def load_order_items(file_name=ORDER_ITEM_FILE):
    item_list = []
    for record in read_records(file_name):
        if len(record) == 6:
            myItem = OrderItem(int(record[0]), record[1], record[2], int(record[3]),
                               float(record[4]), float(record[5]))
            item_list.append(myItem)
    return item_list


# new function to read the orders and give each one its lines from order_items.txt
def load_orders(order_file_name=ORDER_FILE, item_file_name=ORDER_ITEM_FILE):
    order_list = []
    item_list = load_order_items(item_file_name)
    for record in read_records(order_file_name):
        if len(record) == 9:
            customer_id = None
            if record[1] != '':
                customer_id = int(record[1])
            myOrder = Order(int(record[0]), customer_id, int(record[2]), record[3],
                            record[4], record[5], record[6], record[7], record[8])
            for myItem in item_list:
                if myItem.getOrderId() == myOrder.getOrderId():
                    myOrder.addItem(myItem)
            order_list.append(myOrder)
    return order_list


def next_order_id(order_list):
    if len(order_list) == 0:
        return 5001
    last_id = 0
    for myOrder in order_list:
        if myOrder.getOrderId() > last_id:
            last_id = myOrder.getOrderId()
    return last_id + 1


def find_order(order_id, order_file_name=ORDER_FILE, item_file_name=ORDER_ITEM_FILE):
    for myOrder in load_orders(order_file_name, item_file_name):
        if myOrder.getOrderId() == order_id:
            return myOrder
    return None


# new function for the delete rule of the customer form and for the order history report
def load_customer_orders(customer_id, order_file_name=ORDER_FILE,
                         item_file_name=ORDER_ITEM_FILE):
    customer_order_list = []
    for myOrder in load_orders(order_file_name, item_file_name):
        if myOrder.getCustomerId() == customer_id:
            customer_order_list.append(myOrder)
    return customer_order_list


def charge_record(myCharge):
    return (str(myCharge.getChargeNo()) + '\t' + myCharge.getChargeTitle() + '\t'
            + str(myCharge.getChargeRate()) + '\t' + myCharge.getChargeKind())


def save_charge(myCharge, file_name=CHARGE_FILE):
    charge_file = open(file_name, 'a')
    charge_file.write(charge_record(myCharge) + '\n')
    charge_file.close()
    return True


def save_charges(charge_list, file_name=CHARGE_FILE):
    line_list = []
    for myCharge in charge_list:
        line_list.append(charge_record(myCharge))
    write_records(file_name, line_list)
    return len(charge_list)


def load_charges(file_name=CHARGE_FILE):
    charge_list = []
    for record in read_records(file_name):
        if len(record) == 4:
            myCharge = Charge(int(record[0]), record[1], float(record[2]), record[3])
            charge_list.append(myCharge)
    return charge_list


def find_charge(charge_no, file_name=CHARGE_FILE):
    for myCharge in load_charges(file_name):
        if myCharge.getChargeNo() == charge_no:
            return myCharge
    return None


def save_bill_detail(myBillDetail, file_name=BILL_DETAIL_FILE):
    bill_file = open(file_name, 'a')
    bill_file.write(str(myBillDetail.getOrderId()) + '\t' + str(myBillDetail.getChargeNo())
                    + '\t' + str(myBillDetail.getBase()) + '\t' + str(myBillDetail.getRate())
                    + '\t' + str(myBillDetail.getAmount()) + '\t'
                    + str(myBillDetail.getMonth()) + '\t' + str(myBillDetail.getYear()) + '\n')
    bill_file.close()
    return True


def load_bill_details(file_name=BILL_DETAIL_FILE):
    bill_list = []
    for record in read_records(file_name):
        if len(record) == 7:
            myBillDetail = BillDetail(int(record[0]), int(record[1]), float(record[2]),
                                      float(record[3]), float(record[4]), int(record[5]),
                                      int(record[6]))
            bill_list.append(myBillDetail)
    return bill_list


# new function to get the bill of one order: an empty list means the order was never billed
def load_order_bill(order_id, file_name=BILL_DETAIL_FILE):
    order_bill_list = []
    for myBillDetail in load_bill_details(file_name):
        if myBillDetail.getOrderId() == order_id:
            order_bill_list.append(myBillDetail)
    return order_bill_list


# new function called when the application starts: it creates the first admin account
# and the charges of the bill, and writes nothing when the files already hold records
def create_default_data():
    if len(load_staff()) == 0:
        myStaff = Staff(2001, 'Administrator', 'Shop', 'Flower Shop, Montreal, QC',
                        '514-555-0100', 'admin@flowershop.com', 'Owner',
                        DEFAULT_ADMIN_USERNAME, None, ACCESS_ADMIN)
        myStaff.setPassword(DEFAULT_ADMIN_PASSWORD)
        save_staff(myStaff)

    if len(load_charges()) == 0:
        # the subtotal and the total are stored as 100 percent of their own base
        save_charge(Charge(CHARGE_SUBTOTAL, 'Subtotal', 100.0, CHARGE_PERCENT))
        save_charge(Charge(CHARGE_GST, 'GST', 5.0, CHARGE_PERCENT))
        save_charge(Charge(CHARGE_QST, 'QST', 9.975, CHARGE_PERCENT))
        save_charge(Charge(CHARGE_DELIVERY, 'Delivery fee', DEFAULT_DELIVERY_FEE, CHARGE_FIXED))
        save_charge(Charge(CHARGE_TOTAL, 'Total', 100.0, CHARGE_PERCENT))
