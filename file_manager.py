# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Sep 20, 2026
Algorithm:
Class: Python Teams online class
Inputs: Customer and Product objects, the names of the text files
Processing: writing one record per line with the tab character as separator,
reading the records back and instantiating the objects again
Outputs: customers.txt, products.txt, lists of Customer and Product objects
"""
from person_template import Customer
from product_template import Product, Bouquet, PottedPlant

CUSTOMER_FILE = 'customers.txt'
PRODUCT_FILE = 'products.txt'


# Returning function: writes one customer at the end of the file
def save_customer(myCustomer, file_name=CUSTOMER_FILE):
    customer_file = open(file_name, 'a')
    customer_file.write(str(myCustomer.getPersonId()) + '\t' + myCustomer.getLastName() + '\t'
                        + myCustomer.getFirstName() + '\t' + myCustomer.getAddress() + '\t'
                        + myCustomer.getPhone() + '\t' + myCustomer.getEmail() + '\t'
                        + myCustomer.getDeliveryAddress() + '\n')
    customer_file.close()
    return True


# Returning function: writes the whole list and replaces the file
def save_customers(customer_list, file_name=CUSTOMER_FILE):
    customer_file = open(file_name, 'w')
    for myCustomer in customer_list:
        customer_file.write(str(myCustomer.getPersonId()) + '\t' + myCustomer.getLastName() + '\t'
                            + myCustomer.getFirstName() + '\t' + myCustomer.getAddress() + '\t'
                            + myCustomer.getPhone() + '\t' + myCustomer.getEmail() + '\t'
                            + myCustomer.getDeliveryAddress() + '\n')
    customer_file.close()
    return len(customer_list)


# Returning function: reads the file and instantiates one Customer object per record
def load_customers(file_name=CUSTOMER_FILE):
    customer_list = []
    try:
        customer_file = open(file_name, 'r')
    except FileNotFoundError:
        return customer_list

    for line in customer_file:
        record = line.rstrip('\n').split('\t')
        if len(record) == 7:
            myCustomer = Customer(int(record[0]), record[1], record[2], record[3],
                                  record[4], record[5], record[6])
            customer_list.append(myCustomer)
    customer_file.close()
    return customer_list


# Returning function: the identifier of the next customer to register
def next_customer_id(customer_list):
    if len(customer_list) == 0:
        return 1001
    last_id = 0
    for myCustomer in customer_list:
        if myCustomer.getPersonId() > last_id:
            last_id = myCustomer.getPersonId()
    return last_id + 1


# Returning function: writes the catalog and replaces the file
def save_products(product_list, file_name=PRODUCT_FILE):
    product_file = open(file_name, 'w')
    for myProduct in product_list:
        # getProductType() and getExtraInfo() are overridden in the child classes
        product_file.write(myProduct.getProductCode() + '\t' + myProduct.getProductName() + '\t'
                           + myProduct.getCategory() + '\t' + str(myProduct.getUnitPrice()) + '\t'
                           + str(myProduct.getStockQty()) + '\t' + myProduct.getProductType() + '\t'
                           + myProduct.getExtraInfo() + '\n')
    product_file.close()
    return len(product_list)


# Returning function: reads the catalog and instantiates the matching child class
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

