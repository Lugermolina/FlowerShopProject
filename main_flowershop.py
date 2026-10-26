# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Sep 20, 2026, updating started on Oct 10, 2026 for iteration 2, and on Oct 24, 2026
for iteration 3
Algorithm:
Class: Python Teams online class
Inputs: the username and the password typed in the login form, the menu item selected
by the user
Processing: create_default_data() of the database_manager module, style sheet of the
application, building of the menus
according to the access level of the employee who logged in, instantiation of the
form that matches the selected menu item
Outputs: the main window of the Flower Shop Management System, showing the login form
first and then one form at a time
"""
import sys

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

import database_manager
from login_form import LoginForm
from registration_form import RegistrationForm
from catalog_form import CatalogForm
from product_form import ProductForm
from staff_form import StaffForm
from charge_form import ChargeForm
from order_form import OrderForm
from billing_form import BillingForm
from report_form import ReportForm
from supplier_form import SupplierForm
from restock_form import RestockForm
from order_followup_form import OrderFollowUpForm
from analytics_form import AnalyticsForm

WINDOW_TITLE = 'Flower Shop Management System'

# new: one style sheet for the whole application, in the colors of the flower shop: a muted
# rose for the main buttons, the menus and the table headers, neutral grays and white for
# the work areas, Clear with a gray outline, Delete outlined in dark red, the form titles
# in rose
ACCENT = '#A23E5C'
APP_STYLE = """
QWidget { background-color: #F7F5F6; color: #2B2B2B; font-family: "Segoe UI"; font-size: 10pt; }
QLineEdit, QTextEdit { background-color: #FFFFFF; border: 1px solid #C9C3C6;
    border-radius: 4px; padding: 4px; }
QLineEdit:focus, QTextEdit:focus { border: 1px solid ACCENT; }
QPushButton { background-color: ACCENT; color: #FFFFFF; border: none; border-radius: 4px;
    padding: 6px 14px; }
QPushButton:hover { background-color: #8E3553; }
QPushButton:pressed { background-color: #7A2D47; }
QPushButton:disabled { background-color: #D9C7CD; }
QPushButton[text="Clear"], QPushButton[text="Show all"], QPushButton[checkable="true"] {
    background-color: #FFFFFF; color: #2B2B2B; border: 1px solid #B9B2B5; }
QPushButton[text="Clear"]:hover, QPushButton[text="Show all"]:hover,
QPushButton[checkable="true"]:hover { background-color: #EFEBED; }
QPushButton[text="Delete"], QPushButton[text="Remove selected line"] {
    background-color: #FFFFFF; color: #9B1C1C; border: 1px solid #9B1C1C; }
QPushButton[text="Delete"]:hover, QPushButton[text="Remove selected line"]:hover {
    background-color: #FBEAEA; }
QMenuBar { background-color: #FFFFFF; border-bottom: 3px solid ACCENT; }
QMenuBar::item { padding: 6px 12px; background: transparent; }
QMenuBar::item:selected { background-color: #F3E6EA; color: ACCENT; }
QMenu { background-color: #FFFFFF; border: 1px solid #E2DCDF; }
QMenu::item { padding: 6px 24px; }
QMenu::item:selected { background-color: ACCENT; color: #FFFFFF; }
QLabel#title { color: ACCENT; font-size: 14pt; font-weight: bold; }
QLabel#session { background-color: ACCENT; color: #FFFFFF; font-weight: bold;
    border-radius: 10px; padding: 3px 12px; margin: 3px 8px; }
QTableWidget { background-color: #FFFFFF; alternate-background-color: #FBF3F6;
    gridline-color: #E2DCDF;
    selection-background-color: #F3E6EA; selection-color: #2B2B2B; }
QHeaderView::section { background-color: ACCENT; color: #FFFFFF; padding: 5px;
    border: none; font-weight: bold; }
""".replace('ACCENT', ACCENT)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # new data attribute: the employee who logged in, None while nobody is logged in
        self.myStaff = None
        # new: the name and the access level of the employee in session, at the right of
        # the menu bar, hidden while nobody is logged in
        self.label_session = QLabel('')
        self.label_session.setObjectName('session')
        self.menuBar().setCornerWidget(self.label_session)
        self.show_login()

    # new method: the window starts, and comes back after a log out, with the login
    # form and no menu, so nothing can be opened before logging in
    def show_login(self):
        self.myStaff = None
        self.menuBar().clear()
        self.label_session.hide()
        self.setWindowTitle(WINDOW_TITLE)
        self.setCentralWidget(LoginForm(self))

    # new method called by the login form once the username and the password are accepted
    def start_session(self, myStaff):
        self.myStaff = myStaff
        self.setWindowTitle(WINDOW_TITLE + ', ' + myStaff.getFullName() + ' ('
                            + myStaff.getAccessLevel() + ')')
        self.build_menus()
        self.label_session.setText(myStaff.getFullName() + ' (' + myStaff.getAccessLevel() + ')')
        self.label_session.show()
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
        self.add_menu_item(menu_orders, 'Order follow-up', self.open_order_followup)

        # new: the suppliers and the restocks for a manager and for an admin
        if self.myStaff.canManage():
            menu_suppliers = self.menuBar().addMenu('Suppliers')
            self.add_menu_item(menu_suppliers, 'Suppliers', self.open_suppliers)
            self.add_menu_item(menu_suppliers, 'Restock', self.open_restock)

        menu_billing = self.menuBar().addMenu('Billing')
        self.add_menu_item(menu_billing, 'Bill an order', self.open_billing)

        menu_reports = self.menuBar().addMenu('Reports')
        self.add_menu_item(menu_reports, 'Catalog search', self.open_catalog_search)
        self.add_menu_item(menu_reports, 'Clerk reports', self.open_clerk_reports)
        if self.myStaff.canManage():
            self.add_menu_item(menu_reports, 'Management reports',
                               self.open_management_reports)
            # new: the charts of the sales, the stock and the restock costs
            self.add_menu_item(menu_reports, 'Analytics', self.open_analytics)

        menu_session = self.menuBar().addMenu('Session')
        self.add_menu_item(menu_session, 'Log out', self.show_login)
        self.add_menu_item(menu_session, 'Exit', self.close)

    def show_text(self, message):
        label_text = QLabel(message)
        label_text.setStyleSheet('font-weight: bold; margin: 20px;')
        self.setCentralWidget(label_text)

    # updated: a new form object is created every time its menu item is selected, so
    # it always reads the tables again; this replaces the tabs of iteration 1
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

    def open_suppliers(self):
        self.setCentralWidget(SupplierForm())

    def open_restock(self):
        self.setCentralWidget(RestockForm())

    def open_order_followup(self):
        self.setCentralWidget(OrderFollowUpForm())

    def open_billing(self):
        self.setCentralWidget(BillingForm())

    def open_clerk_reports(self):
        self.setCentralWidget(ReportForm(self.myStaff, False))

    def open_management_reports(self):
        self.setCentralWidget(ReportForm(self.myStaff, True))

    def open_analytics(self):
        self.setCentralWidget(AnalyticsForm())


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)

    # updated: the first admin account and the charges are created when their tables are empty
    database_manager.create_default_data()

    # create the main window of the application
    window = MainWindow()
    window.resize(1000, 620)
    window.show()

    app.exec()  # loop event


main()
