# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Starting on Sep 20, 2026, updating started on Oct 10, 2026 for iteration 2
Algorithm:
Class: Python Teams online class
Inputs: customer number, last name, first name, home address, phone, email, delivery
address, state of the "same as home address" check box, the button pressed
Processing: validation of the entered values, duplicate email check, instantiation of
a Customer object, add, search, update and delete of a record through the file_manager
module, delete rule based on the orders of the customer
Outputs: the customer record added to, changed in or removed from customers.txt, the
record found displayed in the fields, a confirmation or an error message displayed
on the form
"""
import sys

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QCheckBox, QGridLayout, QHBoxLayout, QMessageBox)

import file_manager
from person_template import Customer, is_valid_phone, is_valid_email, CUSTOMER_INACTIVE


class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Flower Shop, customers')

        # new data attribute: the number of the customer displayed after a search,
        # None while the form is empty; update and delete only act on this customer
        self.loaded_customer_id = None

        self.label_title = QLabel('Customers')
        self.label_title.setStyleSheet('font-weight: bold;')
        self.label_customer_id = QLabel('Customer number:')
        self.label_status = QLabel('')
        self.label_last_name = QLabel('Last name:')
        self.label_first_name = QLabel('First name:')
        self.label_address = QLabel('Home address:')
        self.label_phone = QLabel('Phone:')
        self.label_email = QLabel('Email:')
        self.label_delivery = QLabel('Delivery address:')
        self.label_message = QLabel('')

        self.field_customer_id = QLineEdit()
        self.field_last_name = QLineEdit()
        self.field_first_name = QLineEdit()
        self.field_address = QLineEdit()
        self.field_phone = QLineEdit()
        self.field_email = QLineEdit()
        self.field_delivery = QLineEdit()

        self.field_customer_id.setPlaceholderText('type a number to search; a new customer '
                                                  'gets the number automatically')
        self.field_address.setPlaceholderText('450 Rue Sherbrooke, Montreal, QC H2X 1Y4')
        self.field_phone.setPlaceholderText('514-555-0142')
        self.field_email.setPlaceholderText('name@gmail.com')

        self.check_same_address = QCheckBox('Delivery address is the same as the home address')
        self.check_same_address.setChecked(True)
        self.field_delivery.setEnabled(False)

        self.button_register = QPushButton('Add')
        self.button_search = QPushButton('Search')
        self.button_update = QPushButton('Update')
        self.button_delete = QPushButton('Delete')
        self.button_clear = QPushButton('Clear')

        self.buildLayout()

        # connect the signal (event) to the slot (action) method of this class
        self.check_same_address.stateChanged.connect(self.sameAddressChanged)
        self.button_register.clicked.connect(self.registerCustomer)
        self.button_search.clicked.connect(self.searchCustomer)
        self.button_update.clicked.connect(self.updateCustomer)
        self.button_delete.clicked.connect(self.deleteCustomer)
        self.button_clear.clicked.connect(self.clearForm)

    def buildLayout(self):
        grid = QGridLayout()
        grid.setColumnStretch(1, 1)

        grid.addWidget(self.label_title, 0, 0, 1, 2)
        grid.addWidget(self.label_customer_id, 1, 0)
        grid.addWidget(self.field_customer_id, 1, 1)
        grid.addWidget(self.label_status, 1, 2)
        grid.addWidget(self.label_last_name, 2, 0)
        grid.addWidget(self.field_last_name, 2, 1)
        grid.addWidget(self.label_first_name, 3, 0)
        grid.addWidget(self.field_first_name, 3, 1)
        grid.addWidget(self.label_address, 4, 0)
        grid.addWidget(self.field_address, 4, 1)
        grid.addWidget(self.label_phone, 5, 0)
        grid.addWidget(self.field_phone, 5, 1)
        grid.addWidget(self.label_email, 6, 0)
        grid.addWidget(self.field_email, 6, 1)
        grid.addWidget(self.check_same_address, 7, 1)
        grid.addWidget(self.label_delivery, 8, 0)
        grid.addWidget(self.field_delivery, 8, 1)

        row_buttons = QHBoxLayout()
        row_buttons.addWidget(self.button_register)
        row_buttons.addWidget(self.button_search)
        row_buttons.addWidget(self.button_update)
        row_buttons.addWidget(self.button_delete)
        row_buttons.addWidget(self.button_clear)
        row_buttons.addStretch()

        grid.addLayout(row_buttons, 9, 1)
        grid.addWidget(self.label_message, 10, 0, 1, 3)
        grid.setRowStretch(11, 1)

        self.setLayout(grid)

    # the delivery address is typed only when it differs from the home address
    def sameAddressChanged(self):
        self.field_delivery.setEnabled(not self.check_same_address.isChecked())
        if self.check_same_address.isChecked():
            self.field_delivery.setText('')

    def showMessage(self, message, is_error):
        self.label_message.setText(message)
        if is_error:
            self.label_message.setStyleSheet('color: #B22222;')
        else:
            self.label_message.setStyleSheet('color: #1F7A40;')

    def clearFields(self):
        self.loaded_customer_id = None
        self.field_customer_id.setText('')
        self.label_status.setText('')
        self.field_last_name.setText('')
        self.field_first_name.setText('')
        self.field_address.setText('')
        self.field_phone.setText('')
        self.field_email.setText('')
        self.field_delivery.setText('')
        self.check_same_address.setChecked(True)

    def clearForm(self):
        self.clearFields()
        self.showMessage('', False)

    # updated: the reading and the validation of the fields moved here from
    # registerCustomer(), because the update needs the same checks. The method returns
    # a Customer object, or None after displaying the error
    def readCustomer(self, person_id):
        new_last_name = self.field_last_name.text().strip()
        new_first_name = self.field_first_name.text().strip()
        new_address = self.field_address.text().strip()
        new_phone = self.field_phone.text().strip()
        new_email = self.field_email.text().strip()

        if self.check_same_address.isChecked():
            new_delivery_address = new_address
        else:
            new_delivery_address = self.field_delivery.text().strip()

        # validation of the entered values
        if (new_last_name == '' or new_first_name == '' or new_address == ''
                or new_phone == '' or new_email == ''):
            self.showMessage('All the fields are required.', True)
            return None

        if new_delivery_address == '':
            self.showMessage('Enter a delivery address or check the box above.', True)
            return None

        if not is_valid_phone(new_phone):
            self.showMessage('The phone number must hold ten digits, for example 514-555-0142.', True)
            return None

        if not is_valid_email(new_email):
            self.showMessage('The email address is not valid, for example name@gmail.com.', True)
            return None

        # new: two customers cannot share an email; on an update the customer
        # themselves is not counted
        sameEmailCustomer = file_manager.find_customer_by_email(new_email)
        if sameEmailCustomer is not None and sameEmailCustomer.getPersonId() != person_id:
            self.showMessage('The email ' + new_email + ' already belongs to customer '
                             + str(sameEmailCustomer.getPersonId()) + ', '
                             + sameEmailCustomer.getFullName() + ' ('
                             + sameEmailCustomer.getStatus() + ').', True)
            return None

        return Customer(person_id, new_last_name, new_first_name, new_address,
                        new_phone, new_email, new_delivery_address)

    def registerCustomer(self):
        # new: a customer displayed by a search is changed with Update, not added again
        if self.loaded_customer_id is not None:
            self.showMessage('This customer is already registered. Use Update to change the '
                             'record, or Clear to add a new customer.', True)
            return

        customer_list = file_manager.load_customers()
        new_person_id = file_manager.next_customer_id(customer_list)

        myCustomer = self.readCustomer(new_person_id)
        if myCustomer is None:
            return

        file_manager.save_customer(myCustomer)

        self.clearFields()
        self.showMessage('Customer ' + str(myCustomer.getPersonId()) + ', '
                         + myCustomer.getFullName() + ', registered with the phone '
                         + myCustomer.getPhone() + '.', False)

    # new method to display one customer found by the number
    def searchCustomer(self):
        try:
            typed_id = int(self.field_customer_id.text())
        except ValueError:
            self.showMessage('Type the customer number, for example 1001.', True)
            return

        myCustomer = file_manager.find_customer(typed_id)
        if myCustomer is None:
            self.clearFields()
            self.showMessage('There is no customer with the number ' + str(typed_id) + '.', True)
            return

        self.loaded_customer_id = myCustomer.getPersonId()
        self.field_customer_id.setText(str(myCustomer.getPersonId()))
        self.label_status.setText(myCustomer.getStatus())
        self.field_last_name.setText(myCustomer.getLastName())
        self.field_first_name.setText(myCustomer.getFirstName())
        self.field_address.setText(myCustomer.getAddress())
        self.field_phone.setText(myCustomer.getPhone())
        self.field_email.setText(myCustomer.getEmail())

        if myCustomer.getDeliveryAddress() == myCustomer.getAddress():
            self.check_same_address.setChecked(True)
        else:
            self.check_same_address.setChecked(False)
            self.field_delivery.setText(myCustomer.getDeliveryAddress())

        self.showMessage('Customer ' + str(myCustomer.getPersonId()) + ' found.', False)

    # new method: update and delete are refused when the number in the field is not
    # the one of the customer displayed, so a record is never changed by mistake
    def isCustomerLoaded(self):
        if (self.loaded_customer_id is None
                or self.field_customer_id.text().strip() != str(self.loaded_customer_id)):
            self.showMessage('Search the customer by number first.', True)
            return False
        return True

    # new method to rewrite the record of the customer displayed
    def updateCustomer(self):
        if not self.isCustomerLoaded():
            return

        myCustomer = self.readCustomer(self.loaded_customer_id)
        if myCustomer is None:
            return

        # an inactive customer who is updated becomes active again
        was_inactive = False
        customer_list = file_manager.load_customers()
        for position in range(len(customer_list)):
            if customer_list[position].getPersonId() == self.loaded_customer_id:
                was_inactive = not customer_list[position].isActive()
                customer_list[position] = myCustomer
        file_manager.save_customers(customer_list)

        self.label_status.setText(myCustomer.getStatus())
        if was_inactive:
            self.showMessage('Customer ' + str(myCustomer.getPersonId()) + ', '
                             + myCustomer.getFullName() + ', updated and active again.', False)
        else:
            self.showMessage('Customer ' + str(myCustomer.getPersonId()) + ', '
                             + myCustomer.getFullName() + ', updated.', False)

    # new method with the three cases of the delete rule: refused while an order is
    # active, marked inactive when past orders exist, erased when there is no order
    def deleteCustomer(self):
        if not self.isCustomerLoaded():
            return

        customer_id = self.loaded_customer_id
        order_list = file_manager.load_customer_orders(customer_id)

        for myOrder in order_list:
            if myOrder.isActive():
                self.showMessage('Customer ' + str(customer_id) + ' cannot be deleted: order '
                                 + str(myOrder.getOrderId()) + ' is not completed and paid.', True)
                return

        if len(order_list) > 0 and self.label_status.text() == CUSTOMER_INACTIVE:
            self.showMessage('Customer ' + str(customer_id) + ' is already inactive.', True)
            return

        answer = QMessageBox.question(self, 'Delete customer',
                                      'Delete customer ' + str(customer_id) + '?')
        if answer != QMessageBox.StandardButton.Yes:
            return

        customer_list = file_manager.load_customers()
        new_customer_list = []
        for myCustomer in customer_list:
            if myCustomer.getPersonId() != customer_id:
                new_customer_list.append(myCustomer)
            elif len(order_list) > 0:
                myCustomer.setStatus(CUSTOMER_INACTIVE)
                new_customer_list.append(myCustomer)
        file_manager.save_customers(new_customer_list)

        self.clearFields()
        if len(order_list) > 0:
            self.showMessage('Customer ' + str(customer_id) + ' has ' + str(len(order_list))
                             + ' past order(s): the record is kept and marked inactive.', False)
        else:
            self.showMessage('Customer ' + str(customer_id) + ' deleted.', False)


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)

    # create the window of the registration form
    window = RegistrationForm()
    window.resize(760, 340)
    window.show()

    app.exec()


# the form is started alone only when this module is the one executed
if __name__ == '__main__':
    main()
