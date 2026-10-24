# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Starting on Oct 10, 2026, updating started on Oct 24, 2026 for iteration 3
Algorithm:
Class: Python Teams online class
Inputs: charge number, title, rate, kind of charge (percent or fixed amount), the
button pressed
Processing: validation of the entered values, instantiation of a Charge object, add,
search, update and delete of a record through the database_manager module, rules
that protect the charges the billing form depends on
Outputs: the charge record added to, changed in or removed from the charge table, the
record found displayed in the fields, the list of all the charges, a confirmation or
an error message displayed on the form
"""
import sys

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QComboBox, QTextEdit, QGridLayout, QHBoxLayout, QMessageBox)

import database_manager
from billing_template import (Charge, CHARGE_PERCENT, CHARGE_FIXED, CHARGE_SUBTOTAL,
                              CHARGE_TOTAL, CHARGE_GST, CHARGE_QST, CHARGE_DELIVERY)

# the subtotal and the total are calculated lines, they are never changed
CALCULATED_CHARGES = [CHARGE_SUBTOTAL, CHARGE_TOTAL]
# the billing form looks for these charges by their number, so they stay in the file
REQUIRED_CHARGES = [CHARGE_SUBTOTAL, CHARGE_TOTAL, CHARGE_GST, CHARGE_QST, CHARGE_DELIVERY]


class ChargeForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Flower Shop, charges')

        # the number of the charge displayed after a search, None while the form is
        # empty; update and delete only act on this charge
        self.loaded_charge_no = None

        self.label_title = QLabel('Charges of the bill')
        self.label_title.setObjectName('title')
        self.label_charge_no = QLabel('Charge number:')
        self.label_charge_title = QLabel('Title:')
        self.label_rate = QLabel('Rate:')
        self.label_kind = QLabel('Kind:')
        self.label_message = QLabel('')

        self.field_charge_no = QLineEdit()
        self.field_charge_title = QLineEdit()
        self.field_rate = QLineEdit()

        self.field_charge_no.setPlaceholderText('200 to 299 for a tax, 300 to 399 for a fee')
        self.field_charge_title.setPlaceholderText('Delivery fee')
        self.field_rate.setPlaceholderText('a percentage such as 9.975, or an amount '
                                           'such as 11.00')

        self.combo_kind = QComboBox()
        self.combo_kind.addItem(CHARGE_PERCENT)
        self.combo_kind.addItem(CHARGE_FIXED)

        self.text_charges = QTextEdit()
        self.text_charges.setReadOnly(True)

        self.button_add = QPushButton('Add')
        self.button_search = QPushButton('Search')
        self.button_update = QPushButton('Update')
        self.button_delete = QPushButton('Delete')
        self.button_clear = QPushButton('Clear')

        self.buildLayout()

        # connect the signal (event) to the slot (action) method of this class
        self.button_add.clicked.connect(self.addCharge)
        self.button_search.clicked.connect(self.searchCharge)
        self.button_update.clicked.connect(self.updateCharge)
        self.button_delete.clicked.connect(self.deleteCharge)
        self.button_clear.clicked.connect(self.clearForm)

        self.showCharges()

    def buildLayout(self):
        grid = QGridLayout()
        grid.setColumnStretch(1, 1)

        grid.addWidget(self.label_title, 0, 0, 1, 2)
        grid.addWidget(self.label_charge_no, 1, 0)
        grid.addWidget(self.field_charge_no, 1, 1)
        grid.addWidget(self.label_charge_title, 2, 0)
        grid.addWidget(self.field_charge_title, 2, 1)
        grid.addWidget(self.label_rate, 3, 0)
        grid.addWidget(self.field_rate, 3, 1)
        grid.addWidget(self.label_kind, 4, 0)
        grid.addWidget(self.combo_kind, 4, 1)

        row_buttons = QHBoxLayout()
        row_buttons.addWidget(self.button_add)
        row_buttons.addWidget(self.button_search)
        row_buttons.addWidget(self.button_update)
        row_buttons.addWidget(self.button_delete)
        row_buttons.addWidget(self.button_clear)
        row_buttons.addStretch()

        grid.addLayout(row_buttons, 5, 1)
        grid.addWidget(self.label_message, 6, 0, 1, 2)
        grid.addWidget(self.text_charges, 7, 0, 1, 2)
        grid.setRowStretch(7, 1)

        self.setLayout(grid)

    def showMessage(self, message, is_error):
        self.label_message.setText(message)
        if is_error:
            self.label_message.setStyleSheet('color: #B22222;')
        else:
            self.label_message.setStyleSheet('color: #1F7A40;')

    # the list of all the charges, with the numbers aligned to the right
    def showCharges(self):
        html_text = ('<table border="1" cellspacing="0" cellpadding="4">'
                     '<tr><th align="right">Number</th><th align="left">Title</th>'
                     '<th align="right">Rate</th><th align="left">Kind</th></tr>')
        for myCharge in database_manager.load_charges():
            if myCharge.isPercent():
                rate_text = str(myCharge.getChargeRate()) + ' %'
            else:
                rate_text = format(myCharge.getChargeRate(), '.2f') + ' $'
            html_text = (html_text + '<tr><td align="right">' + str(myCharge.getChargeNo())
                         + '</td><td align="left">' + myCharge.getChargeTitle()
                         + '</td><td align="right">' + rate_text
                         + '</td><td align="left">' + myCharge.getChargeKind() + '</td></tr>')
        html_text = html_text + '</table>'
        self.text_charges.setHtml(html_text)

    def clearFields(self):
        self.loaded_charge_no = None
        self.field_charge_no.setText('')
        self.field_charge_title.setText('')
        self.field_rate.setText('')
        self.combo_kind.setEnabled(True)
        self.combo_kind.setCurrentIndex(0)

    def clearForm(self):
        self.clearFields()
        self.showMessage('', False)

    # reading and validating the fields; the method returns a Charge object, or None
    # after displaying the error
    def readCharge(self, charge_no):
        new_title = self.field_charge_title.text().strip()
        new_kind = self.combo_kind.currentText()

        if new_title == '':
            self.showMessage('The title is required.', True)
            return None

        try:
            new_rate = float(self.field_rate.text())
        except ValueError:
            self.showMessage('The rate must be a number, for example 9.975 or 11.00.', True)
            return None

        if new_rate < 0:
            self.showMessage('The rate cannot be negative.', True)
            return None

        if new_kind == CHARGE_PERCENT and new_rate > 100:
            self.showMessage('A percentage cannot be above 100.', True)
            return None

        return Charge(charge_no, new_title, new_rate, new_kind)

    def addCharge(self):
        if self.loaded_charge_no is not None:
            self.showMessage('This charge already exists. Use Update to change the record, '
                             'or Clear to add a new charge.', True)
            return

        # the number of a charge is typed, because it tells the group of the charge:
        # the 200 numbers are taxes and the 300 numbers are fees
        try:
            new_charge_no = int(self.field_charge_no.text())
        except ValueError:
            self.showMessage('Type the charge number, for example 301.', True)
            return

        if new_charge_no < 200 or new_charge_no > 399:
            self.showMessage('The charge number must be between 200 and 399.', True)
            return

        if database_manager.find_charge(new_charge_no) is not None:
            self.showMessage('The charge number ' + str(new_charge_no) + ' is already used.', True)
            return

        myCharge = self.readCharge(new_charge_no)
        if myCharge is None:
            return

        database_manager.save_charge(myCharge)

        self.clearFields()
        self.showCharges()
        self.showMessage('Charge ' + str(myCharge.getChargeNo()) + ', '
                         + myCharge.getChargeTitle() + ', added.', False)

    def searchCharge(self):
        try:
            typed_no = int(self.field_charge_no.text())
        except ValueError:
            self.showMessage('Type the charge number, for example 300.', True)
            return

        myCharge = database_manager.find_charge(typed_no)
        if myCharge is None:
            self.clearFields()
            self.showMessage('There is no charge with the number ' + str(typed_no) + '.', True)
            return

        self.loaded_charge_no = myCharge.getChargeNo()
        self.field_charge_no.setText(str(myCharge.getChargeNo()))
        self.field_charge_title.setText(myCharge.getChargeTitle())
        self.field_rate.setText(str(myCharge.getChargeRate()))
        self.combo_kind.setCurrentText(myCharge.getChargeKind())
        # the kind of a charge the billing form depends on cannot be changed
        self.combo_kind.setEnabled(myCharge.getChargeNo() not in REQUIRED_CHARGES)

        self.showMessage('Charge ' + str(myCharge.getChargeNo()) + ' found.', False)

    # update and delete are refused when the number in the field is not the one of
    # the charge displayed, so a record is never changed by mistake
    def isChargeLoaded(self):
        if (self.loaded_charge_no is None
                or self.field_charge_no.text().strip() != str(self.loaded_charge_no)):
            self.showMessage('Search the charge by number first.', True)
            return False
        return True

    # a new rate applies to the bills paid from now on; the bills already paid keep
    # the rate and the amount stored in the bill_detail table
    def updateCharge(self):
        if not self.isChargeLoaded():
            return

        if self.loaded_charge_no in CALCULATED_CHARGES:
            self.showMessage('The subtotal and the total are calculated lines and cannot '
                             'be changed.', True)
            return

        myCharge = self.readCharge(self.loaded_charge_no)
        if myCharge is None:
            return

        # updated: one UPDATE of the charge row replaces the rewriting of the whole file
        database_manager.update_charge(myCharge)

        self.showCharges()
        self.showMessage('Charge ' + str(myCharge.getChargeNo()) + ', '
                         + myCharge.getChargeTitle() + ', updated.', False)

    # a charge cannot be deleted when the billing form depends on it or when a paid
    # bill holds it
    def deleteCharge(self):
        if not self.isChargeLoaded():
            return

        charge_no = self.loaded_charge_no

        if charge_no in REQUIRED_CHARGES:
            self.showMessage('Charge ' + str(charge_no) + ' is needed to calculate every '
                             'bill and cannot be deleted.', True)
            return

        for myBillDetail in database_manager.load_bill_details():
            if myBillDetail.getChargeNo() == charge_no:
                self.showMessage('Charge ' + str(charge_no) + ' cannot be deleted: the bill '
                                 'of order ' + str(myBillDetail.getOrderId()) + ' holds it.', True)
                return

        answer = QMessageBox.question(self, 'Delete charge',
                                      'Delete charge ' + str(charge_no) + '?')
        if answer != QMessageBox.StandardButton.Yes:
            return

        # updated: one DELETE of the charge row replaces the rewriting of the whole file
        database_manager.delete_charge(charge_no)

        self.clearFields()
        self.showCharges()
        self.showMessage('Charge ' + str(charge_no) + ' deleted.', False)


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)

    # the charges of the bill are created when the charge table holds no record
    database_manager.create_default_data()

    # create the window of the charge form
    window = ChargeForm()
    window.resize(760, 460)
    window.show()

    app.exec()


# the form is started alone only when this module is the one executed
if __name__ == '__main__':
    main()
