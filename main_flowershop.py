# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Sep 20, 2026
Algorithm:
Class: Python Teams online class
Inputs: the tab selected by the user
Processing: instantiation of the two forms of iteration 1, reloading of the catalog
when its tab is opened
Outputs: the main window of the Flower Shop Management System holding both forms
"""
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget

from registration_form import RegistrationForm
from catalog_form import CatalogForm


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Flower Shop Management System, iteration 1')

        self.form_registration = RegistrationForm()
        self.form_catalog = CatalogForm()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.form_registration, 'Customer registration')
        self.tabs.addTab(self.form_catalog, 'Catalog search')

        # connect the signal (event) to the slot (action) method of this class
        self.tabs.currentChanged.connect(self.tab_changed)

        self.setCentralWidget(self.tabs)

    # the catalog file is read again every time its tab is opened
    def tab_changed(self):
        if self.tabs.currentWidget() == self.form_catalog:
            self.form_catalog.load_categories()
            self.form_catalog.show_all_items()


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)

    # create the main window of the application
    window = MainWindow()
    window.resize(1000, 620)
    window.show()

    app.exec()  # loop event


main()