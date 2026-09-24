# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Sep 20, 2026
Algorithm:
Class: Python Teams online class
Inputs: last name, first name, home address, phone, email, delivery address,
state of the "same as home address" check box
Processing: validation of the entered values, instantiation of a Customer object,
save_customer() of the file_manager module
Outputs: the customer record appended to customers.txt, a confirmation or an error
message displayed on the form
"""
import sys

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QCheckBox, QGridLayout, QHBoxLayout)

import file_manager
from person_template import Customer, is_valid_phone, is_valid_email


class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Flower Shop, customer registration')

        self.label_title = QLabel('Register a new customer')
        self.label_title.setStyleSheet('font-weight: bold;')
        self.label_last_name = QLabel('Last name:')
        self.label_first_name = QLabel('First name:')
        self.label_address = QLabel('Home address:')
        self.label_phone = QLabel('Phone:')
        self.label_email = QLabel('Email:')
        self.label_delivery = QLabel('Delivery address:')
        self.label_message = QLabel('')

        self.field_last_name = QLineEdit()
        self.field_first_name = QLineEdit()
        self.field_address = QLineEdit()
        self.field_phone = QLineEdit()
        self.field_email = QLineEdit()
        self.field_delivery = QLineEdit()

        self.field_address.setPlaceholderText('450 Rue Sherbrooke, Montreal, QC H2X 1Y4')
        self.field_phone.setPlaceholderText('514-555-0142')
        self.field_email.setPlaceholderText('name@gmail.com')

        self.check_same_address = QCheckBox('Delivery address is the same as the home address')
        self.check_same_address.setChecked(True)
        self.field_delivery.setEnabled(False)

        self.button_register = QPushButton('Register')
        self.button_clear = QPushButton('Clear')

        self.buildLayout()

        # connect the signal (event) to the slot (action) method of this class
        self.check_same_address.stateChanged.connect(self.sameAddressChanged)
        self.button_register.clicked.connect(self.registerCustomer)
        self.button_clear.clicked.connect(self.clearForm)

    def buildLayout(self):
        grid = QGridLayout()
        grid.setColumnStretch(1, 1)

        grid.addWidget(self.label_title, 0, 0, 1, 2)
        grid.addWidget(self.label_last_name, 1, 0)
        grid.addWidget(self.field_last_name, 1, 1)
        grid.addWidget(self.label_first_name, 2, 0)
        grid.addWidget(self.field_first_name, 2, 1)
        grid.addWidget(self.label_address, 3, 0)
        grid.addWidget(self.field_address, 3, 1)
        grid.addWidget(self.label_phone, 4, 0)
        grid.addWidget(self.field_phone, 4, 1)
        grid.addWidget(self.label_email, 5, 0)
        grid.addWidget(self.field_email, 5, 1)
        grid.addWidget(self.check_same_address, 6, 1)
        grid.addWidget(self.label_delivery, 7, 0)
        grid.addWidget(self.field_delivery, 7, 1)

        row_buttons = QHBoxLayout()
        row_buttons.addWidget(self.button_register)
        row_buttons.addWidget(self.button_clear)
        row_buttons.addStretch()

        grid.addLayout(row_buttons, 8, 1)
        grid.addWidget(self.label_message, 9, 0, 1, 2)
        grid.setRowStretch(10, 1)

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

    def clearForm(self):
        self.field_last_name.setText('')
        self.field_first_name.setText('')
        self.field_address.setText('')
        self.field_phone.setText('')
        self.field_email.setText('')
        self.field_delivery.setText('')
        self.check_same_address.setChecked(True)
        self.showMessage('', False)

    def registerCustomer(self):
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
            return

        if new_delivery_address == '':
            self.showMessage('Enter a delivery address or check the box above.', True)
            return

        if not is_valid_phone(new_phone):
            self.showMessage('The phone number must hold ten digits, for example 514-555-0142.', True)
            return

        if not is_valid_email(new_email):
            self.showMessage('The email address is not valid, for example name@gmail.com.', True)
            return

        # instantiate the object and store it
        customer_list = file_manager.load_customers()
        new_person_id = file_manager.next_customer_id(customer_list)

        myCustomer = Customer(new_person_id, new_last_name, new_first_name, new_address,
                              new_phone, new_email, new_delivery_address)
        file_manager.save_customer(myCustomer)

        self.showMessage('Customer ' + str(myCustomer.getPersonId()) + ', '
                         + myCustomer.getFullName() + ', registered with the phone '
                         + myCustomer.getPhone() + '.', False)

        self.field_last_name.setText('')
        self.field_first_name.setText('')
        self.field_address.setText('')
        self.field_phone.setText('')
        self.field_email.setText('')
        self.field_delivery.setText('')
        self.check_same_address.setChecked(True)


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)

    # create the window of the registration form
    window = RegistrationForm()
    window.resize(620, 300)
    window.show()

    app.exec()


# the form is started alone only when this module is the one executed
if __name__ == '__main__':
    main()