# create an interactive Python program -> this is a Python comment
# Author: Luis Gerardo Molina
"""
Date: Sep 20, 2026
Algorithm:
Class: Python Teams online class
Inputs: customer records for myCustomer1 to myCustomer3, end-user input for myCustomer4,
catalog records for myProduct1 to myProduct5, one Staff object
Processing: constructors and setter methods, format_phone() applied by setPhone(),
getRole() and calculateDisplayPrice()
applied to objects of different classes (polymorphism), file_manager functions
Outputs: printed customer and catalog information, customers.txt, products.txt,
the records read back from both files
"""
import person_template
from person_template import Person, Customer, Staff
from product_template import Product, Bouquet, PottedPlant
import file_manager


def main():
    print('Flower Shop Project: instantiate objects from the Person and Product classes')

    # Instantiate objects from the Customer class using the constructor with parameters
    myCustomer1 = Customer(1001, 'Tremblay', 'Marie', '450 Rue Sherbrooke, Montreal, QC H2X 1Y4',
                           '514-555-0142', 'marie.tremblay@gmail.com',
                           '1200 Rue Saint-Denis, Montreal, QC H1M 2P8')
    myCustomer2 = Customer(1002, 'Nguyen', 'Bao', '78 Avenue du Parc, Montreal, QC H2X 1V6',
                           '5145550177', 'bao.nguyen@gmail.com',
                           '78 Avenue du Parc, Montreal, QC H2X 1V6')
    myCustomer3 = Customer(1003, 'Silva', 'Paulo', '300 Boulevard Saint-Laurent, Montreal, QC H3H 1A1',
                           '(438) 555 0109', 'paulo.silva@gmail.com',
                           '55 Rue Rachel, Montreal, QC H1E 7C8')

    print('\nThe data attributes of customer 1:')
    myCustomer1.printPersonInfo()
    print('\nThe data attributes of customer 2:')
    myCustomer2.printPersonInfo()
    print('\nThe data attributes of customer 3:')
    myCustomer3.printPersonInfo()

    # Setting new data attributes for myCustomer4 using the setter methods
    print('\nSet data attributes for customer 4')
    myCustomer4 = Customer()

    newLastName = input('Please enter the customer last name: ')
    newFirstName = input('Please enter the customer first name: ')
    newAddress = input('Please enter the customer address: ')
    newPhone = input('Please enter the customer phone: ')
    newEmail = input('Please enter the customer email: ')
    newDeliveryAddress = input('Please enter the delivery address: ')

    myCustomer4.setPersonId(1004)
    myCustomer4.setLastName(newLastName)
    myCustomer4.setFirstName(newFirstName)
    myCustomer4.setAddress(newAddress)
    myCustomer4.setPhone(newPhone)
    myCustomer4.setEmail(newEmail)
    myCustomer4.setDeliveryAddress(newDeliveryAddress)

    print('The data attributes for customer 4 after entered by end user:')
    myCustomer4.printPersonInfo()

    print('The data attributes for customer 4 by invoking the getter methods:')
    print(myCustomer4.getPersonId(), '-', myCustomer4.getFullName(), '-',
          myCustomer4.getPhone(), '-', myCustomer4.getEmail())

    # Instantiate one object from the Staff child class
    myStaff1 = Staff(2001, 'Gagnon', 'Lucie', '12 Rue Ontario, Montreal, QC H2L 1N8',
                     '514-555-0188', 'lucie.gagnon@flowershop.com', 'Counter clerk')
    print('\nThe data attributes of the staff object from the child class Staff:')
    myStaff1.printPersonInfo()

    # apply Polymorphism: same method call on objects of different classes
    print('\nApply Polymorphism on the Person hierarchy')
    myPerson1 = Person(3001, 'Person', 'Generic', 'No address', '0000000000', 'none@email.com')
    for myPerson in [myPerson1, myCustomer1, myStaff1]:
        print('The role of', myPerson.getFullName(), 'is', myPerson.getRole())

    # Store the customers into customers.txt
    print('\nStore the customer objects into customers.txt')
    customer_list = [myCustomer1, myCustomer2, myCustomer3, myCustomer4]
    total_saved = file_manager.save_customers(customer_list)
    print('Number of customer records written:', total_saved)

    # Instantiate objects from the Product class and from its child classes
    print('\nInstantiate the catalog objects')
    myProduct1 = Bouquet('B001', 'Red rose bouquet', 'Bouquets', 45.00, 12, 12)
    myProduct2 = Bouquet('B002', 'Spring mixed bouquet', 'Bouquets', 38.50, 7, 15)
    myProduct3 = PottedPlant('P001', 'Orchid in ceramic pot', 'Potted plants', 52.00, 4, '15 cm')
    myProduct4 = PottedPlant('P002', 'Small succulent', 'Potted plants', 14.75, 0, '8 cm')
    myProduct5 = Product('O001', 'Sympathy arrangement', 'Occasions', 75.00, 3)

    product_list = [myProduct1, myProduct2, myProduct3, myProduct4, myProduct5]

    for myProduct in product_list:
        print('\nThe data attributes of the catalog item:')
        myProduct.printProductInfo()
        print(f'Display price: {myProduct.calculateDisplayPrice():.2f} $ // '
              f'stock value: {myProduct.calculateStockValue():.2f} $ // '
              f'available: {myProduct.isAvailable()}')

    # Store the catalog into products.txt
    print('\nStore the catalog objects into products.txt')
    total_saved = file_manager.save_products(product_list)
    print('Number of catalog records written:', total_saved)

    # Read both files back and instantiate the objects again
    print('\nRead customers.txt and instantiate the Customer objects again')
    for myCustomer in file_manager.load_customers():
        myCustomer.printPersonInfo()

    print('\nA phone number is accepted in several formats and stored in one:')
    for typed_phone in ['514-555-0142', '5145550177', '(438) 555 0109', '1 514 341 7845']:
        print(typed_phone, '->', person_template.format_phone(typed_phone))

    print('\nThe identifier of the next customer to register is',
          file_manager.next_customer_id(file_manager.load_customers()))

    print('\nRead products.txt and instantiate the catalog objects again')
    for myProduct in file_manager.load_products():
        print(myProduct.getProductCode(), '//', myProduct.getProductName(), '//',
              myProduct.getCategory(), '//',
              f'{myProduct.calculateDisplayPrice():.2f} $')


main()

