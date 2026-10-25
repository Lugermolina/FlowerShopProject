# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Oct 24, 2026 for iteration 3
Algorithm:
Class: Python Teams online class
Inputs: supplier number, company name, contact name, phone, email, address, the button
pressed, the row clicked in the list of suppliers
Processing: validation of the entered values, duplicate name check, instantiation of a
Supplier object, add, search, update and delete of a record through the
database_manager module, delete rule based on the restocks of the supplier
Outputs: the supplier record added to, changed in or removed from the supplier table,
the record found displayed in the fields, the list of all the suppliers, a confirmation
or an error message displayed on the form
"""
import sys

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QGridLayout, QHBoxLayout, QMessageBox, QTableWidget,
                             QTableWidgetItem, QAbstractItemView)

import database_manager
from person_template import is_valid_phone, is_valid_email
from supplier_template import Supplier

COLUMN_TITLES = ['Number', 'Supplier', 'Contact', 'Phone', 'Email', 'Address']


class SupplierForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Flower Shop, suppliers')

        # the number of the supplier displayed after a search, None while the form is
        # empty; update and delete only act on this supplier
        self.loaded_supplier_id = None

        self.label_title = QLabel('Suppliers')
        self.label_title.setObjectName('title')
        self.label_supplier_id = QLabel('Supplier number:')
        self.label_supplier_name = QLabel('Company name:')
        self.label_contact_name = QLabel('Contact name:')
        self.label_phone = QLabel('Phone:')
        self.label_email = QLabel('Email:')
        self.label_address = QLabel('Address:')
        self.label_message = QLabel('')

        self.field_supplier_id = QLineEdit()
        self.field_supplier_name = QLineEdit()
        self.field_contact_name = QLineEdit()
        self.field_phone = QLineEdit()
        self.field_email = QLineEdit()
        self.field_address = QLineEdit()

        self.field_supplier_id.setPlaceholderText('type a number to search, or click a supplier '
                                                  'in the list; a new supplier gets a number '
                                                  'automatically')
        self.field_supplier_name.setPlaceholderText('Laurentian Greenhouses')
        self.field_contact_name.setPlaceholderText('Sophie Lavoie')
        self.field_phone.setPlaceholderText('450-555-0131')
        self.field_email.setPlaceholderText('orders@supplier.ca')
        self.field_address.setPlaceholderText('1400 Chemin du Lac, Saint-Sauveur, QC J0R 1R0')

        self.button_add = QPushButton('Add')
        self.button_search = QPushButton('Search')
        self.button_update = QPushButton('Update')
        self.button_delete = QPushButton('Delete')
        self.button_clear = QPushButton('Clear')

        self.table_suppliers = QTableWidget()
        self.table_suppliers.setColumnCount(len(COLUMN_TITLES))
        self.table_suppliers.setHorizontalHeaderLabels(COLUMN_TITLES)
        self.table_suppliers.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_suppliers.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_suppliers.setAlternatingRowColors(True)

        self.buildLayout()

        # connect the signal (event) to the slot (action) method of this class
        self.button_add.clicked.connect(self.addSupplier)
        self.button_search.clicked.connect(self.searchSupplier)
        self.button_update.clicked.connect(self.updateSupplier)
        self.button_delete.clicked.connect(self.deleteSupplier)
        self.button_clear.clicked.connect(self.clearForm)
        # a click on a row of the list displays that supplier in the fields
        self.table_suppliers.cellClicked.connect(self.supplierClicked)

        self.showSuppliers()

    def buildLayout(self):
        grid = QGridLayout()
        grid.setColumnStretch(1, 1)

        grid.addWidget(self.label_title, 0, 0, 1, 2)
        grid.addWidget(self.label_supplier_id, 1, 0)
        grid.addWidget(self.field_supplier_id, 1, 1)
        grid.addWidget(self.label_supplier_name, 2, 0)
        grid.addWidget(self.field_supplier_name, 2, 1)
        grid.addWidget(self.label_contact_name, 3, 0)
        grid.addWidget(self.field_contact_name, 3, 1)
        grid.addWidget(self.label_phone, 4, 0)
        grid.addWidget(self.field_phone, 4, 1)
        grid.addWidget(self.label_email, 5, 0)
        grid.addWidget(self.field_email, 5, 1)
        grid.addWidget(self.label_address, 6, 0)
        grid.addWidget(self.field_address, 6, 1)

        row_buttons = QHBoxLayout()
        row_buttons.addWidget(self.button_add)
        row_buttons.addWidget(self.button_search)
        row_buttons.addWidget(self.button_update)
        row_buttons.addWidget(self.button_delete)
        row_buttons.addWidget(self.button_clear)
        row_buttons.addStretch()

        grid.addLayout(row_buttons, 7, 1)
        grid.addWidget(self.label_message, 8, 0, 1, 2)
        grid.addWidget(self.table_suppliers, 9, 0, 1, 2)

        self.setLayout(grid)

    def showMessage(self, message, is_error):
        self.label_message.setText(message)
        if is_error:
            self.label_message.setStyleSheet('color: #B22222;')
        else:
            self.label_message.setStyleSheet('color: #1F7A40;')

    def showSuppliers(self):
        supplier_list = database_manager.load_suppliers()
        self.table_suppliers.setRowCount(len(supplier_list))

        row = 0
        for mySupplier in supplier_list:
            self.table_suppliers.setItem(row, 0, QTableWidgetItem(str(mySupplier.getSupplierId())))
            self.table_suppliers.setItem(row, 1, QTableWidgetItem(mySupplier.getSupplierName()))
            self.table_suppliers.setItem(row, 2, QTableWidgetItem(mySupplier.getContactName()))
            self.table_suppliers.setItem(row, 3, QTableWidgetItem(mySupplier.getPhone()))
            self.table_suppliers.setItem(row, 4, QTableWidgetItem(mySupplier.getEmail()))
            self.table_suppliers.setItem(row, 5, QTableWidgetItem(mySupplier.getAddress()))
            row = row + 1

        self.table_suppliers.resizeColumnsToContents()

    def clearFields(self):
        self.loaded_supplier_id = None
        self.field_supplier_id.setText('')
        self.field_supplier_name.setText('')
        self.field_contact_name.setText('')
        self.field_phone.setText('')
        self.field_email.setText('')
        self.field_address.setText('')
        self.table_suppliers.clearSelection()

    def clearForm(self):
        self.clearFields()
        self.showMessage('', False)

    # reading and validating the fields; the method returns a Supplier object, or None
    # after displaying the error
    def readSupplier(self, supplier_id):
        new_supplier_name = self.field_supplier_name.text().strip()
        new_contact_name = self.field_contact_name.text().strip()
        new_phone = self.field_phone.text().strip()
        new_email = self.field_email.text().strip()
        new_address = self.field_address.text().strip()

        if (new_supplier_name == '' or new_contact_name == '' or new_phone == ''
                or new_email == '' or new_address == ''):
            self.showMessage('All the fields are required.', True)
            return None

        if not is_valid_phone(new_phone):
            self.showMessage('The phone number must hold ten digits, for example 450-555-0131.', True)
            return None

        if not is_valid_email(new_email):
            self.showMessage('The email address is not valid, for example orders@supplier.ca.', True)
            return None

        # two suppliers cannot share a company name; on an update the supplier itself
        # is not counted
        for mySupplier in database_manager.load_suppliers():
            if (mySupplier.getSupplierName().lower() == new_supplier_name.lower()
                    and mySupplier.getSupplierId() != supplier_id):
                self.showMessage('The company ' + new_supplier_name + ' is already supplier '
                                 + str(mySupplier.getSupplierId()) + '.', True)
                return None

        return Supplier(supplier_id, new_supplier_name, new_contact_name, new_phone,
                        new_email, new_address)

    def addSupplier(self):
        if self.loaded_supplier_id is not None:
            self.showMessage('This supplier is already registered. Use Update to change the '
                             'record, or Clear to add a new supplier.', True)
            return

        new_supplier_id = database_manager.next_supplier_id()

        mySupplier = self.readSupplier(new_supplier_id)
        if mySupplier is None:
            return

        database_manager.save_supplier(mySupplier)

        self.clearFields()
        self.showSuppliers()
        self.showMessage('Supplier ' + str(mySupplier.getSupplierId()) + ', '
                         + mySupplier.getSupplierName() + ', added with the phone '
                         + mySupplier.getPhone() + '.', False)

    def searchSupplier(self):
        try:
            typed_id = int(self.field_supplier_id.text())
        except ValueError:
            self.showMessage('Type the supplier number, for example 3001.', True)
            return

        mySupplier = database_manager.find_supplier(typed_id)
        if mySupplier is None:
            self.clearFields()
            self.showMessage('There is no supplier with the number ' + str(typed_id) + '.', True)
            return

        self.loaded_supplier_id = mySupplier.getSupplierId()
        self.field_supplier_id.setText(str(mySupplier.getSupplierId()))
        self.field_supplier_name.setText(mySupplier.getSupplierName())
        self.field_contact_name.setText(mySupplier.getContactName())
        self.field_phone.setText(mySupplier.getPhone())
        self.field_email.setText(mySupplier.getEmail())
        self.field_address.setText(mySupplier.getAddress())

        self.showMessage('Supplier ' + str(mySupplier.getSupplierId()) + ' found.', False)

    def supplierClicked(self, row, column):
        self.field_supplier_id.setText(self.table_suppliers.item(row, 0).text())
        self.searchSupplier()

    # update and delete are refused when the number in the field is not the one of the
    # supplier displayed, so a record is never changed by mistake
    def isSupplierLoaded(self):
        if (self.loaded_supplier_id is None
                or self.field_supplier_id.text().strip() != str(self.loaded_supplier_id)):
            self.showMessage('Search the supplier by number first.', True)
            return False
        return True

    def updateSupplier(self):
        if not self.isSupplierLoaded():
            return

        mySupplier = self.readSupplier(self.loaded_supplier_id)
        if mySupplier is None:
            return

        database_manager.update_supplier(mySupplier)

        self.showSuppliers()
        self.showMessage('Supplier ' + str(mySupplier.getSupplierId()) + ', '
                         + mySupplier.getSupplierName() + ', updated.', False)

    # a supplier cannot be deleted once a restock came from it, because the restock
    # history refers to it
    def deleteSupplier(self):
        if not self.isSupplierLoaded():
            return

        supplier_id = self.loaded_supplier_id

        total_restocks = database_manager.count_supplier_restocks(supplier_id)
        if total_restocks > 0:
            self.showMessage('Supplier ' + str(supplier_id) + ' cannot be deleted: '
                             + str(total_restocks) + ' restock(s) came from this supplier.', True)
            return

        answer = QMessageBox.question(self, 'Delete supplier',
                                      'Delete supplier ' + str(supplier_id) + '?')
        if answer != QMessageBox.StandardButton.Yes:
            return

        database_manager.delete_supplier(supplier_id)

        self.clearFields()
        self.showSuppliers()
        self.showMessage('Supplier ' + str(supplier_id) + ' deleted.', False)


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)

    # create the window of the supplier form
    window = SupplierForm()
    window.resize(900, 520)
    window.show()

    app.exec()


# the form is started alone only when this module is the one executed
if __name__ == '__main__':
    main()
