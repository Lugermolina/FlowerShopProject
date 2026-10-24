# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Starting on Oct 10, 2026, updating started on Oct 24, 2026 for iteration 3
Algorithm:
Class: Python Teams online class
Inputs: item code, type of item, name, category, unit price, stock, number of flowers
or pot size, the button pressed
Processing: validation of the entered values, generation of the item code,
instantiation of a Product, Bouquet or PottedPlant object, add, search, update and
delete of a record through the database_manager module, delete rule based on the
orders that hold the item and on its restocks
Outputs: the catalog record added to, changed in or removed from the product table, the
record found displayed in the fields, a confirmation or an error message displayed
on the form
"""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QComboBox, QGridLayout, QHBoxLayout, QMessageBox, QCompleter)

import database_manager
from product_template import Product, Bouquet, PottedPlant

TYPE_BOUQUET = 'Bouquet'
TYPE_POTTED_PLANT = 'Potted plant'
TYPE_OTHER = 'Other item'


class ProductForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Flower Shop, catalog')

        # the code of the item displayed after a search, None while the form is empty;
        # update and delete only act on this item
        self.loaded_product_code = None

        self.label_title = QLabel('Catalog')
        self.label_title.setStyleSheet('font-weight: bold;')
        self.label_code = QLabel('Item code:')
        self.label_type = QLabel('Type:')
        self.label_name = QLabel('Name:')
        self.label_category = QLabel('Category:')
        self.label_unit_price = QLabel('Unit price:')
        self.label_stock = QLabel('Stock:')
        self.label_extra_info = QLabel('Number of flowers:')
        self.label_price_to_pay = QLabel('')
        self.label_message = QLabel('')

        self.field_code = QLineEdit()
        self.field_name = QLineEdit()
        self.field_category = QLineEdit()
        self.field_unit_price = QLineEdit()
        self.field_stock = QLineEdit()
        self.field_extra_info = QLineEdit()

        self.field_code.setPlaceholderText('type a code to search; a new item gets its '
                                           'code automatically')
        self.field_category.setPlaceholderText('Bouquets')
        self.field_unit_price.setPlaceholderText('45.00')
        self.field_stock.setPlaceholderText('12')

        self.combo_type = QComboBox()
        self.combo_type.addItem(TYPE_BOUQUET)
        self.combo_type.addItem(TYPE_POTTED_PLANT)
        self.combo_type.addItem(TYPE_OTHER)

        self.button_add = QPushButton('Add')
        self.button_search = QPushButton('Search')
        self.button_update = QPushButton('Update')
        self.button_delete = QPushButton('Delete')
        self.button_clear = QPushButton('Clear')

        self.buildLayout()
        self.loadCategorySuggestions()

        # connect the signal (event) to the slot (action) method of this class
        self.combo_type.currentIndexChanged.connect(self.typeChanged)
        self.button_add.clicked.connect(self.addProduct)
        self.button_search.clicked.connect(self.searchProduct)
        self.button_update.clicked.connect(self.updateProduct)
        self.button_delete.clicked.connect(self.deleteProduct)
        self.button_clear.clicked.connect(self.clearForm)

    def buildLayout(self):
        grid = QGridLayout()
        grid.setColumnStretch(1, 1)

        grid.addWidget(self.label_title, 0, 0, 1, 2)
        grid.addWidget(self.label_code, 1, 0)
        grid.addWidget(self.field_code, 1, 1)
        grid.addWidget(self.label_type, 2, 0)
        grid.addWidget(self.combo_type, 2, 1)
        grid.addWidget(self.label_name, 3, 0)
        grid.addWidget(self.field_name, 3, 1)
        grid.addWidget(self.label_category, 4, 0)
        grid.addWidget(self.field_category, 4, 1)
        grid.addWidget(self.label_unit_price, 5, 0)
        grid.addWidget(self.field_unit_price, 5, 1)
        grid.addWidget(self.label_stock, 6, 0)
        grid.addWidget(self.field_stock, 6, 1)
        grid.addWidget(self.label_extra_info, 7, 0)
        grid.addWidget(self.field_extra_info, 7, 1)
        grid.addWidget(self.label_price_to_pay, 8, 1)

        row_buttons = QHBoxLayout()
        row_buttons.addWidget(self.button_add)
        row_buttons.addWidget(self.button_search)
        row_buttons.addWidget(self.button_update)
        row_buttons.addWidget(self.button_delete)
        row_buttons.addWidget(self.button_clear)
        row_buttons.addStretch()

        grid.addLayout(row_buttons, 9, 1)
        grid.addWidget(self.label_message, 10, 0, 1, 2)
        grid.setRowStretch(11, 1)

        self.setLayout(grid)

    # the categories already in the catalog are suggested while the user types, so
    # the same category is not written in two different ways
    def loadCategorySuggestions(self):
        category_list = []
        for myProduct in database_manager.load_products():
            if myProduct.getCategory() not in category_list:
                category_list.append(myProduct.getCategory())

        completer = QCompleter(category_list)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.field_category.setCompleter(completer)

    # the last field asks for what the selected type needs: the number of flowers of
    # a bouquet, the pot size of a potted plant, nothing for another item
    def typeChanged(self):
        selected_type = self.combo_type.currentText()
        self.field_extra_info.setEnabled(selected_type != TYPE_OTHER)

        if selected_type == TYPE_BOUQUET:
            self.label_extra_info.setText('Number of flowers:')
            self.field_extra_info.setPlaceholderText('12')
        elif selected_type == TYPE_POTTED_PLANT:
            self.label_extra_info.setText('Pot size:')
            self.field_extra_info.setPlaceholderText('15 cm')
        else:
            self.label_extra_info.setText('No extra information:')
            self.field_extra_info.setPlaceholderText('')
            self.field_extra_info.setText('')

    def showMessage(self, message, is_error):
        self.label_message.setText(message)
        if is_error:
            self.label_message.setStyleSheet('color: #B22222;')
        else:
            self.label_message.setStyleSheet('color: #1F7A40;')

    def clearFields(self):
        self.loaded_product_code = None
        self.field_code.setText('')
        self.field_name.setText('')
        self.field_category.setText('')
        self.field_unit_price.setText('')
        self.field_stock.setText('')
        self.field_extra_info.setText('')
        self.label_price_to_pay.setText('')
        self.combo_type.setEnabled(True)
        self.combo_type.setCurrentIndex(0)

    def clearForm(self):
        self.clearFields()
        self.showMessage('', False)

    # the first letter of the code tells the type of the item
    def getCodeLetter(self):
        selected_type = self.combo_type.currentText()
        if selected_type == TYPE_BOUQUET:
            return 'B'
        if selected_type == TYPE_POTTED_PLANT:
            return 'P'
        return 'O'

    # reading and validating the fields; the method returns an object of the class that
    # matches the selected type, or None after displaying the error
    def readProduct(self, product_code):
        selected_type = self.combo_type.currentText()
        new_name = self.field_name.text().strip()
        new_category = self.field_category.text().strip()
        new_extra_info = self.field_extra_info.text().strip()

        if new_name == '' or new_category == '':
            self.showMessage('The name and the category are required.', True)
            return None

        try:
            new_unit_price = float(self.field_unit_price.text())
            new_stock = int(self.field_stock.text())
        except ValueError:
            self.showMessage('The unit price must be a number, for example 45.00, and the '
                             'stock a whole number, for example 12.', True)
            return None

        if new_unit_price <= 0 or new_stock < 0:
            self.showMessage('The unit price must be above zero and the stock cannot be '
                             'negative.', True)
            return None

        if selected_type == TYPE_BOUQUET:
            try:
                new_flower_count = int(new_extra_info)
            except ValueError:
                self.showMessage('The number of flowers must be a whole number, for '
                                 'example 12.', True)
                return None
            if new_flower_count <= 0:
                self.showMessage('The number of flowers must be above zero.', True)
                return None
            return Bouquet(product_code, new_name, new_category, new_unit_price,
                           new_stock, new_flower_count)

        if selected_type == TYPE_POTTED_PLANT:
            if new_extra_info == '':
                self.showMessage('Enter the pot size, for example 15 cm.', True)
                return None
            return PottedPlant(product_code, new_name, new_category, new_unit_price,
                               new_stock, new_extra_info)

        return Product(product_code, new_name, new_category, new_unit_price, new_stock)

    def showPriceToPay(self, myProduct):
        self.label_price_to_pay.setText('Extra charge: ' + format(myProduct.getExtraCharge(), '.2f')
                                        + ' $, price to pay: '
                                        + format(myProduct.calculateDisplayPrice(), '.2f') + ' $')

    def addProduct(self):
        if self.loaded_product_code is not None:
            self.showMessage('This item is already in the catalog. Use Update to change the '
                             'record, or Clear to add a new item.', True)
            return

        # updated: the next code comes from the codes of the same letter in the product table
        new_code = database_manager.next_product_code(self.getCodeLetter())

        myProduct = self.readProduct(new_code)
        if myProduct is None:
            return

        database_manager.save_product(myProduct)
        self.loadCategorySuggestions()

        self.clearFields()
        self.showMessage('Item ' + myProduct.getProductCode() + ', '
                         + myProduct.getProductName() + ', added to the catalog at '
                         + format(myProduct.calculateDisplayPrice(), '.2f') + ' $.', False)

    def searchProduct(self):
        typed_code = self.field_code.text().strip().upper()
        if typed_code == '':
            self.showMessage('Type the item code, for example B001.', True)
            return

        myProduct = database_manager.find_product(typed_code)
        if myProduct is None:
            self.clearFields()
            self.showMessage('There is no item with the code ' + typed_code + '.', True)
            return

        self.loaded_product_code = myProduct.getProductCode()
        self.field_code.setText(myProduct.getProductCode())

        # the type of an item is part of its code, so it cannot be changed afterward
        if myProduct.getProductType() == 'Bouquet':
            self.combo_type.setCurrentText(TYPE_BOUQUET)
        elif myProduct.getProductType() == 'PottedPlant':
            self.combo_type.setCurrentText(TYPE_POTTED_PLANT)
        else:
            self.combo_type.setCurrentText(TYPE_OTHER)
        self.combo_type.setEnabled(False)

        self.field_name.setText(myProduct.getProductName())
        self.field_category.setText(myProduct.getCategory())
        self.field_unit_price.setText(format(myProduct.getUnitPrice(), '.2f'))
        self.field_stock.setText(str(myProduct.getStockQty()))
        if self.combo_type.currentText() != TYPE_OTHER:
            self.field_extra_info.setText(myProduct.getExtraInfo())

        self.showPriceToPay(myProduct)
        self.showMessage('Item ' + myProduct.getProductCode() + ' found.', False)

    # update and delete are refused when the code in the field is not the one of the
    # item displayed, so a record is never changed by mistake
    def isProductLoaded(self):
        if (self.loaded_product_code is None
                or self.field_code.text().strip().upper() != self.loaded_product_code):
            self.showMessage('Search the item by its code first.', True)
            return False
        return True

    def updateProduct(self):
        if not self.isProductLoaded():
            return

        myProduct = self.readProduct(self.loaded_product_code)
        if myProduct is None:
            return

        # updated: one UPDATE of the product row replaces the rewriting of the whole file
        database_manager.update_product(myProduct)
        self.loadCategorySuggestions()

        self.showPriceToPay(myProduct)
        self.showMessage('Item ' + myProduct.getProductCode() + ', '
                         + myProduct.getProductName() + ', updated.', False)

    # an item cannot be deleted while an order that is not completed and paid holds
    # it; finished orders keep their own copy of the name and the prices. An item that
    # was restocked cannot be deleted either, because the restock history refers to it
    def deleteProduct(self):
        if not self.isProductLoaded():
            return

        product_code = self.loaded_product_code

        for myOrder in database_manager.load_orders():
            if myOrder.isActive():
                for myItem in myOrder.getItemList():
                    if myItem.getProductCode() == product_code:
                        self.showMessage('Item ' + product_code + ' cannot be deleted: order '
                                         + str(myOrder.getOrderId())
                                         + ' holds it and is not completed and paid.', True)
                        return

        # new: the restock table refers to the product, so the row must stay
        total_restocks = database_manager.count_product_restocks(product_code)
        if total_restocks > 0:
            self.showMessage('Item ' + product_code + ' cannot be deleted: '
                             + str(total_restocks) + ' restock(s) from suppliers refer to it.', True)
            return

        answer = QMessageBox.question(self, 'Delete item',
                                      'Delete item ' + product_code + ' from the catalog?')
        if answer != QMessageBox.StandardButton.Yes:
            return

        # updated: one DELETE of the product row replaces the rewriting of the whole file
        database_manager.delete_product(product_code)

        self.clearFields()
        self.showMessage('Item ' + product_code + ' deleted from the catalog.', False)


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)

    # create the window of the catalog maintenance form
    window = ProductForm()
    window.resize(760, 360)
    window.show()

    app.exec()


# the form is started alone only when this module is the one executed
if __name__ == '__main__':
    main()
