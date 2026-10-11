# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Starting on Oct 11, 2026
Algorithm:
Class: Python Teams online class
Inputs: order number, customer number or the walk-in check box, type of order (pickup
or delivery), delivery address, pickup or delivery date, order status, item selected
in the catalog, quantity, the button pressed
Processing: search of the customer, validation of the entered values, check of each
quantity against the stock, instantiation of Order and OrderItem objects, add, search,
update and delete of an order through the file_manager module, adjustment of the stock
of the catalog
Outputs: the order stored in orders.txt and its lines in order_items.txt, the stock
updated in products.txt, the order found displayed on the form with its lines and its
subtotal, a confirmation or an error message displayed on the form
"""
import sys
import datetime

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QComboBox, QCheckBox, QGridLayout, QHBoxLayout, QMessageBox,
                             QTableWidget, QTableWidgetItem, QAbstractItemView)

import file_manager
from order_template import (Order, OrderItem, ORDER_PICKUP, ORDER_DELIVERY, STATUS_NEW,
                            STATUS_READY, STATUS_COMPLETED, PAYMENT_UNPAID, PAYMENT_PAID)

COLUMN_TITLES = ['Code', 'Item', 'Quantity', 'Price to pay', 'Line total']


class OrderForm(QWidget):
    # the employee who logged in is received as a parameter and recorded on every
    # new order
    def __init__(self, current_staff=None):
        super().__init__()
        self.setWindowTitle('Flower Shop, orders')
        self.current_staff = current_staff

        # the order displayed after a search, None while a new order is typed;
        # update and delete only act on this order
        self.loadedOrder = None
        # the lines of the order on the form, before they are saved
        self.item_list = []
        # the catalog items in the same sequence as the list of the form
        self.product_list = []

        self.label_title = QLabel('Orders')
        self.label_title.setStyleSheet('font-weight: bold;')
        self.label_order_id = QLabel('Order number:')
        self.label_order_info = QLabel('')
        self.label_customer_id = QLabel('Customer number:')
        self.label_customer_info = QLabel('')
        self.label_order_type = QLabel('Type:')
        self.label_delivery_date = QLabel('Pickup or delivery date:')
        self.label_delivery_address = QLabel('Delivery address:')
        self.label_order_status = QLabel('Order status:')
        self.label_product = QLabel('Item:')
        self.label_quantity = QLabel('Quantity:')
        self.label_subtotal = QLabel('Subtotal: 0.00 $')
        self.label_subtotal.setStyleSheet('font-weight: bold;')
        self.label_message = QLabel('')

        self.field_order_id = QLineEdit()
        self.field_customer_id = QLineEdit()
        self.field_delivery_date = QLineEdit()
        self.field_delivery_address = QLineEdit()
        self.field_quantity = QLineEdit()

        self.field_order_id.setPlaceholderText('type a number to search; a new order gets '
                                               'a number automatically')
        self.field_customer_id.setPlaceholderText('1001')

        # a walk-in customer buys at the counter without being registered
        self.check_walk_in = QCheckBox('Walk-in customer (pickup, no customer record)')
        self.field_delivery_date.setPlaceholderText('2026-10-15')
        self.field_quantity.setPlaceholderText('1')
        self.field_quantity.setFixedWidth(80)

        self.combo_order_type = QComboBox()
        self.combo_order_type.addItem(ORDER_PICKUP)
        self.combo_order_type.addItem(ORDER_DELIVERY)

        self.combo_order_status = QComboBox()
        self.combo_order_status.addItem(STATUS_NEW)
        self.combo_order_status.addItem(STATUS_READY)
        self.combo_order_status.addItem(STATUS_COMPLETED)

        self.combo_product = QComboBox()

        self.table_items = QTableWidget()
        self.table_items.setColumnCount(len(COLUMN_TITLES))
        self.table_items.setHorizontalHeaderLabels(COLUMN_TITLES)
        self.table_items.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_items.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.button_find_customer = QPushButton('Find customer')
        self.button_add_line = QPushButton('Add line')
        self.button_remove_line = QPushButton('Remove selected line')
        self.button_add = QPushButton('Add')
        self.button_search = QPushButton('Search')
        self.button_update = QPushButton('Update')
        self.button_delete = QPushButton('Delete')
        self.button_clear = QPushButton('Clear')

        self.buildLayout()

        # connect the signal (event) to the slot (action) method of this class
        self.combo_order_type.currentIndexChanged.connect(self.orderTypeChanged)
        self.check_walk_in.stateChanged.connect(self.walkInChanged)
        self.button_find_customer.clicked.connect(self.findCustomer)
        self.button_add_line.clicked.connect(self.addLine)
        self.button_remove_line.clicked.connect(self.removeLine)
        self.button_add.clicked.connect(self.addOrder)
        self.button_search.clicked.connect(self.searchOrder)
        self.button_update.clicked.connect(self.updateOrder)
        self.button_delete.clicked.connect(self.deleteOrder)
        self.button_clear.clicked.connect(self.clearForm)

        self.clearFields()

    def buildLayout(self):
        grid = QGridLayout()
        grid.setColumnStretch(3, 1)

        grid.addWidget(self.label_title, 0, 0, 1, 4)
        grid.addWidget(self.label_order_id, 1, 0)
        grid.addWidget(self.field_order_id, 1, 1, 1, 2)
        grid.addWidget(self.label_order_info, 1, 3)
        grid.addWidget(self.label_customer_id, 2, 0)
        grid.addWidget(self.field_customer_id, 2, 1)
        grid.addWidget(self.button_find_customer, 2, 2)
        grid.addWidget(self.label_customer_info, 2, 3)
        grid.addWidget(self.check_walk_in, 3, 1, 1, 3)
        grid.addWidget(self.label_order_type, 4, 0)
        grid.addWidget(self.combo_order_type, 4, 1)
        grid.addWidget(self.label_delivery_date, 4, 2)
        grid.addWidget(self.field_delivery_date, 4, 3)
        grid.addWidget(self.label_delivery_address, 5, 0)
        grid.addWidget(self.field_delivery_address, 5, 1, 1, 3)
        grid.addWidget(self.label_order_status, 6, 0)
        grid.addWidget(self.combo_order_status, 6, 1)

        row_line = QHBoxLayout()
        row_line.addWidget(self.combo_product)
        row_line.addWidget(self.label_quantity)
        row_line.addWidget(self.field_quantity)
        row_line.addWidget(self.button_add_line)
        row_line.addWidget(self.button_remove_line)
        row_line.addStretch()

        grid.addWidget(self.label_product, 7, 0)
        grid.addLayout(row_line, 7, 1, 1, 3)
        grid.addWidget(self.table_items, 8, 0, 1, 4)
        grid.addWidget(self.label_subtotal, 9, 3)

        row_buttons = QHBoxLayout()
        row_buttons.addWidget(self.button_add)
        row_buttons.addWidget(self.button_search)
        row_buttons.addWidget(self.button_update)
        row_buttons.addWidget(self.button_delete)
        row_buttons.addWidget(self.button_clear)
        row_buttons.addStretch()

        grid.addLayout(row_buttons, 10, 1, 1, 3)
        grid.addWidget(self.label_message, 11, 0, 1, 4)
        grid.setRowStretch(8, 1)

        self.setLayout(grid)

    def showMessage(self, message, is_error):
        self.label_message.setText(message)
        if is_error:
            self.label_message.setStyleSheet('color: #B22222;')
        else:
            self.label_message.setStyleSheet('color: #1F7A40;')

    # the list of items is read from the catalog again after every change of stock
    def loadProducts(self):
        self.product_list = file_manager.load_products()
        self.combo_product.clear()
        for myProduct in self.product_list:
            self.combo_product.addItem(myProduct.getProductCode() + ', '
                                       + myProduct.getProductName() + ', '
                                       + format(myProduct.calculateDisplayPrice(), '.2f')
                                       + ' $, ' + str(myProduct.getStockQty()) + ' in stock')

    # a walk-in order has no customer number and is always a pickup, because a
    # delivery needs the address and the phone of a registered customer
    def walkInChanged(self):
        is_walk_in = self.check_walk_in.isChecked()
        self.field_customer_id.setEnabled(not is_walk_in)
        self.button_find_customer.setEnabled(not is_walk_in)
        self.combo_order_type.setEnabled(not is_walk_in)
        if is_walk_in:
            self.field_customer_id.setText('')
            self.label_customer_info.setText('Walk-in customer')
            self.combo_order_type.setCurrentText(ORDER_PICKUP)
        else:
            self.label_customer_info.setText('')

    def orderTypeChanged(self):
        is_delivery = self.combo_order_type.currentText() == ORDER_DELIVERY
        self.field_delivery_address.setEnabled(is_delivery)
        if not is_delivery:
            self.field_delivery_address.setText('')

    def showLines(self):
        self.table_items.setRowCount(len(self.item_list))

        row = 0
        subtotal = 0.0
        for myItem in self.item_list:
            self.table_items.setItem(row, 0, QTableWidgetItem(myItem.getProductCode()))
            self.table_items.setItem(row, 1, QTableWidgetItem(myItem.getProductName()))
            self.table_items.setItem(row, 2, QTableWidgetItem(str(myItem.getQuantity())))
            self.table_items.setItem(row, 3, QTableWidgetItem(f'{myItem.calculatePriceToPay():.2f} $'))
            self.table_items.setItem(row, 4, QTableWidgetItem(f'{myItem.calculateLineTotal():.2f} $'))
            subtotal = subtotal + myItem.calculateLineTotal()
            row = row + 1

        self.table_items.resizeColumnsToContents()
        self.label_subtotal.setText('Subtotal: ' + format(subtotal, '.2f') + ' $')

    def clearFields(self):
        self.loadedOrder = None
        self.item_list = []
        self.field_order_id.setText('')
        self.label_order_info.setText('')
        self.field_customer_id.setText('')
        self.check_walk_in.setEnabled(True)
        self.check_walk_in.setChecked(False)
        self.walkInChanged()
        self.combo_order_type.setCurrentIndex(0)
        self.field_delivery_date.setText('')
        self.field_delivery_address.setText('')
        self.field_quantity.setText('')
        # the status of a new order is always New; it changes with Update
        self.combo_order_status.setCurrentIndex(0)
        self.combo_order_status.setEnabled(False)
        self.orderTypeChanged()
        self.loadProducts()
        self.showLines()

    def clearForm(self):
        self.clearFields()
        self.showMessage('', False)

    # the method returns True only when the typed number is the number of an
    # active customer
    def findCustomer(self):
        typed_text = self.field_customer_id.text().strip()
        if typed_text == '':
            self.label_customer_info.setText('')
            self.showMessage('Type the customer number, for example 1001.', True)
            return False

        try:
            typed_id = int(typed_text)
        except ValueError:
            self.label_customer_info.setText('')
            self.showMessage('The customer number must be a number, for example 1001.', True)
            return False

        myCustomer = file_manager.find_customer(typed_id)
        if myCustomer is None:
            self.label_customer_info.setText('')
            self.showMessage('There is no customer with the number ' + str(typed_id) + '.', True)
            return False

        if not myCustomer.isActive():
            self.label_customer_info.setText('')
            self.showMessage('Customer ' + str(typed_id) + ' is inactive. Update the customer '
                             'record to make it active again.', True)
            return False

        self.label_customer_info.setText(myCustomer.getFullName() + ', ' + myCustomer.getPhone())
        if (self.combo_order_type.currentText() == ORDER_DELIVERY
                and self.field_delivery_address.text().strip() == ''):
            self.field_delivery_address.setText(myCustomer.getDeliveryAddress())
        self.showMessage('Customer ' + str(typed_id) + ' found.', False)
        return True

    # the lines of a paid order are part of its bill, so they cannot change anymore
    def canChangeLines(self):
        if self.loadedOrder is not None and self.loadedOrder.getPaymentStatus() == PAYMENT_PAID:
            self.showMessage('Order ' + str(self.loadedOrder.getOrderId())
                             + ' is paid: its lines cannot be changed.', True)
            return False
        return True

    def getLineQuantity(self, line_list, product_code):
        quantity = 0
        for myItem in line_list:
            if myItem.getProductCode() == product_code:
                quantity = quantity + myItem.getQuantity()
        return quantity

    # the quantity that can still be ordered: the stock, plus what the saved order
    # already holds of the item, minus what the lines on the form hold of it
    def getAvailableQuantity(self, myProduct):
        available = myProduct.getStockQty()
        if self.loadedOrder is not None:
            available = available + self.getLineQuantity(self.loadedOrder.getItemList(),
                                                         myProduct.getProductCode())
        return available - self.getLineQuantity(self.item_list, myProduct.getProductCode())

    def addLine(self):
        if not self.canChangeLines():
            return

        if self.combo_product.currentIndex() < 0:
            self.showMessage('The catalog holds no item.', True)
            return
        myProduct = self.product_list[self.combo_product.currentIndex()]

        try:
            new_quantity = int(self.field_quantity.text())
        except ValueError:
            self.showMessage('The quantity must be a whole number, for example 2.', True)
            return

        if new_quantity <= 0:
            self.showMessage('The quantity must be above zero.', True)
            return

        available = self.getAvailableQuantity(myProduct)
        if new_quantity > available:
            self.showMessage('Only ' + str(available) + ' of ' + myProduct.getProductName()
                             + ' can be added: the stock is not enough.', True)
            return

        # an item already on the order gets a higher quantity instead of a second line
        line_found = False
        for myItem in self.item_list:
            if myItem.getProductCode() == myProduct.getProductCode():
                myItem.setQuantity(myItem.getQuantity() + new_quantity)
                line_found = True

        if not line_found:
            self.item_list.append(OrderItem(None, myProduct.getProductCode(),
                                            myProduct.getProductName(), new_quantity,
                                            myProduct.getUnitPrice(),
                                            myProduct.getExtraCharge()))

        self.field_quantity.setText('')
        self.showLines()
        self.showMessage(str(new_quantity) + ' x ' + myProduct.getProductName()
                         + ' added to the order.', False)

    def removeLine(self):
        if not self.canChangeLines():
            return

        selected_row = self.table_items.currentRow()
        if selected_row < 0 or selected_row >= len(self.item_list):
            self.showMessage('Select a line in the table first.', True)
            return

        removed_name = self.item_list[selected_row].getProductName()
        self.item_list.pop(selected_row)
        self.showLines()
        self.showMessage(removed_name + ' removed from the order.', False)

    # reading and validating the fields; the method returns an Order object holding
    # the lines of the form, or None after displaying the error
    def readOrder(self, order_id, staff_id, order_date, payment_status):
        new_order_type = self.combo_order_type.currentText()
        new_delivery_date = self.field_delivery_date.text().strip()
        new_delivery_address = self.field_delivery_address.text().strip()
        customer_text = self.field_customer_id.text().strip()

        # an order belongs to a registered customer, unless the walk-in box is checked
        new_customer_id = None
        if not self.check_walk_in.isChecked():
            if customer_text == '':
                self.showMessage('Type the customer number, or check the walk-in box for a '
                                 'pickup without a customer record.', True)
                return None
            if self.loadedOrder is None and not self.findCustomer():
                return None
            new_customer_id = int(customer_text)

        if new_order_type == ORDER_DELIVERY:
            if new_delivery_address == '':
                self.showMessage('A delivery needs a delivery address.', True)
                return None
        else:
            new_delivery_address = ''

        # the date is text in the format year-month-day
        try:
            new_delivery_date = str(datetime.date.fromisoformat(new_delivery_date))
        except ValueError:
            self.showMessage('The date must be written as year-month-day, for example '
                             '2026-10-15.', True)
            return None

        if new_delivery_date < order_date:
            self.showMessage('The pickup or delivery date cannot be before the date of the '
                             'order, ' + order_date + '.', True)
            return None

        if len(self.item_list) == 0:
            self.showMessage('Add at least one line to the order.', True)
            return None

        myOrder = Order(order_id, new_customer_id, staff_id, order_date, new_delivery_date,
                        new_order_type, new_delivery_address,
                        self.combo_order_status.currentText(), payment_status)
        for myItem in self.item_list:
            myItem.setOrderId(order_id)
            myOrder.addItem(myItem)
        return myOrder

    # the stock of every item changes by the difference between the lines saved
    # before and the new lines: it goes down when an order is added, comes back when
    # an order is deleted, and moves by the difference when an order is updated.
    # The method returns False, and changes nothing, when the stock is not enough
    def adjustStock(self, old_item_list, new_item_list):
        product_list = file_manager.load_products()

        for myProduct in product_list:
            difference = (self.getLineQuantity(new_item_list, myProduct.getProductCode())
                          - self.getLineQuantity(old_item_list, myProduct.getProductCode()))
            if difference > myProduct.getStockQty():
                self.showMessage('The stock of ' + myProduct.getProductName()
                                 + ' is not enough anymore: ' + str(myProduct.getStockQty())
                                 + ' left.', True)
                return False

        for myProduct in product_list:
            difference = (self.getLineQuantity(new_item_list, myProduct.getProductCode())
                          - self.getLineQuantity(old_item_list, myProduct.getProductCode()))
            myProduct.setStockQty(myProduct.getStockQty() - difference)

        file_manager.save_products(product_list)
        return True

    def addOrder(self):
        if self.loadedOrder is not None:
            self.showMessage('This order is already saved. Use Update to change it, or Clear '
                             'to add a new order.', True)
            return

        if self.current_staff is None:
            self.showMessage('Log in before adding an order.', True)
            return

        new_order_id = file_manager.next_order_id(file_manager.load_orders())
        today_text = str(datetime.date.today())

        myOrder = self.readOrder(new_order_id, self.current_staff.getPersonId(), today_text,
                                 PAYMENT_UNPAID)
        if myOrder is None:
            return

        if not self.adjustStock([], myOrder.getItemList()):
            return

        file_manager.save_order(myOrder)

        subtotal = myOrder.calculateSubtotal()
        self.clearFields()
        self.showMessage('Order ' + str(myOrder.getOrderId()) + ' saved, '
                         + myOrder.getOrderType() + ' on ' + myOrder.getDeliveryDate()
                         + ', subtotal ' + format(subtotal, '.2f') + ' $.', False)

    def searchOrder(self):
        try:
            typed_id = int(self.field_order_id.text())
        except ValueError:
            self.showMessage('Type the order number, for example 5001.', True)
            return

        myOrder = file_manager.find_order(typed_id)
        if myOrder is None:
            self.clearFields()
            self.showMessage('There is no order with the number ' + str(typed_id) + '.', True)
            return

        self.clearFields()
        self.loadedOrder = myOrder
        self.field_order_id.setText(str(myOrder.getOrderId()))

        staff_name = ''
        myStaff = file_manager.find_staff(myOrder.getStaffId())
        if myStaff is not None:
            staff_name = ', taken by ' + myStaff.getFullName()
        self.label_order_info.setText('Ordered on ' + myOrder.getOrderDate() + staff_name
                                      + ', ' + myOrder.getPaymentStatus())

        # the customer of a saved order cannot be changed
        self.check_walk_in.setChecked(myOrder.getCustomerId() is None)
        self.walkInChanged()
        self.check_walk_in.setEnabled(False)
        self.field_customer_id.setEnabled(False)
        self.button_find_customer.setEnabled(False)
        if myOrder.getCustomerId() is not None:
            self.field_customer_id.setText(str(myOrder.getCustomerId()))
            myCustomer = file_manager.find_customer(myOrder.getCustomerId())
            if myCustomer is not None:
                self.label_customer_info.setText(myCustomer.getFullName() + ', '
                                                 + myCustomer.getPhone())

        self.combo_order_type.setCurrentText(myOrder.getOrderType())
        self.field_delivery_date.setText(myOrder.getDeliveryDate())
        self.field_delivery_address.setText(myOrder.getDeliveryAddress())
        self.combo_order_status.setEnabled(True)
        self.combo_order_status.setCurrentText(myOrder.getOrderStatus())

        # the form works on a copy of the lines, so the saved lines stay available
        # to calculate the difference of stock on an update
        for myItem in myOrder.getItemList():
            self.item_list.append(OrderItem(myItem.getOrderId(), myItem.getProductCode(),
                                            myItem.getProductName(), myItem.getQuantity(),
                                            myItem.getUnitPrice(), myItem.getExtraCharge()))
        self.showLines()

        if not myOrder.isActive():
            self.showMessage('Order ' + str(myOrder.getOrderId())
                             + ' is completed and paid: it can only be consulted.', False)
        else:
            self.showMessage('Order ' + str(myOrder.getOrderId()) + ' found.', False)

    # update and delete are refused when the number in the field is not the one of
    # the order displayed, so an order is never changed by mistake
    def isOrderLoaded(self):
        if (self.loadedOrder is None
                or self.field_order_id.text().strip() != str(self.loadedOrder.getOrderId())):
            self.showMessage('Search the order by number first.', True)
            return False
        return True

    def updateOrder(self):
        if not self.isOrderLoaded():
            return

        oldOrder = self.loadedOrder
        if not oldOrder.isActive():
            self.showMessage('Order ' + str(oldOrder.getOrderId())
                             + ' is completed and paid: it cannot be changed.', True)
            return

        myOrder = self.readOrder(oldOrder.getOrderId(), oldOrder.getStaffId(),
                                 oldOrder.getOrderDate(), oldOrder.getPaymentStatus())
        if myOrder is None:
            return

        # the delivery fee is part of the bill, so the type is fixed once the order is paid
        if (oldOrder.getPaymentStatus() == PAYMENT_PAID
                and myOrder.getOrderType() != oldOrder.getOrderType()):
            self.showMessage('Order ' + str(oldOrder.getOrderId())
                             + ' is paid: its type cannot be changed.', True)
            return

        if not self.adjustStock(oldOrder.getItemList(), myOrder.getItemList()):
            return

        order_list = file_manager.load_orders()
        for position in range(len(order_list)):
            if order_list[position].getOrderId() == myOrder.getOrderId():
                order_list[position] = myOrder
        file_manager.save_orders(order_list)

        updated_id = myOrder.getOrderId()
        self.field_order_id.setText(str(updated_id))
        self.searchOrder()
        self.showMessage('Order ' + str(updated_id) + ' updated, status '
                         + myOrder.getOrderStatus() + ', subtotal '
                         + format(myOrder.calculateSubtotal(), '.2f') + ' $.', False)

    # an order can be deleted only while it is unpaid; its quantities come back
    # to the stock
    def deleteOrder(self):
        if not self.isOrderLoaded():
            return

        oldOrder = self.loadedOrder
        if oldOrder.getPaymentStatus() == PAYMENT_PAID:
            self.showMessage('Order ' + str(oldOrder.getOrderId())
                             + ' is paid and cannot be deleted.', True)
            return

        answer = QMessageBox.question(self, 'Delete order',
                                      'Delete order ' + str(oldOrder.getOrderId()) + '?')
        if answer != QMessageBox.StandardButton.Yes:
            return

        self.adjustStock(oldOrder.getItemList(), [])

        new_order_list = []
        for myOrder in file_manager.load_orders():
            if myOrder.getOrderId() != oldOrder.getOrderId():
                new_order_list.append(myOrder)
        file_manager.save_orders(new_order_list)

        self.clearFields()
        self.showMessage('Order ' + str(oldOrder.getOrderId())
                         + ' deleted, its items are back in stock.', False)


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)

    # started alone, the form records the orders under the first staff account
    file_manager.create_default_data()
    first_staff = file_manager.load_staff()[0]

    # create the window of the order form
    window = OrderForm(first_staff)
    window.resize(1000, 620)
    window.show()

    app.exec()


# the form is started alone only when this module is the one executed
if __name__ == '__main__':
    main()
