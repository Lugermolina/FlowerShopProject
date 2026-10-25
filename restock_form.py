# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Oct 24, 2026 for iteration 3
Algorithm:
Class: Python Teams online class
Inputs: item selected in the catalog, supplier selected, quantity received, unit cost,
the button pressed
Processing: validation of the entered values, instantiation of a Restock object with
the date of the day, save_restock() of the database_manager module, which adds the
restock and raises the stock of the item with one commit, total cost of the restocks
Outputs: the restock stored in the restock table, the stock updated in the product
table, the history of the restocks displayed in a table with their total cost, a
confirmation or an error message displayed on the form
"""
import sys
import datetime

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QComboBox, QGridLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QAbstractItemView)

import database_manager
from supplier_template import Restock

COLUMN_TITLES = ['Number', 'Date', 'Code', 'Item', 'Supplier', 'Quantity', 'Unit cost',
                 'Total cost']


class RestockForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Flower Shop, restock')

        # the catalog and the suppliers offered in the lists, in the same sequence
        self.product_list = []
        self.supplier_list = []

        self.label_title = QLabel('Restock from suppliers')
        self.label_title.setObjectName('title')
        self.label_product = QLabel('Item:')
        self.label_supplier = QLabel('Supplier:')
        self.label_quantity = QLabel('Quantity received:')
        self.label_unit_cost = QLabel('Unit cost:')
        self.label_date = QLabel('Date:')
        self.label_date_value = QLabel(str(datetime.date.today()))
        self.label_total_cost = QLabel('')
        self.label_message = QLabel('')

        self.combo_product = QComboBox()
        self.combo_supplier = QComboBox()
        self.field_quantity = QLineEdit()
        self.field_unit_cost = QLineEdit()
        self.field_quantity.setPlaceholderText('6')
        self.field_unit_cost.setPlaceholderText('18.50')
        self.field_quantity.setFixedWidth(120)
        self.field_unit_cost.setFixedWidth(120)

        self.button_add = QPushButton('Add')
        self.button_clear = QPushButton('Clear')

        self.table_restocks = QTableWidget()
        self.table_restocks.setColumnCount(len(COLUMN_TITLES))
        self.table_restocks.setHorizontalHeaderLabels(COLUMN_TITLES)
        self.table_restocks.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_restocks.setAlternatingRowColors(True)

        self.buildLayout()

        # connect the signal (event) to the slot (action) method of this class
        self.button_add.clicked.connect(self.addRestock)
        self.button_clear.clicked.connect(self.clearForm)

        self.loadLists()
        self.showRestocks()

    def buildLayout(self):
        grid = QGridLayout()
        grid.setColumnStretch(2, 1)

        grid.addWidget(self.label_title, 0, 0, 1, 3)
        grid.addWidget(self.label_product, 1, 0)
        grid.addWidget(self.combo_product, 1, 1, 1, 2)
        grid.addWidget(self.label_supplier, 2, 0)
        grid.addWidget(self.combo_supplier, 2, 1, 1, 2)
        grid.addWidget(self.label_quantity, 3, 0)
        grid.addWidget(self.field_quantity, 3, 1)
        grid.addWidget(self.label_unit_cost, 4, 0)
        grid.addWidget(self.field_unit_cost, 4, 1)
        grid.addWidget(self.label_date, 5, 0)
        grid.addWidget(self.label_date_value, 5, 1)

        row_buttons = QHBoxLayout()
        row_buttons.addWidget(self.button_add)
        row_buttons.addWidget(self.button_clear)
        row_buttons.addStretch()

        grid.addLayout(row_buttons, 6, 1, 1, 2)
        grid.addWidget(self.label_message, 7, 0, 1, 3)
        grid.addWidget(self.table_restocks, 8, 0, 1, 3)
        grid.addWidget(self.label_total_cost, 9, 0, 1, 3)

        self.setLayout(grid)

    def showMessage(self, message, is_error):
        self.label_message.setText(message)
        if is_error:
            self.label_message.setStyleSheet('color: #B22222;')
        else:
            self.label_message.setStyleSheet('color: #1F7A40;')

    # the lists are read again after every restock, so the stock shown is current
    def loadLists(self):
        product_index = self.combo_product.currentIndex()
        supplier_index = self.combo_supplier.currentIndex()

        self.product_list = database_manager.load_products()
        self.combo_product.clear()
        for myProduct in self.product_list:
            self.combo_product.addItem(myProduct.getProductCode() + ', '
                                       + myProduct.getProductName() + ', '
                                       + str(myProduct.getStockQty()) + ' in stock')

        self.supplier_list = database_manager.load_suppliers()
        self.combo_supplier.clear()
        for mySupplier in self.supplier_list:
            self.combo_supplier.addItem(str(mySupplier.getSupplierId()) + ', '
                                        + mySupplier.getSupplierName())

        if product_index > 0:
            self.combo_product.setCurrentIndex(product_index)
        if supplier_index > 0:
            self.combo_supplier.setCurrentIndex(supplier_index)

    def getProductName(self, product_code):
        for myProduct in self.product_list:
            if myProduct.getProductCode() == product_code:
                return myProduct.getProductName()
        return ''

    def getSupplierName(self, supplier_id):
        for mySupplier in self.supplier_list:
            if mySupplier.getSupplierId() == supplier_id:
                return mySupplier.getSupplierName()
        return ''

    def showRestocks(self):
        restock_list = database_manager.load_restocks()
        self.table_restocks.setRowCount(len(restock_list))

        total_cost = 0.0
        row = 0
        for myRestock in restock_list:
            self.table_restocks.setItem(row, 0, QTableWidgetItem(str(myRestock.getRestockId())))
            self.table_restocks.setItem(row, 1, QTableWidgetItem(myRestock.getRestockDate()))
            self.table_restocks.setItem(row, 2, QTableWidgetItem(myRestock.getProductCode()))
            self.table_restocks.setItem(row, 3, QTableWidgetItem(
                self.getProductName(myRestock.getProductCode())))
            self.table_restocks.setItem(row, 4, QTableWidgetItem(
                self.getSupplierName(myRestock.getSupplierId())))
            self.table_restocks.setItem(row, 5, QTableWidgetItem(str(myRestock.getQuantity())))
            self.table_restocks.setItem(row, 6, QTableWidgetItem(
                format(myRestock.getUnitCost(), '.2f') + ' $'))
            self.table_restocks.setItem(row, 7, QTableWidgetItem(
                format(myRestock.calculateCost(), '.2f') + ' $'))
            total_cost = total_cost + myRestock.calculateCost()
            row = row + 1

        self.table_restocks.resizeColumnsToContents()
        self.label_total_cost.setText(str(len(restock_list)) + ' restock(s), total cost '
                                      + format(total_cost, '.2f') + ' $')

    def clearForm(self):
        self.field_quantity.setText('')
        self.field_unit_cost.setText('')
        self.combo_product.setCurrentIndex(0)
        self.combo_supplier.setCurrentIndex(0)
        self.showMessage('', False)

    def addRestock(self):
        if len(self.product_list) == 0 or len(self.supplier_list) == 0:
            self.showMessage('The catalog and the list of suppliers must hold at least one '
                             'record.', True)
            return

        try:
            new_quantity = int(self.field_quantity.text())
            new_unit_cost = float(self.field_unit_cost.text())
        except ValueError:
            self.showMessage('The quantity must be a whole number, for example 6, and the unit '
                             'cost a number, for example 18.50.', True)
            return

        if new_quantity <= 0 or new_unit_cost <= 0:
            self.showMessage('The quantity and the unit cost must be above zero.', True)
            return

        myProduct = self.product_list[self.combo_product.currentIndex()]
        mySupplier = self.supplier_list[self.combo_supplier.currentIndex()]

        myRestock = Restock(database_manager.next_restock_id(), myProduct.getProductCode(),
                            mySupplier.getSupplierId(), str(datetime.date.today()),
                            new_quantity, new_unit_cost)
        database_manager.save_restock(myRestock)

        self.field_quantity.setText('')
        self.field_unit_cost.setText('')
        self.loadLists()
        self.showRestocks()
        self.showMessage('Restock ' + str(myRestock.getRestockId()) + ': '
                         + str(new_quantity) + ' x ' + myProduct.getProductName() + ' from '
                         + mySupplier.getSupplierName() + ', cost '
                         + format(myRestock.calculateCost(), '.2f') + ' $; the stock is now '
                         + str(myProduct.getStockQty() + new_quantity) + '.', False)


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)

    # create the window of the restock form
    window = RestockForm()
    window.resize(900, 560)
    window.show()

    app.exec()


# the form is started alone only when this module is the one executed
if __name__ == '__main__':
    main()
