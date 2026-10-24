# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Starting on Oct 11, 2026, updating started on Oct 24, 2026 for iteration 3
Algorithm:
Class: Python Teams online class
Inputs: the report selected in the list, the value the report asks for (customer
number, date, order number or stock level), the Show button
Processing: reading of the customers, the staff, the catalog, the orders and the
bills through the database_manager module, selection and totaling of the records of the
report selected
Outputs: the report displayed as a table, with the numbers and their column headings
aligned to the right, and the number of records found
"""
import sys
import datetime

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QComboBox, QTextEdit, QGridLayout)

import database_manager
from order_template import PAYMENT_PAID
from billing_template import CHARGE_SUBTOTAL, CHARGE_TOTAL, CHARGE_GST, CHARGE_DELIVERY
from billing_form import build_bill_html

# the reports of the clerk, the end user of the system
REPORT_CUSTOMER_ORDERS = 'Order history of a customer'
REPORT_DELIVERIES = 'Deliveries of a date'
REPORT_RECEIPT = 'Receipt of an order'
# the management reports
REPORT_ALL_CUSTOMERS = 'List of all customers'
REPORT_ALL_ORDERS = 'List of all orders'
REPORT_SALES = 'Sales summary by month'
REPORT_LOW_STOCK = 'Low stock items'
REPORT_UNPAID = 'Unpaid orders'
REPORT_STAFF = 'List of the staff'

DEFAULT_STOCK_LEVEL = 5


class ReportForm(QWidget):
    # the form shows the clerk reports or the management reports, according to the
    # menu item that opened it; the list of the staff is added only for an admin
    def __init__(self, current_staff=None, show_management=False):
        super().__init__()
        self.setWindowTitle('Flower Shop, reports')

        if show_management:
            self.label_title = QLabel('Management reports')
        else:
            self.label_title = QLabel('Clerk reports')
        self.label_title.setObjectName('title')
        self.label_report = QLabel('Report:')
        self.label_value = QLabel('')
        self.label_message = QLabel('')

        self.combo_report = QComboBox()
        if show_management:
            self.combo_report.addItem(REPORT_ALL_CUSTOMERS)
            self.combo_report.addItem(REPORT_ALL_ORDERS)
            self.combo_report.addItem(REPORT_SALES)
            self.combo_report.addItem(REPORT_LOW_STOCK)
            self.combo_report.addItem(REPORT_UNPAID)
            if current_staff is not None and current_staff.isAdmin():
                self.combo_report.addItem(REPORT_STAFF)
        else:
            self.combo_report.addItem(REPORT_CUSTOMER_ORDERS)
            self.combo_report.addItem(REPORT_DELIVERIES)
            self.combo_report.addItem(REPORT_RECEIPT)

        self.field_value = QLineEdit()
        self.button_show = QPushButton('Show')

        self.text_report = QTextEdit()
        self.text_report.setReadOnly(True)

        self.buildLayout()

        # connect the signal (event) to the slot (action) method of this class
        self.combo_report.currentIndexChanged.connect(self.reportChanged)
        self.button_show.clicked.connect(self.showReport)

        self.reportChanged()

    def buildLayout(self):
        grid = QGridLayout()
        grid.setColumnStretch(1, 1)

        grid.addWidget(self.label_title, 0, 0, 1, 3)
        grid.addWidget(self.label_report, 1, 0)
        grid.addWidget(self.combo_report, 1, 1)
        grid.addWidget(self.label_value, 2, 0)
        grid.addWidget(self.field_value, 2, 1)
        grid.addWidget(self.button_show, 2, 2)
        grid.addWidget(self.label_message, 3, 0, 1, 3)
        grid.addWidget(self.text_report, 4, 0, 1, 3)
        grid.setRowStretch(4, 1)

        self.setLayout(grid)

    def showMessage(self, message, is_error):
        self.label_message.setText(message)
        if is_error:
            self.label_message.setStyleSheet('color: #B22222;')
        else:
            self.label_message.setStyleSheet('color: #1F7A40;')

    # the field asks for the value the selected report needs, or is disabled when
    # the report needs none
    def reportChanged(self):
        selected_report = self.combo_report.currentText()
        self.text_report.setHtml('')
        self.showMessage('', False)
        self.field_value.setEnabled(True)
        self.field_value.setText('')

        if selected_report == REPORT_CUSTOMER_ORDERS:
            self.label_value.setText('Customer number:')
            self.field_value.setPlaceholderText('1001')
        elif selected_report == REPORT_DELIVERIES:
            self.label_value.setText('Delivery date:')
            self.field_value.setText(str(datetime.date.today()))
        elif selected_report == REPORT_RECEIPT:
            self.label_value.setText('Order number:')
            self.field_value.setPlaceholderText('5001')
        elif selected_report == REPORT_LOW_STOCK:
            self.label_value.setText('Stock at or below:')
            self.field_value.setText(str(DEFAULT_STOCK_LEVEL))
        else:
            self.label_value.setText('No value needed:')
            self.field_value.setPlaceholderText('')
            self.field_value.setEnabled(False)

    # one table of a report: every column heading takes the alignment of its
    # column, left for a text and right for a number
    def buildTable(self, heading_list, align_list, row_list):
        html_text = '<table border="1" cellspacing="0" cellpadding="4"><tr>'
        for position in range(len(heading_list)):
            html_text = (html_text + '<th align="' + align_list[position] + '">'
                         + heading_list[position] + '</th>')
        html_text = html_text + '</tr>'

        for row in row_list:
            html_text = html_text + '<tr>'
            for position in range(len(row)):
                html_text = (html_text + '<td align="' + align_list[position] + '">'
                             + str(row[position]) + '</td>')
            html_text = html_text + '</tr>'
        return html_text + '</table>'

    def getCustomerName(self, myOrder):
        if myOrder.getCustomerId() is None:
            return 'Walk-in customer'
        myCustomer = database_manager.find_customer(myOrder.getCustomerId())
        if myCustomer is None:
            return 'Customer ' + str(myOrder.getCustomerId())
        return myCustomer.getFullName()

    def getStaffName(self, myOrder):
        myStaff = database_manager.find_staff(myOrder.getStaffId())
        if myStaff is None:
            return 'Employee ' + str(myOrder.getStaffId())
        return myStaff.getFullName()

    def showReport(self):
        selected_report = self.combo_report.currentText()

        if selected_report == REPORT_CUSTOMER_ORDERS:
            self.showCustomerOrders()
        elif selected_report == REPORT_DELIVERIES:
            self.showDeliveries()
        elif selected_report == REPORT_RECEIPT:
            self.showReceipt()
        elif selected_report == REPORT_ALL_CUSTOMERS:
            self.showAllCustomers()
        elif selected_report == REPORT_ALL_ORDERS:
            self.showOrderList(database_manager.load_orders(), 'All the orders')
        elif selected_report == REPORT_SALES:
            self.showSales()
        elif selected_report == REPORT_LOW_STOCK:
            self.showLowStock()
        elif selected_report == REPORT_UNPAID:
            self.showUnpaidOrders()
        elif selected_report == REPORT_STAFF:
            self.showStaff()

    # a list of orders with the total of their subtotals, shared by three reports
    def showOrderList(self, order_list, report_title):
        row_list = []
        total_subtotal = 0.0
        for myOrder in order_list:
            subtotal = myOrder.calculateSubtotal()
            total_subtotal = total_subtotal + subtotal
            row_list.append([myOrder.getOrderId(), myOrder.getOrderDate(),
                             self.getCustomerName(myOrder), self.getStaffName(myOrder),
                             myOrder.getOrderType(), myOrder.getDeliveryDate(),
                             myOrder.getOrderStatus(), myOrder.getPaymentStatus(),
                             format(subtotal, '.2f') + ' $'])
        row_list.append(['', '', '', '', '', '', '', '<b>Total</b>',
                         '<b>' + format(total_subtotal, '.2f') + ' $</b>'])

        html_text = '<h3>' + report_title + '</h3>' + self.buildTable(
            ['Order', 'Ordered on', 'Customer', 'Taken by', 'Type', 'Pickup or delivery',
             'Status', 'Payment', 'Subtotal'],
            ['right', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'right'],
            row_list)
        self.text_report.setHtml(html_text)
        self.showMessage(str(len(order_list)) + ' order(s).', False)

    def showCustomerOrders(self):
        try:
            typed_id = int(self.field_value.text())
        except ValueError:
            self.text_report.setHtml('')
            self.showMessage('Type the customer number, for example 1001.', True)
            return

        myCustomer = database_manager.find_customer(typed_id)
        if myCustomer is None:
            self.text_report.setHtml('')
            self.showMessage('There is no customer with the number ' + str(typed_id) + '.', True)
            return

        self.showOrderList(database_manager.load_customer_orders(typed_id),
                           'Orders of customer ' + str(typed_id) + ', '
                           + myCustomer.getFullName() + ' (' + myCustomer.getStatus() + ')')

    def showDeliveries(self):
        typed_date = self.field_value.text().strip()
        try:
            typed_date = str(datetime.date.fromisoformat(typed_date))
        except ValueError:
            self.text_report.setHtml('')
            self.showMessage('The date must be written as year-month-day, for example '
                             '2026-10-15.', True)
            return

        row_list = []
        for myOrder in database_manager.load_orders():
            if myOrder.isDelivery() and myOrder.getDeliveryDate() == typed_date:
                phone_text = ''
                myCustomer = database_manager.find_customer(myOrder.getCustomerId())
                if myCustomer is not None:
                    phone_text = myCustomer.getPhone()

                item_text = ''
                for myItem in myOrder.getItemList():
                    if item_text != '':
                        item_text = item_text + ', '
                    item_text = (item_text + str(myItem.getQuantity()) + ' x '
                                 + myItem.getProductName())

                row_list.append([myOrder.getOrderId(), self.getCustomerName(myOrder),
                                 phone_text, myOrder.getDeliveryAddress(), item_text,
                                 myOrder.getOrderStatus(), myOrder.getPaymentStatus()])

        html_text = '<h3>Deliveries of ' + typed_date + '</h3>' + self.buildTable(
            ['Order', 'Customer', 'Phone', 'Delivery address', 'Items', 'Status', 'Payment'],
            ['right', 'left', 'left', 'left', 'left', 'left', 'left'], row_list)
        self.text_report.setHtml(html_text)
        self.showMessage(str(len(row_list)) + ' delivery(ies) on ' + typed_date + '.', False)

    def showReceipt(self):
        try:
            typed_id = int(self.field_value.text())
        except ValueError:
            self.text_report.setHtml('')
            self.showMessage('Type the order number, for example 5001.', True)
            return

        myOrder = database_manager.find_order(typed_id)
        if myOrder is None:
            self.text_report.setHtml('')
            self.showMessage('There is no order with the number ' + str(typed_id) + '.', True)
            return

        if myOrder.getPaymentStatus() != PAYMENT_PAID:
            self.text_report.setHtml('')
            self.showMessage('Order ' + str(typed_id) + ' is not paid yet: it has no receipt.', True)
            return

        # the receipt is the bill stored on the day of the payment
        bill_list = database_manager.load_order_bill(typed_id)
        self.text_report.setHtml(build_bill_html(myOrder, bill_list, True))
        self.showMessage('Receipt of order ' + str(typed_id) + '.', False)

    def showAllCustomers(self):
        row_list = []
        total_active = 0
        for myCustomer in database_manager.load_customers():
            if myCustomer.isActive():
                total_active = total_active + 1
            row_list.append([myCustomer.getPersonId(), myCustomer.getFullName(),
                             myCustomer.getPhone(), myCustomer.getEmail(),
                             myCustomer.getAddress(), myCustomer.getDeliveryAddress(),
                             myCustomer.getStatus(),
                             len(database_manager.load_customer_orders(myCustomer.getPersonId()))])

        html_text = '<h3>All the customers</h3>' + self.buildTable(
            ['Number', 'Name', 'Phone', 'Email', 'Home address', 'Delivery address',
             'Status', 'Orders'],
            ['right', 'left', 'left', 'left', 'left', 'left', 'left', 'right'], row_list)
        self.text_report.setHtml(html_text)
        self.showMessage(str(len(row_list)) + ' customer(s), ' + str(total_active)
                         + ' active and ' + str(len(row_list) - total_active)
                         + ' inactive.', False)

    # summary report: the paid bills grouped by month, each amount of
    # the bill_detail table added to the column of its group of charges
    def showSales(self):
        month_list = []
        summary_list = []

        for myBillDetail in database_manager.load_bill_details():
            month_text = (str(myBillDetail.getYear()) + '-'
                          + format(myBillDetail.getMonth(), '02d'))
            if month_text not in month_list:
                month_list.append(month_text)
                # number of bills, subtotal, fees, taxes, total
                summary_list.append([0, 0.0, 0.0, 0.0, 0.0])
            summary = summary_list[month_list.index(month_text)]

            charge_no = myBillDetail.getChargeNo()
            if charge_no == CHARGE_SUBTOTAL:
                summary[0] = summary[0] + 1
                summary[1] = summary[1] + myBillDetail.getAmount()
            elif charge_no == CHARGE_TOTAL:
                summary[4] = summary[4] + myBillDetail.getAmount()
            elif charge_no >= CHARGE_DELIVERY:
                summary[2] = summary[2] + myBillDetail.getAmount()
            elif charge_no >= CHARGE_GST:
                summary[3] = summary[3] + myBillDetail.getAmount()

        row_list = []
        grand_total = [0, 0.0, 0.0, 0.0, 0.0]
        for position in range(len(month_list)):
            summary = summary_list[position]
            for column in range(5):
                grand_total[column] = grand_total[column] + summary[column]
            row_list.append([month_list[position], summary[0],
                             format(summary[1], '.2f') + ' $', format(summary[2], '.2f') + ' $',
                             format(summary[3], '.2f') + ' $', format(summary[4], '.2f') + ' $'])
        row_list.append(['<b>Total</b>', '<b>' + str(grand_total[0]) + '</b>',
                         '<b>' + format(grand_total[1], '.2f') + ' $</b>',
                         '<b>' + format(grand_total[2], '.2f') + ' $</b>',
                         '<b>' + format(grand_total[3], '.2f') + ' $</b>',
                         '<b>' + format(grand_total[4], '.2f') + ' $</b>'])

        html_text = '<h3>Sales summary by month, paid orders</h3>' + self.buildTable(
            ['Month', 'Paid orders', 'Subtotal', 'Fees', 'Taxes', 'Total'],
            ['left', 'right', 'right', 'right', 'right', 'right'], row_list)
        self.text_report.setHtml(html_text)
        self.showMessage(str(len(month_list)) + ' month(s) with sales.', False)

    # exception report: only the items whose stock reached the level typed
    def showLowStock(self):
        try:
            stock_level = int(self.field_value.text())
        except ValueError:
            self.text_report.setHtml('')
            self.showMessage('The stock level must be a whole number, for example 5.', True)
            return

        row_list = []
        for myProduct in database_manager.load_products():
            if myProduct.getStockQty() <= stock_level:
                if myProduct.isAvailable():
                    remark = 'Low'
                else:
                    remark = '<b>Out of stock</b>'
                row_list.append([myProduct.getProductCode(), myProduct.getProductName(),
                                 myProduct.getCategory(),
                                 format(myProduct.calculateDisplayPrice(), '.2f') + ' $',
                                 myProduct.getStockQty(), remark])

        html_text = ('<h3>Items with a stock of ' + str(stock_level) + ' or less</h3>'
                     + self.buildTable(['Code', 'Item', 'Category', 'Price before taxes', 'Stock',
                                        'Remark'],
                                       ['left', 'left', 'left', 'right', 'right', 'left'],
                                       row_list))
        self.text_report.setHtml(html_text)
        self.showMessage(str(len(row_list)) + ' item(s) to reorder.', False)

    # exception report: only the orders that are not paid yet
    def showUnpaidOrders(self):
        unpaid_list = []
        for myOrder in database_manager.load_orders():
            if myOrder.getPaymentStatus() != PAYMENT_PAID:
                unpaid_list.append(myOrder)
        self.showOrderList(unpaid_list, 'Unpaid orders')

    def showStaff(self):
        row_list = []
        for myStaff in database_manager.load_staff():
            row_list.append([myStaff.getPersonId(), myStaff.getFullName(),
                             myStaff.getPosition(), myStaff.getUsername(),
                             myStaff.getAccessLevel(), myStaff.getPhone(), myStaff.getEmail()])

        html_text = '<h3>The staff</h3>' + self.buildTable(
            ['Number', 'Name', 'Position', 'Username', 'Access level', 'Phone', 'Email'],
            ['right', 'left', 'left', 'left', 'left', 'left', 'left'], row_list)
        self.text_report.setHtml(html_text)
        self.showMessage(str(len(row_list)) + ' employee(s).', False)


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)

    # started alone, the form shows the management reports of the first staff account
    database_manager.create_default_data()
    first_staff = database_manager.load_staff()[0]

    # create the window of the report form
    window = ReportForm(first_staff, True)
    window.resize(1000, 620)
    window.show()

    app.exec()


# the form is started alone only when this module is the one executed
if __name__ == '__main__':
    main()
