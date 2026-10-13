# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Starting on Oct 11, 2026
Algorithm:
Class: Python Teams online class
Inputs: order number, the optional fees checked for this bill, the button pressed
Processing: search of the order, calculation of the bill from the charges of
charges.txt (subtotal, delivery fee for a delivery, optional fees, taxes, total),
instantiation of one BillDetail object per charge, payment of the order
Outputs: the bill displayed on the form, one line per charge stored in
bill_details.txt with the month and the year, the order marked as paid in orders.txt,
a confirmation or an error message displayed on the form
"""
import sys
import datetime

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QCheckBox, QTextEdit, QGridLayout, QHBoxLayout)

import file_manager
from order_template import PAYMENT_PAID
from billing_template import (BillDetail, CHARGE_SUBTOTAL, CHARGE_TOTAL, CHARGE_GST,
                              CHARGE_DELIVERY)

SHOP_NAME = 'Flower Shop'


# the bill of an order as an HTML text, with the numbers aligned to the right; the
# same text is the receipt of a paid order
def build_bill_html(myOrder, bill_list, is_paid):
    customer_text = 'Walk-in customer'
    if myOrder.getCustomerId() is not None:
        customer_text = 'Customer ' + str(myOrder.getCustomerId())
        myCustomer = file_manager.find_customer(myOrder.getCustomerId())
        if myCustomer is not None:
            customer_text = (customer_text + ', ' + myCustomer.getFullName() + ', '
                             + myCustomer.getPhone())

    staff_text = str(myOrder.getStaffId())
    myStaff = file_manager.find_staff(myOrder.getStaffId())
    if myStaff is not None:
        staff_text = myStaff.getFullName()

    html_text = ('<h3>' + SHOP_NAME + ', order ' + str(myOrder.getOrderId()) + '</h3>'
                 + '<p>' + customer_text + '<br>Ordered on ' + myOrder.getOrderDate()
                 + ', taken by ' + staff_text + '<br>' + myOrder.getOrderType() + ' on '
                 + myOrder.getDeliveryDate())
    if myOrder.isDelivery():
        html_text = html_text + ', ' + myOrder.getDeliveryAddress()
    html_text = html_text + '</p>'

    html_text = (html_text + '<table border="1" cellspacing="0" cellpadding="4">'
                 + '<tr><th align="left">Code</th><th align="left">Item</th>'
                 + '<th align="right">Quantity</th><th align="right">Price to pay</th>'
                 + '<th align="right">Line total</th></tr>')
    for myItem in myOrder.getItemList():
        html_text = (html_text + '<tr><td align="left">' + myItem.getProductCode()
                     + '</td><td align="left">' + myItem.getProductName()
                     + '</td><td align="right">' + str(myItem.getQuantity())
                     + '</td><td align="right">' + format(myItem.calculatePriceToPay(), '.2f')
                     + ' $</td><td align="right">' + format(myItem.calculateLineTotal(), '.2f')
                     + ' $</td></tr>')
    html_text = html_text + '</table><br>'

    html_text = (html_text + '<table border="1" cellspacing="0" cellpadding="4">'
                 + '<tr><th align="right">Number</th><th align="left">Charge</th>'
                 + '<th align="right">Rate</th><th align="right">Amount</th></tr>')
    for myBillDetail in bill_list:
        charge_title = 'Charge ' + str(myBillDetail.getChargeNo())
        rate_text = ''
        myCharge = file_manager.find_charge(myBillDetail.getChargeNo())
        if myCharge is not None:
            charge_title = myCharge.getChargeTitle()
            # the rate is displayed for the percentages applied to a base, the taxes
            if (myCharge.isPercent() and myBillDetail.getChargeNo() != CHARGE_SUBTOTAL
                    and myBillDetail.getChargeNo() != CHARGE_TOTAL):
                rate_text = str(myBillDetail.getRate()) + ' %'

        if myBillDetail.getChargeNo() == CHARGE_TOTAL:
            charge_title = '<b>' + charge_title + '</b>'
            amount_text = '<b>' + format(myBillDetail.getAmount(), '.2f') + ' $</b>'
        else:
            amount_text = format(myBillDetail.getAmount(), '.2f') + ' $'

        html_text = (html_text + '<tr><td align="right">' + str(myBillDetail.getChargeNo())
                     + '</td><td align="left">' + charge_title
                     + '</td><td align="right">' + rate_text
                     + '</td><td align="right">' + amount_text + '</td></tr>')
    html_text = html_text + '</table>'

    if is_paid and len(bill_list) > 0:
        html_text = (html_text + '<p><b>Paid</b>, ' + str(bill_list[0].getMonth()) + '/'
                     + str(bill_list[0].getYear()) + '</p>')
    else:
        html_text = html_text + '<p>Not paid yet</p>'
    return html_text


class BillingForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Flower Shop, billing')

        # the order displayed after a search, None while the form is empty
        self.loadedOrder = None
        # the optional fees of charges.txt, in the same sequence as their check boxes
        self.optional_charge_list = []
        self.optional_check_list = []

        self.label_title = QLabel('Bill an order')
        self.label_title.setStyleSheet('font-weight: bold;')
        self.label_order_id = QLabel('Order number:')
        self.label_optional = QLabel('Optional fees:')
        self.label_message = QLabel('')

        self.field_order_id = QLineEdit()
        self.field_order_id.setPlaceholderText('5001')

        self.text_bill = QTextEdit()
        self.text_bill.setReadOnly(True)

        self.button_search = QPushButton('Search')
        self.button_calculate = QPushButton('Calculate')
        self.button_pay = QPushButton('Pay')
        self.button_clear = QPushButton('Clear')

        self.buildLayout()

        # connect the signal (event) to the slot (action) method of this class
        self.button_search.clicked.connect(self.searchOrder)
        self.button_calculate.clicked.connect(self.calculateClicked)
        self.button_pay.clicked.connect(self.payOrder)
        self.button_clear.clicked.connect(self.clearForm)

    def buildLayout(self):
        grid = QGridLayout()
        grid.setColumnStretch(1, 1)

        row_buttons = QHBoxLayout()
        row_buttons.addWidget(self.button_search)
        row_buttons.addWidget(self.button_calculate)
        row_buttons.addWidget(self.button_pay)
        row_buttons.addWidget(self.button_clear)
        row_buttons.addStretch()

        # one check box per optional fee: a fee numbered from 301 is added to a bill
        # only when the clerk checks it, because it does not apply to every order
        row_optional = QHBoxLayout()
        for myCharge in file_manager.load_charges():
            if myCharge.getChargeNo() > CHARGE_DELIVERY and myCharge.getChargeNo() <= 399:
                if myCharge.isPercent():
                    rate_text = str(myCharge.getChargeRate()) + ' %'
                else:
                    rate_text = format(myCharge.getChargeRate(), '.2f') + ' $'
                check_charge = QCheckBox(myCharge.getChargeTitle() + ' (' + rate_text + ')')
                self.optional_charge_list.append(myCharge)
                self.optional_check_list.append(check_charge)
                row_optional.addWidget(check_charge)
        row_optional.addStretch()

        grid.addWidget(self.label_title, 0, 0, 1, 2)
        grid.addWidget(self.label_order_id, 1, 0)
        grid.addWidget(self.field_order_id, 1, 1)
        if len(self.optional_check_list) > 0:
            grid.addWidget(self.label_optional, 2, 0)
            grid.addLayout(row_optional, 2, 1)
        grid.addLayout(row_buttons, 3, 1)
        grid.addWidget(self.label_message, 4, 0, 1, 2)
        grid.addWidget(self.text_bill, 5, 0, 1, 2)
        grid.setRowStretch(5, 1)

        self.setLayout(grid)

    def showMessage(self, message, is_error):
        self.label_message.setText(message)
        if is_error:
            self.label_message.setStyleSheet('color: #B22222;')
        else:
            self.label_message.setStyleSheet('color: #1F7A40;')

    def setOptionalEnabled(self, is_enabled):
        for check_charge in self.optional_check_list:
            check_charge.setEnabled(is_enabled)
            if not is_enabled:
                check_charge.setChecked(False)

    def clearForm(self):
        self.loadedOrder = None
        self.field_order_id.setText('')
        self.text_bill.setHtml('')
        self.setOptionalEnabled(True)
        self.showMessage('', False)

    def searchOrder(self):
        try:
            typed_id = int(self.field_order_id.text())
        except ValueError:
            self.showMessage('Type the order number, for example 5001.', True)
            return

        myOrder = file_manager.find_order(typed_id)
        if myOrder is None:
            self.clearForm()
            self.showMessage('There is no order with the number ' + str(typed_id) + '.', True)
            return

        self.loadedOrder = myOrder
        self.field_order_id.setText(str(myOrder.getOrderId()))

        # a paid order displays its receipt, read from bill_details.txt, so it shows
        # the rates and the amounts of the day of the payment
        if myOrder.getPaymentStatus() == PAYMENT_PAID:
            self.setOptionalEnabled(False)
            bill_list = file_manager.load_order_bill(myOrder.getOrderId())
            self.text_bill.setHtml(build_bill_html(myOrder, bill_list, True))
            self.showMessage('Order ' + str(myOrder.getOrderId())
                             + ' is already paid: this is its receipt.', False)
        else:
            self.setOptionalEnabled(True)
            self.text_bill.setHtml(build_bill_html(myOrder, [], False))
            self.showMessage('Order ' + str(myOrder.getOrderId())
                             + ' found. Click Calculate to see the bill.', False)

    # calculate and pay are refused when the number in the field is not the one of
    # the order displayed
    def isOrderLoaded(self):
        if (self.loadedOrder is None
                or self.field_order_id.text().strip() != str(self.loadedOrder.getOrderId())):
            self.showMessage('Search the order by number first.', True)
            return False

        if self.loadedOrder.getPaymentStatus() == PAYMENT_PAID:
            self.showMessage('Order ' + str(self.loadedOrder.getOrderId())
                             + ' is already paid and cannot be billed twice.', True)
            return False
        return True

    # the bill of the order displayed: one BillDetail object per charge, in the
    # sequence subtotal, fees, taxes, total. The taxes apply to the subtotal plus
    # the fees
    def calculateBill(self):
        myOrder = self.loadedOrder
        today = datetime.date.today()
        bill_list = []

        subtotal = round(myOrder.calculateSubtotal(), 2)
        subtotalCharge = file_manager.find_charge(CHARGE_SUBTOTAL)
        bill_list.append(BillDetail(myOrder.getOrderId(), CHARGE_SUBTOTAL, subtotal,
                                    subtotalCharge.getChargeRate(), subtotal,
                                    today.month, today.year))

        fee_list = []
        if myOrder.isDelivery():
            fee_list.append(file_manager.find_charge(CHARGE_DELIVERY))
        for position in range(len(self.optional_check_list)):
            if self.optional_check_list[position].isChecked():
                fee_list.append(self.optional_charge_list[position])

        taxable_base = subtotal
        for myCharge in fee_list:
            amount = myCharge.calculateAmount(subtotal)
            taxable_base = taxable_base + amount
            bill_list.append(BillDetail(myOrder.getOrderId(), myCharge.getChargeNo(), subtotal,
                                        myCharge.getChargeRate(), amount,
                                        today.month, today.year))
        taxable_base = round(taxable_base, 2)

        total = taxable_base
        for myCharge in file_manager.load_charges():
            if myCharge.getChargeNo() >= CHARGE_GST and myCharge.getChargeNo() <= 299:
                amount = myCharge.calculateAmount(taxable_base)
                total = total + amount
                bill_list.append(BillDetail(myOrder.getOrderId(), myCharge.getChargeNo(),
                                            taxable_base, myCharge.getChargeRate(), amount,
                                            today.month, today.year))
        total = round(total, 2)

        totalCharge = file_manager.find_charge(CHARGE_TOTAL)
        bill_list.append(BillDetail(myOrder.getOrderId(), CHARGE_TOTAL, total,
                                    totalCharge.getChargeRate(), total,
                                    today.month, today.year))
        return bill_list

    def calculateClicked(self):
        if not self.isOrderLoaded():
            return

        bill_list = self.calculateBill()
        self.text_bill.setHtml(build_bill_html(self.loadedOrder, bill_list, False))
        self.showMessage('Bill of order ' + str(self.loadedOrder.getOrderId())
                         + ' calculated, total '
                         + format(bill_list[len(bill_list) - 1].getAmount(), '.2f')
                         + ' $. Click Pay to record the payment.', False)

    # the payment stores the lines of the bill and marks the order as paid; from
    # then on the order cannot be billed again and its lines cannot change
    def payOrder(self):
        if not self.isOrderLoaded():
            return

        # the order is read again, in case it changed since the search
        myOrder = file_manager.find_order(self.loadedOrder.getOrderId())
        if myOrder is None or myOrder.getPaymentStatus() == PAYMENT_PAID:
            self.showMessage('Search the order again: it changed since it was displayed.', True)
            return
        self.loadedOrder = myOrder

        bill_list = self.calculateBill()
        for myBillDetail in bill_list:
            file_manager.save_bill_detail(myBillDetail)

        order_list = file_manager.load_orders()
        for savedOrder in order_list:
            if savedOrder.getOrderId() == myOrder.getOrderId():
                savedOrder.setPaymentStatus(PAYMENT_PAID)
        file_manager.save_orders(order_list)

        myOrder.setPaymentStatus(PAYMENT_PAID)
        self.setOptionalEnabled(False)
        self.text_bill.setHtml(build_bill_html(myOrder, bill_list, True))
        self.showMessage('Order ' + str(myOrder.getOrderId()) + ' paid, total '
                         + format(bill_list[len(bill_list) - 1].getAmount(), '.2f') + ' $.', False)


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)

    # the charges of the bill are created when charges.txt holds no record
    file_manager.create_default_data()

    # create the window of the billing form
    window = BillingForm()
    window.resize(820, 620)
    window.show()

    app.exec()


# the form is started alone only when this module is the one executed
if __name__ == '__main__':
    main()
