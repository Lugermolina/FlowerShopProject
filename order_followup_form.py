# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Oct 24, 2026 for iteration 3
Algorithm:
Class: Python Teams online class
Inputs: the list of orders selected (all open orders, to prepare, ready, due today),
the order selected in the table, the button pressed
Processing: reading of the open orders by pickup or delivery date through the
database_manager module, selection of the orders of the list chosen, comparison of
each date with the date of the day, change of the status of the selected order to the
next one (New, Ready, Completed)
Outputs: the open orders displayed in a table, colored by status, with the late orders
in red, the status updated in the customer_order table, a confirmation or an error
message displayed on the form
"""
import sys
import datetime

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QComboBox,
                             QGridLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QAbstractItemView)

import database_manager
from order_template import STATUS_NEW, STATUS_READY, STATUS_COMPLETED, PAYMENT_UNPAID

LIST_ALL_OPEN = 'All open orders'
LIST_TO_PREPARE = 'To prepare (New)'
LIST_READY = 'Ready for pickup or delivery'
LIST_DUE_TODAY = 'Due today'

COLUMN_TITLES = ['Order', 'Date', 'Type', 'Customer', 'Phone', 'Delivery address', 'Items',
                 'Status', 'Payment']

COLOR_NEW = '#FFF4D6'
COLOR_READY = '#E3F4E8'
COLOR_LATE = '#B22222'


class OrderFollowUpForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Flower Shop, order follow-up')

        # the orders displayed in the table, in the same sequence as its rows
        self.shown_order_list = []

        self.label_title = QLabel('Order follow-up')
        self.label_title.setObjectName('title')
        self.label_list = QLabel('Show:')
        self.label_legend = QLabel('Yellow: to prepare. Green: ready. Red date: late.')
        self.label_message = QLabel('')

        self.combo_list = QComboBox()
        self.combo_list.addItem(LIST_ALL_OPEN)
        self.combo_list.addItem(LIST_TO_PREPARE)
        self.combo_list.addItem(LIST_READY)
        self.combo_list.addItem(LIST_DUE_TODAY)

        self.button_show = QPushButton('Show')
        self.button_next_status = QPushButton('Move to next status')

        self.table_orders = QTableWidget()
        self.table_orders.setColumnCount(len(COLUMN_TITLES))
        self.table_orders.setHorizontalHeaderLabels(COLUMN_TITLES)
        self.table_orders.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_orders.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.buildLayout()

        # connect the signal (event) to the slot (action) method of this class
        self.button_show.clicked.connect(self.showOrders)
        self.combo_list.currentIndexChanged.connect(self.showOrders)
        self.button_next_status.clicked.connect(self.moveToNextStatus)

        self.showOrders()

    def buildLayout(self):
        grid = QGridLayout()
        grid.setColumnStretch(3, 1)

        grid.addWidget(self.label_title, 0, 0, 1, 4)
        grid.addWidget(self.label_list, 1, 0)
        grid.addWidget(self.combo_list, 1, 1)
        grid.addWidget(self.button_show, 1, 2)
        grid.addWidget(self.table_orders, 2, 0, 1, 4)

        row_buttons = QHBoxLayout()
        row_buttons.addWidget(self.button_next_status)
        row_buttons.addWidget(self.label_legend)
        row_buttons.addStretch()

        grid.addLayout(row_buttons, 3, 0, 1, 4)
        grid.addWidget(self.label_message, 4, 0, 1, 4)

        self.setLayout(grid)

    def showMessage(self, message, is_error):
        self.label_message.setText(message)
        if is_error:
            self.label_message.setStyleSheet('color: #B22222;')
        else:
            self.label_message.setStyleSheet('color: #1F7A40;')

    # the items of the order in one text, so the order can be prepared from the list
    def getItemsText(self, myOrder):
        items_text = ''
        for myItem in myOrder.getItemList():
            if items_text != '':
                items_text = items_text + '; '
            items_text = items_text + str(myItem.getQuantity()) + ' x ' + myItem.getProductName()
        return items_text

    def showOrders(self):
        selected_list = self.combo_list.currentText()
        today_text = str(datetime.date.today())

        self.shown_order_list = []
        for myOrder in database_manager.load_open_orders():
            keep_order = True
            if selected_list == LIST_TO_PREPARE and myOrder.getOrderStatus() != STATUS_NEW:
                keep_order = False
            if selected_list == LIST_READY and myOrder.getOrderStatus() != STATUS_READY:
                keep_order = False
            if selected_list == LIST_DUE_TODAY and myOrder.getDeliveryDate() != today_text:
                keep_order = False
            if keep_order:
                self.shown_order_list.append(myOrder)

        self.table_orders.setRowCount(len(self.shown_order_list))

        total_late = 0
        row = 0
        for myOrder in self.shown_order_list:
            customer_name = 'Walk-in'
            customer_phone = ''
            if myOrder.getCustomerId() is not None:
                myCustomer = database_manager.find_customer(myOrder.getCustomerId())
                customer_name = myCustomer.getFullName()
                customer_phone = myCustomer.getPhone()

            item_list = [QTableWidgetItem(str(myOrder.getOrderId())),
                         QTableWidgetItem(myOrder.getDeliveryDate()),
                         QTableWidgetItem(myOrder.getOrderType()),
                         QTableWidgetItem(customer_name),
                         QTableWidgetItem(customer_phone),
                         QTableWidgetItem(myOrder.getDeliveryAddress()),
                         QTableWidgetItem(self.getItemsText(myOrder)),
                         QTableWidgetItem(myOrder.getOrderStatus()),
                         QTableWidgetItem(myOrder.getPaymentStatus())]

            # the row takes the color of the status, the date turns red when it is past
            if myOrder.getOrderStatus() == STATUS_NEW:
                row_color = QColor(COLOR_NEW)
            else:
                row_color = QColor(COLOR_READY)

            for column in range(len(item_list)):
                item_list[column].setBackground(row_color)
                self.table_orders.setItem(row, column, item_list[column])

            if myOrder.getDeliveryDate() < today_text:
                item_list[1].setText(myOrder.getDeliveryDate() + ' (late)')
                item_list[1].setForeground(QColor(COLOR_LATE))
                total_late = total_late + 1

            row = row + 1

        self.table_orders.resizeColumnsToContents()

        message = str(len(self.shown_order_list)) + ' order(s) in the list'
        if total_late > 0:
            message = message + ', ' + str(total_late) + ' late'
        self.showMessage(message + '.', False)

    # New becomes Ready, Ready becomes Completed; a completed order leaves the list
    def moveToNextStatus(self):
        row = self.table_orders.currentRow()
        if row < 0:
            self.showMessage('Click an order in the list first.', True)
            return

        myOrder = self.shown_order_list[row]
        if myOrder.getOrderStatus() == STATUS_NEW:
            new_status = STATUS_READY
        else:
            new_status = STATUS_COMPLETED

        database_manager.update_order_status(myOrder.getOrderId(), new_status)

        self.showOrders()
        message = 'Order ' + str(myOrder.getOrderId()) + ' is now ' + new_status + '.'
        if new_status == STATUS_COMPLETED and myOrder.getPaymentStatus() == PAYMENT_UNPAID:
            message = message + ' It is still unpaid: bill it in Billing.'
        self.showMessage(message, False)


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)

    # create the window of the order follow-up form
    window = OrderFollowUpForm()
    window.resize(1100, 520)
    window.show()

    app.exec()


# the form is started alone only when this module is the one executed
if __name__ == '__main__':
    main()
