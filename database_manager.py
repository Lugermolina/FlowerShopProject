# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Oct 24, 2026 for iteration 3
Algorithm:
Class: Python Teams online class
Inputs: Customer, Staff, Supplier, Product, Order, OrderItem, Charge, BillDetail and
Restock objects, the tables of the MySQL database flowershopdb
Processing: CRUD operations with pymysql: INSERT a new record, SELECT the records and
instantiate the objects again, UPDATE one record, DELETE one record, totals with
GROUP BY for the analytics charts
Outputs: rows in the tables customer, staff, supplier, product, customer_order,
order_item, charge, bill_detail and restock, lists of objects of the nine classes
"""
import os

import pymysql

from person_template import Customer, Staff, ACCESS_ADMIN
from product_template import Product, Bouquet, PottedPlant
from order_template import Order, OrderItem, PAYMENT_PAID
from supplier_template import Supplier, Restock
from billing_template import (Charge, BillDetail, CHARGE_PERCENT, CHARGE_FIXED,
                              CHARGE_SUBTOTAL, CHARGE_TOTAL, CHARGE_GST, CHARGE_QST,
                              CHARGE_DELIVERY)

DATABASE_NAME = 'flowershopdb'

DEFAULT_ADMIN_USERNAME = 'admin'
DEFAULT_ADMIN_PASSWORD = 'admin123'
DEFAULT_DELIVERY_FEE = 11.00


def get_connection():
    return pymysql.connect(host='localhost', user='root', password=os.environ['XK7_VALUE'],
                           database=DATABASE_NAME, charset='utf8')


# runs a SELECT and returns all its rows
def select_rows(sql, values=None):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, values)
    rows = cursor.fetchall()
    # close the database connection to release memory
    connection.close()
    return rows


# runs one INSERT, UPDATE or DELETE and returns the number of rows changed
def execute_command(sql, values):
    connection = get_connection()
    cursor = connection.cursor()
    row_count = cursor.execute(sql, values)
    connection.commit()
    connection.close()
    return row_count


# a DATE column comes back as a date object, the classes keep the text YYYY-MM-DD
def date_text(value):
    if value is None:
        return ''
    return str(value)


# ---------- customer table ----------

def customer_from_row(row):
    return Customer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])


def save_customer(myCustomer):
    execute_command('INSERT INTO customer (customer_id, last_name, first_name, address, phone, '
                    'email, delivery_address, customer_status) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                    (myCustomer.getPersonId(), myCustomer.getLastName(),
                     myCustomer.getFirstName(), myCustomer.getAddress(), myCustomer.getPhone(),
                     myCustomer.getEmail(), myCustomer.getDeliveryAddress(),
                     myCustomer.getStatus()))
    return True


def update_customer(myCustomer):
    row_count = execute_command('UPDATE customer SET last_name = %s, first_name = %s, '
                                'address = %s, phone = %s, email = %s, delivery_address = %s, '
                                'customer_status = %s WHERE customer_id = %s',
                                (myCustomer.getLastName(), myCustomer.getFirstName(),
                                 myCustomer.getAddress(), myCustomer.getPhone(),
                                 myCustomer.getEmail(), myCustomer.getDeliveryAddress(),
                                 myCustomer.getStatus(), myCustomer.getPersonId()))
    return row_count


def delete_customer(customer_id):
    return execute_command('DELETE FROM customer WHERE customer_id = %s', (customer_id,))


def load_customers():
    customer_list = []
    for row in select_rows('SELECT * FROM customer ORDER BY customer_id'):
        customer_list.append(customer_from_row(row))
    return customer_list


def find_customer(person_id):
    rows = select_rows('SELECT * FROM customer WHERE customer_id = %s', (person_id,))
    if len(rows) == 0:
        return None
    return customer_from_row(rows[0])


def find_customer_by_email(email):
    rows = select_rows('SELECT * FROM customer WHERE LOWER(email) = LOWER(%s)', (email,))
    if len(rows) == 0:
        return None
    return customer_from_row(rows[0])


def next_customer_id():
    rows = select_rows('SELECT MAX(customer_id) FROM customer')
    if rows[0][0] is None:
        return 1001
    return rows[0][0] + 1


# ---------- product table ----------

# the product type decides which child class is instantiated
def product_from_row(row):
    if row[5] == 'Bouquet':
        return Bouquet(row[0], row[1], row[2], float(row[3]), int(row[4]), int(row[6]))
    if row[5] == 'PottedPlant':
        return PottedPlant(row[0], row[1], row[2], float(row[3]), int(row[4]), row[6])
    return Product(row[0], row[1], row[2], float(row[3]), int(row[4]))


def save_product(myProduct):
    # getProductType() and getExtraInfo() are overridden in the child classes
    execute_command('INSERT INTO product (product_code, product_name, category, unit_price, '
                    'stock_qty, product_type, extra_info) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (myProduct.getProductCode(), myProduct.getProductName(),
                     myProduct.getCategory(), myProduct.getUnitPrice(),
                     myProduct.getStockQty(), myProduct.getProductType(),
                     myProduct.getExtraInfo()))
    return True


def update_product(myProduct):
    row_count = execute_command('UPDATE product SET product_name = %s, category = %s, '
                                'unit_price = %s, stock_qty = %s, product_type = %s, '
                                'extra_info = %s WHERE product_code = %s',
                                (myProduct.getProductName(), myProduct.getCategory(),
                                 myProduct.getUnitPrice(), myProduct.getStockQty(),
                                 myProduct.getProductType(), myProduct.getExtraInfo(),
                                 myProduct.getProductCode()))
    return row_count


def delete_product(product_code):
    return execute_command('DELETE FROM product WHERE product_code = %s', (product_code,))


def load_products():
    product_list = []
    for row in select_rows('SELECT product_code, product_name, category, unit_price, stock_qty, '
                           'product_type, extra_info FROM product ORDER BY product_code'):
        product_list.append(product_from_row(row))
    return product_list


def find_product(product_code):
    rows = select_rows('SELECT product_code, product_name, category, unit_price, stock_qty, '
                       'product_type, extra_info FROM product WHERE product_code = %s',
                       (product_code,))
    if len(rows) == 0:
        return None
    return product_from_row(rows[0])


# the code of a new catalog item: the letter of its type followed by the next number
# of that letter, for example B004 after B003
def next_product_code(code_letter):
    last_number = 0
    rows = select_rows('SELECT product_code FROM product WHERE product_code LIKE %s',
                       (code_letter + '%',))
    for row in rows:
        if row[0][1:].isdigit() and int(row[0][1:]) > last_number:
            last_number = int(row[0][1:])
    return code_letter + format(last_number + 1, '03d')


# ---------- staff table ----------

def staff_from_row(row):
    return Staff(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])


def save_staff(myStaff):
    execute_command('INSERT INTO staff (staff_id, last_name, first_name, address, phone, email, '
                    'position, username, password_hash, access_level) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (myStaff.getPersonId(), myStaff.getLastName(), myStaff.getFirstName(),
                     myStaff.getAddress(), myStaff.getPhone(), myStaff.getEmail(),
                     myStaff.getPosition(), myStaff.getUsername(), myStaff.getPasswordHash(),
                     myStaff.getAccessLevel()))
    return True


def update_staff(myStaff):
    row_count = execute_command('UPDATE staff SET last_name = %s, first_name = %s, address = %s, '
                                'phone = %s, email = %s, position = %s, username = %s, '
                                'password_hash = %s, access_level = %s WHERE staff_id = %s',
                                (myStaff.getLastName(), myStaff.getFirstName(),
                                 myStaff.getAddress(), myStaff.getPhone(), myStaff.getEmail(),
                                 myStaff.getPosition(), myStaff.getUsername(),
                                 myStaff.getPasswordHash(), myStaff.getAccessLevel(),
                                 myStaff.getPersonId()))
    return row_count


def delete_staff(staff_id):
    return execute_command('DELETE FROM staff WHERE staff_id = %s', (staff_id,))


def load_staff():
    staff_list = []
    for row in select_rows('SELECT * FROM staff ORDER BY staff_id'):
        staff_list.append(staff_from_row(row))
    return staff_list


def find_staff(person_id):
    rows = select_rows('SELECT * FROM staff WHERE staff_id = %s', (person_id,))
    if len(rows) == 0:
        return None
    return staff_from_row(rows[0])


def find_staff_by_username(username):
    rows = select_rows('SELECT * FROM staff WHERE username = %s', (username,))
    if len(rows) == 0:
        return None
    return staff_from_row(rows[0])


def next_staff_id():
    rows = select_rows('SELECT MAX(staff_id) FROM staff')
    if rows[0][0] is None:
        return 2001
    return rows[0][0] + 1


# ---------- supplier table ----------

def supplier_from_row(row):
    return Supplier(row[0], row[1], row[2], row[3], row[4], row[5])


def save_supplier(mySupplier):
    execute_command('INSERT INTO supplier (supplier_id, supplier_name, contact_name, phone, '
                    'email, address) VALUES (%s, %s, %s, %s, %s, %s)',
                    (mySupplier.getSupplierId(), mySupplier.getSupplierName(),
                     mySupplier.getContactName(), mySupplier.getPhone(), mySupplier.getEmail(),
                     mySupplier.getAddress()))
    return True


def update_supplier(mySupplier):
    return execute_command('UPDATE supplier SET supplier_name = %s, contact_name = %s, '
                           'phone = %s, email = %s, address = %s WHERE supplier_id = %s',
                           (mySupplier.getSupplierName(), mySupplier.getContactName(),
                            mySupplier.getPhone(), mySupplier.getEmail(),
                            mySupplier.getAddress(), mySupplier.getSupplierId()))


def delete_supplier(supplier_id):
    return execute_command('DELETE FROM supplier WHERE supplier_id = %s', (supplier_id,))


def load_suppliers():
    supplier_list = []
    for row in select_rows('SELECT * FROM supplier ORDER BY supplier_id'):
        supplier_list.append(supplier_from_row(row))
    return supplier_list


def find_supplier(supplier_id):
    rows = select_rows('SELECT * FROM supplier WHERE supplier_id = %s', (supplier_id,))
    if len(rows) == 0:
        return None
    return supplier_from_row(rows[0])


def next_supplier_id():
    rows = select_rows('SELECT MAX(supplier_id) FROM supplier')
    if rows[0][0] is None:
        return 3001
    return rows[0][0] + 1


# ---------- customer_order and order_item tables ----------

def order_values(myOrder):
    return (myOrder.getCustomerId(), myOrder.getStaffId(), myOrder.getOrderDate(),
            myOrder.getDeliveryDate(), myOrder.getOrderType(), myOrder.getDeliveryAddress(),
            myOrder.getOrderStatus(), myOrder.getPaymentStatus(), myOrder.getOrderId())


def insert_order_items(cursor, myOrder):
    for myItem in myOrder.getItemList():
        cursor.execute('INSERT INTO order_item (order_id, product_code, product_name, quantity, '
                       'unit_price, extra_charge) VALUES (%s, %s, %s, %s, %s, %s)',
                       (myItem.getOrderId(), myItem.getProductCode(), myItem.getProductName(),
                        myItem.getQuantity(), myItem.getUnitPrice(), myItem.getExtraCharge()))


# the order and its lines are written with one commit: if a command fails before it,
# the connection closes without commit and the database keeps none of them
def save_order(myOrder):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO customer_order (customer_id, staff_id, order_date, delivery_date, '
                   'order_type, delivery_address, order_status, payment_status, order_id) '
                   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', order_values(myOrder))
    insert_order_items(cursor, myOrder)
    connection.commit()
    connection.close()
    return True


# the lines of the order are deleted and inserted again, with one commit
def update_order(myOrder):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('UPDATE customer_order SET customer_id = %s, staff_id = %s, order_date = %s, '
                   'delivery_date = %s, order_type = %s, delivery_address = %s, '
                   'order_status = %s, payment_status = %s WHERE order_id = %s',
                   order_values(myOrder))
    cursor.execute('DELETE FROM order_item WHERE order_id = %s', (myOrder.getOrderId(),))
    insert_order_items(cursor, myOrder)
    connection.commit()
    connection.close()
    return True


# the lines go first because order_item refers to customer_order
def delete_order(order_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM order_item WHERE order_id = %s', (order_id,))
    row_count = cursor.execute('DELETE FROM customer_order WHERE order_id = %s', (order_id,))
    connection.commit()
    connection.close()
    return row_count


def load_order_items(order_id):
    item_list = []
    for row in select_rows('SELECT order_id, product_code, product_name, quantity, unit_price, '
                           'extra_charge FROM order_item WHERE order_id = %s', (order_id,)):
        item_list.append(OrderItem(row[0], row[1], row[2], int(row[3]), float(row[4]),
                                   float(row[5])))
    return item_list


def orders_from_rows(rows):
    order_list = []
    for row in rows:
        myOrder = Order(row[0], row[1], row[2], date_text(row[3]), date_text(row[4]),
                        row[5], row[6], row[7], row[8])
        for myItem in load_order_items(myOrder.getOrderId()):
            myOrder.addItem(myItem)
        order_list.append(myOrder)
    return order_list


ORDER_COLUMNS = ('SELECT order_id, customer_id, staff_id, order_date, delivery_date, order_type, '
                 'delivery_address, order_status, payment_status FROM customer_order ')


def load_orders():
    return orders_from_rows(select_rows(ORDER_COLUMNS + 'ORDER BY order_id'))


def find_order(order_id):
    order_list = orders_from_rows(select_rows(ORDER_COLUMNS + 'WHERE order_id = %s',
                                              (order_id,)))
    if len(order_list) == 0:
        return None
    return order_list[0]


# the orders not completed yet, by pickup or delivery date, for the follow-up of the day
def load_open_orders():
    return orders_from_rows(select_rows(ORDER_COLUMNS + 'WHERE order_status <> %s '
                                        'ORDER BY delivery_date, order_id', ('Completed',)))


# only the status changes, the lines of the order stay as they are
def update_order_status(order_id, order_status):
    return execute_command('UPDATE customer_order SET order_status = %s WHERE order_id = %s',
                           (order_status, order_id))


def load_customer_orders(customer_id):
    return orders_from_rows(select_rows(ORDER_COLUMNS + 'WHERE customer_id = %s '
                                        'ORDER BY order_id', (customer_id,)))


def next_order_id():
    rows = select_rows('SELECT MAX(order_id) FROM customer_order')
    if rows[0][0] is None:
        return 5001
    return rows[0][0] + 1


# ---------- restock table ----------

def restock_from_row(row):
    return Restock(row[0], row[1], row[2], date_text(row[3]), int(row[4]), float(row[5]))


# the restock is inserted and the stock of the product goes up with one commit: if a
# command fails before it, the database keeps neither of them
def save_restock(myRestock):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO restock (restock_id, product_code, supplier_id, restock_date, '
                   'quantity, unit_cost) VALUES (%s, %s, %s, %s, %s, %s)',
                   (myRestock.getRestockId(), myRestock.getProductCode(),
                    myRestock.getSupplierId(), myRestock.getRestockDate(),
                    myRestock.getQuantity(), myRestock.getUnitCost()))
    cursor.execute('UPDATE product SET stock_qty = stock_qty + %s WHERE product_code = %s',
                   (myRestock.getQuantity(), myRestock.getProductCode()))
    connection.commit()
    connection.close()
    return True


def load_restocks():
    restock_list = []
    for row in select_rows('SELECT * FROM restock ORDER BY restock_date, restock_id'):
        restock_list.append(restock_from_row(row))
    return restock_list


def next_restock_id():
    rows = select_rows('SELECT MAX(restock_id) FROM restock')
    if rows[0][0] is None:
        return 7001
    return rows[0][0] + 1


# the number of restocks of one product; a product with restocks cannot be deleted
def count_product_restocks(product_code):
    rows = select_rows('SELECT COUNT(*) FROM restock WHERE product_code = %s', (product_code,))
    return rows[0][0]


# the number of restocks of one supplier; a supplier with restocks cannot be deleted
def count_supplier_restocks(supplier_id):
    rows = select_rows('SELECT COUNT(*) FROM restock WHERE supplier_id = %s', (supplier_id,))
    return rows[0][0]


# ---------- charge table ----------

def save_charge(myCharge):
    execute_command('INSERT INTO charge (charge_no, charge_title, charge_rate, charge_kind) '
                    'VALUES (%s, %s, %s, %s)',
                    (myCharge.getChargeNo(), myCharge.getChargeTitle(),
                     myCharge.getChargeRate(), myCharge.getChargeKind()))
    return True


def update_charge(myCharge):
    return execute_command('UPDATE charge SET charge_title = %s, charge_rate = %s, '
                           'charge_kind = %s WHERE charge_no = %s',
                           (myCharge.getChargeTitle(), myCharge.getChargeRate(),
                            myCharge.getChargeKind(), myCharge.getChargeNo()))


def delete_charge(charge_no):
    return execute_command('DELETE FROM charge WHERE charge_no = %s', (charge_no,))


def load_charges():
    charge_list = []
    for row in select_rows('SELECT * FROM charge ORDER BY charge_no'):
        charge_list.append(Charge(row[0], row[1], float(row[2]), row[3]))
    return charge_list


def find_charge(charge_no):
    rows = select_rows('SELECT * FROM charge WHERE charge_no = %s', (charge_no,))
    if len(rows) == 0:
        return None
    return Charge(rows[0][0], rows[0][1], float(rows[0][2]), rows[0][3])


# ---------- bill_detail table ----------

def save_bill_detail(myBillDetail):
    execute_command('INSERT INTO bill_detail (order_id, charge_no, base, rate, amount, '
                    'bill_month, bill_year) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (myBillDetail.getOrderId(), myBillDetail.getChargeNo(),
                     myBillDetail.getBase(), myBillDetail.getRate(), myBillDetail.getAmount(),
                     myBillDetail.getMonth(), myBillDetail.getYear()))
    return True


def bill_details_from_rows(rows):
    bill_list = []
    for row in rows:
        bill_list.append(BillDetail(row[0], row[1], float(row[2]), float(row[3]),
                                    float(row[4]), row[5], row[6]))
    return bill_list


def load_bill_details():
    return bill_details_from_rows(select_rows('SELECT * FROM bill_detail '
                                              'ORDER BY order_id, charge_no'))


# an empty list means the order was never billed; the total is moved to the last line,
# because its number 101 comes before the taxes and the fees
def load_order_bill(order_id):
    bill_list = []
    total_list = []
    for myBillDetail in bill_details_from_rows(select_rows('SELECT * FROM bill_detail '
                                                           'WHERE order_id = %s ORDER BY charge_no',
                                                           (order_id,))):
        if myBillDetail.getChargeNo() == CHARGE_TOTAL:
            total_list.append(myBillDetail)
        else:
            bill_list.append(myBillDetail)
    return bill_list + total_list


# ---------- analytics: totals calculated by MySQL with GROUP BY ----------

# new: one row per month: year, month, number of paid orders, sum of their subtotals
def load_sales_by_month():
    return select_rows('SELECT bill_year, bill_month, COUNT(*), SUM(amount) FROM bill_detail '
                       'WHERE charge_no = %s GROUP BY bill_year, bill_month '
                       'ORDER BY bill_year, bill_month', (CHARGE_SUBTOTAL,))


# new: one row per category: category, sales of the paid orders (price and extra charge);
# an item no longer in the catalog is counted under Other
def load_sales_by_category():
    return select_rows('SELECT IFNULL(product.category, %s) AS category_name, '
                       'SUM(order_item.quantity * (order_item.unit_price + order_item.extra_charge)) '
                       'FROM order_item '
                       'JOIN customer_order ON order_item.order_id = customer_order.order_id '
                       'LEFT JOIN product ON order_item.product_code = product.product_code '
                       'WHERE customer_order.payment_status = %s '
                       'GROUP BY category_name '
                       'ORDER BY SUM(order_item.quantity * (order_item.unit_price + '
                       'order_item.extra_charge)) DESC', ('Other', PAYMENT_PAID))


# new: one row per item, the highest stock first
def load_stock_levels():
    return select_rows('SELECT product_code, product_name, stock_qty FROM product '
                       'ORDER BY stock_qty DESC, product_code DESC')


# new: one row per supplier: name, number of restocks, total cost, the lowest cost first
def load_restock_cost_by_supplier():
    return select_rows('SELECT supplier.supplier_name, COUNT(*), '
                       'SUM(restock.quantity * restock.unit_cost) FROM restock '
                       'JOIN supplier ON restock.supplier_id = supplier.supplier_id '
                       'GROUP BY supplier.supplier_id, supplier.supplier_name '
                       'ORDER BY SUM(restock.quantity * restock.unit_cost)')


# called when the application starts: it creates the first admin account and the
# charges of the bill, and writes nothing when the tables already hold records
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
