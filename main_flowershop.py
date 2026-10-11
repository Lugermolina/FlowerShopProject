# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Sep 20, 2026, updating started on Oct 10, 2026 for iteration 2
Algorithm:
Class: Python Teams online class
Inputs: the username and the password typed in the login form, the menu item selected
by the user
Processing: create_default_data() of the file_manager module, building of the menus
according to the access level of the employee who logged in, instantiation of the
form that matches the selected menu item
Outputs: the main window of the Flower Shop Management System, showing the login form
first and then one form at a time
"""
import sys

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

import file_manager
from login_form import LoginForm
from registration_form import RegistrationForm
from catalog_form import CatalogForm
from product_form import ProductForm
from staff_form import StaffForm
from charge_form import ChargeForm
from order_form import OrderForm

WINDOW_TITLE = 'Flower Shop Management System'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # new data attribute: the employee who logged in, None while nobody is logged in
        self.myStaff = None
        self.show_login()

    # new method: the window starts, and comes back after a log out, with the login
    # form and no menu, so nothing can be opened before logging in
    def show_login(self):
        self.myStaff = None
        self.menuBar().clear()
        self.setWindowTitle(WINDOW_TITLE)
        self.setCentralWidget(LoginForm(self))

    # new method called by the login form once the username and the password are accepted
    def start_session(self, myStaff):
        self.myStaff = myStaff
        self.setWindowTitle(WINDOW_TITLE + ', ' + myStaff.getFullName() + ' ('
                            + myStaff.getAccessLevel() + ')')
        self.build_menus()
        self.show_text('Welcome, ' + myStaff.getFullName()
                       + '. Choose an option in the menu.')

    # new method to add one item to a menu and connect it to its slot method
    def add_menu_item(self, menu, title, slot_method):
        action = QAction(title, self)
        action.triggered.connect(slot_method)
        menu.addAction(action)

    # new method: the catalog maintenance and the management reports are added for a
    # manager and for an admin, the staff and the charges only for an admin
    def build_menus(self):
        menu_input = self.menuBar().addMenu('Input Data')
        self.add_menu_item(menu_input, 'Customers', self.open_customers)
        if self.myStaff.canManage():
            self.add_menu_item(menu_input, 'Catalog', self.open_products)
        if self.myStaff.isAdmin():
            self.add_menu_item(menu_input, 'Staff', self.open_staff)
            self.add_menu_item(menu_input, 'Charges', self.open_charges)

        menu_orders = self.menuBar().addMenu('Orders')
        self.add_menu_item(menu_orders, 'Orders', self.open_orders)

        menu_billing = self.menuBar().addMenu('Billing')
        self.add_menu_item(menu_billing, 'Bill an order', self.open_billing)

        menu_reports = self.menuBar().addMenu('Reports')
        self.add_menu_item(menu_reports, 'Catalog search', self.open_catalog_search)
        self.add_menu_item(menu_reports, 'Clerk reports', self.open_clerk_reports)
        if self.myStaff.canManage():
            self.add_menu_item(menu_reports, 'Management reports',
                               self.open_management_reports)

        menu_session = self.menuBar().addMenu('Session')
        self.add_menu_item(menu_session, 'Log out', self.show_login)
        self.add_menu_item(menu_session, 'Exit', self.close)

    def show_text(self, message):
        label_text = QLabel(message)
        label_text.setStyleSheet('font-weight: bold; margin: 20px;')
        self.setCentralWidget(label_text)

    # updated: a new form object is created every time its menu item is selected, so
    # it always reads the files again; this replaces the tabs of iteration 1
    def open_customers(self):
        self.setCentralWidget(RegistrationForm())

    def open_catalog_search(self):
        self.setCentralWidget(CatalogForm())

    def open_products(self):
        self.setCentralWidget(ProductForm())

    def open_staff(self):
        self.setCentralWidget(StaffForm(self.myStaff))

    def open_charges(self):
        self.setCentralWidget(ChargeForm())

    def open_orders(self):
        self.setCentralWidget(OrderForm(self.myStaff))

    def open_billing(self):
        self.show_text('Billing: this form is not built yet.')

    def open_clerk_reports(self):
        self.show_text('Clerk reports: this form is not built yet.')

    def open_management_reports(self):
        self.show_text('Management reports: this form is not built yet.')


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)

    # new: the first admin account and the charges are created when their files are empty
    file_manager.create_default_data()

    # create the main window of the application
    window = MainWindow()
    window.resize(1000, 620)
    window.show()

    app.exec()  # loop event


main()
