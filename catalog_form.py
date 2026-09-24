# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Sep 20, 2026
Algorithm:
Class: Python Teams online class
Inputs: selected category, minimum price, maximum price, state of the
"available items only" check box
Processing: load_products() of the file_manager module, filtering of the catalog
objects on category, price range and availability, calculateDisplayPrice()
Outputs: the matching catalog items displayed in a table, the number of items found
"""
import sys

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QCheckBox, QComboBox, QGridLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QAbstractItemView)

import file_manager

ALL_CATEGORIES = 'All categories'
COLUMN_TITLES = ['Code', 'Item', 'Category', 'Unit price', 'Extra', 'Price to pay',
                 'Stock', 'Available']


class CatalogForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Flower Shop, catalog search')

        self.label_title = QLabel('Search the catalog')
        self.label_title.setStyleSheet('font-weight: bold;')
        self.label_category = QLabel('Category:')
        self.label_min_price = QLabel('Price to pay from:')
        self.label_max_price = QLabel('to:')
        self.label_message = QLabel('')

        self.combo_category = QComboBox()
        self.field_min_price = QLineEdit()
        self.field_max_price = QLineEdit()
        self.field_min_price.setPlaceholderText('20')
        self.field_max_price.setPlaceholderText('60')
        self.field_min_price.setFixedWidth(120)
        self.field_max_price.setFixedWidth(120)

        self.check_available = QCheckBox('Available items only')

        self.button_search = QPushButton('Search')
        self.button_show_all = QPushButton('Show all')

        self.table_results = QTableWidget()
        self.table_results.setColumnCount(len(COLUMN_TITLES))
        self.table_results.setHorizontalHeaderLabels(COLUMN_TITLES)
        self.table_results.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.build_layout()

        # connect the signal (event) to the slot (action) method of this class
        self.button_search.clicked.connect(self.search_catalog)
        self.button_show_all.clicked.connect(self.show_all_items)

        self.load_categories()
        self.show_all_items()

    def build_layout(self):
        grid = QGridLayout()
        grid.setColumnStretch(6, 1)

        grid.addWidget(self.label_title, 0, 0, 1, 7)
        grid.addWidget(self.label_category, 1, 0)
        grid.addWidget(self.combo_category, 1, 1)
        grid.addWidget(self.label_min_price, 1, 2)
        grid.addWidget(self.field_min_price, 1, 3)
        grid.addWidget(self.label_max_price, 1, 4)
        grid.addWidget(self.field_max_price, 1, 5)
        grid.addWidget(self.check_available, 2, 1)

        row_buttons = QHBoxLayout()
        row_buttons.addWidget(self.button_search)
        row_buttons.addWidget(self.button_show_all)
        row_buttons.addStretch()

        grid.addLayout(row_buttons, 3, 1, 1, 2)
        grid.addWidget(self.table_results, 4, 0, 1, 7)
        grid.addWidget(self.label_message, 5, 0, 1, 7)

        self.setLayout(grid)

    # the categories offered in the list come from the catalog file itself
    def load_categories(self):
        self.combo_category.clear()
        self.combo_category.addItem(ALL_CATEGORIES)
        for myProduct in file_manager.load_products():
            if self.combo_category.findText(myProduct.getCategory()) < 0:
                self.combo_category.addItem(myProduct.getCategory())

    def show_message(self, message, is_error):
        self.label_message.setText(message)
        if is_error:
            self.label_message.setStyleSheet('color: #B22222;')
        else:
            self.label_message.setStyleSheet('color: #1F7A40;')

    def fill_table(self, product_list):
        self.table_results.setRowCount(len(product_list))

        row = 0
        for myProduct in product_list:
            if myProduct.isAvailable():
                availability = 'Yes'
            else:
                availability = 'No'

            self.table_results.setItem(row, 0, QTableWidgetItem(myProduct.getProductCode()))
            self.table_results.setItem(row, 1, QTableWidgetItem(myProduct.getProductName()))
            self.table_results.setItem(row, 2, QTableWidgetItem(myProduct.getCategory()))
            self.table_results.setItem(row, 3, QTableWidgetItem(f'{myProduct.getUnitPrice():.2f} $'))
            self.table_results.setItem(row, 4, QTableWidgetItem(f'{myProduct.getExtraCharge():.2f} $'))
            self.table_results.setItem(row, 5, QTableWidgetItem(f'{myProduct.calculateDisplayPrice():.2f} $'))
            self.table_results.setItem(row, 6, QTableWidgetItem(str(myProduct.getStockQty())))
            self.table_results.setItem(row, 7, QTableWidgetItem(availability))
            row = row + 1

        self.table_results.resizeColumnsToContents()

    def show_all_items(self):
        self.combo_category.setCurrentIndex(0)
        self.field_min_price.setText('')
        self.field_max_price.setText('')
        self.check_available.setChecked(False)

        product_list = file_manager.load_products()
        self.fill_table(product_list)
        self.show_message('The catalog holds ' + str(len(product_list)) + ' items.', False)

    def search_catalog(self):
        selected_category = self.combo_category.currentText()
        min_price_text = self.field_min_price.text().strip()
        max_price_text = self.field_max_price.text().strip()

        min_price = 0.0
        max_price = 0.0  # a maximum of zero means that no upper limit was entered

        try:
            if min_price_text != '':
                min_price = float(min_price_text)
            if max_price_text != '':
                max_price = float(max_price_text)
        except ValueError:
            self.table_results.setRowCount(0)
            self.show_message('The price range accepts numbers only, for example 20 and 60.', True)
            return

        if max_price > 0 and max_price < min_price:
            self.table_results.setRowCount(0)
            self.show_message('The maximum price is lower than the minimum price.', True)
            return

        found_list = []
        for myProduct in file_manager.load_products():
            price_to_pay = myProduct.calculateDisplayPrice()
            keep_item = True

            if selected_category != ALL_CATEGORIES and myProduct.getCategory() != selected_category:
                keep_item = False
            if price_to_pay < min_price:
                keep_item = False
            if max_price > 0 and price_to_pay > max_price:
                keep_item = False
            if self.check_available.isChecked() and not myProduct.isAvailable():
                keep_item = False

            if keep_item:
                found_list.append(myProduct)

        self.fill_table(found_list)

        if len(found_list) == 0:
            self.show_message('No item matches the search.', True)
        elif len(found_list) == 1:
            self.show_message('1 item found.', False)
        else:
            self.show_message(str(len(found_list)) + ' items found.', False)


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)

    # create the window of the catalog search form
    window = CatalogForm()
    window.resize(820, 420)
    window.show()

    app.exec()  # loop event


# the form is started alone only when this module is the one executed
if __name__ == '__main__':
    main()