# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Starting on Oct 10, 2026, updating started on Oct 24, 2026 for iteration 3
Algorithm:
Class: Python Teams online class
Inputs: username, password
Processing: find_staff_by_username() of the database_manager module, checkPassword() of the
Staff class, which compares the hash of the typed password with the stored hash
Outputs: the Staff object of the employee who logged in, handed to the main window,
or an error message displayed on the form
"""
import sys

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QGridLayout, QHBoxLayout)

import database_manager
from eye_icon import make_eye_icon


class LoginForm(QWidget):
    # the main window is received as a parameter, so the form can hand it the employee
    # who logged in; without a main window the form only shows the result
    def __init__(self, main_window=None):
        super().__init__()
        self.setWindowTitle('Flower Shop, log in')
        self.main_window = main_window

        self.label_title = QLabel('Flower Shop Management System')
        self.label_title.setStyleSheet('font-weight: bold;')
        self.label_username = QLabel('Username:')
        self.label_password = QLabel('Password:')
        self.label_message = QLabel('')

        self.field_username = QLineEdit()
        self.field_password = QLineEdit()
        # the typed password is displayed as dots
        self.field_password.setEchoMode(QLineEdit.EchoMode.Password)

        # the eye button shows the typed password while it stays pressed down; the
        # eye is crossed by a line while the password is hidden
        self.button_show_password = QPushButton()
        self.button_show_password.setIcon(make_eye_icon(False))
        self.button_show_password.setCheckable(True)
        self.button_show_password.setFixedWidth(40)
        self.button_show_password.setToolTip('Show the password')

        self.button_login = QPushButton('Log in')
        self.button_clear = QPushButton('Clear')

        self.buildLayout()

        # connect the signal (event) to the slot (action) method of this class
        self.button_login.clicked.connect(self.logIn)
        self.button_clear.clicked.connect(self.clearForm)
        self.button_show_password.clicked.connect(self.showPasswordChanged)
        # the Enter key in the password field does the same as the Log in button
        self.field_password.returnPressed.connect(self.logIn)

    def buildLayout(self):
        grid = QGridLayout()
        grid.setColumnStretch(1, 1)

        grid.addWidget(self.label_title, 0, 0, 1, 2)
        grid.addWidget(self.label_username, 1, 0)
        grid.addWidget(self.field_username, 1, 1)
        grid.addWidget(self.label_password, 2, 0)
        grid.addWidget(self.field_password, 2, 1)
        grid.addWidget(self.button_show_password, 2, 2)

        row_buttons = QHBoxLayout()
        row_buttons.addWidget(self.button_login)
        row_buttons.addWidget(self.button_clear)
        row_buttons.addStretch()

        grid.addLayout(row_buttons, 3, 1)
        grid.addWidget(self.label_message, 4, 0, 1, 2)
        grid.setRowStretch(5, 1)

        self.setLayout(grid)

    def showPasswordChanged(self):
        if self.button_show_password.isChecked():
            self.field_password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.button_show_password.setIcon(make_eye_icon(True))
            self.button_show_password.setToolTip('Hide the password')
        else:
            self.field_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.button_show_password.setIcon(make_eye_icon(False))
            self.button_show_password.setToolTip('Show the password')

    def showMessage(self, message, is_error):
        self.label_message.setText(message)
        if is_error:
            self.label_message.setStyleSheet('color: #B22222;')
        else:
            self.label_message.setStyleSheet('color: #1F7A40;')

    def clearForm(self):
        self.field_username.setText('')
        self.field_password.setText('')
        self.button_show_password.setChecked(False)
        self.showPasswordChanged()
        self.showMessage('', False)

    def logIn(self):
        typed_username = self.field_username.text().strip()
        typed_password = self.field_password.text()

        if typed_username == '' or typed_password == '':
            self.showMessage('Enter the username and the password.', True)
            return

        myStaff = database_manager.find_staff_by_username(typed_username)

        # one single message for both cases, so the form does not reveal which
        # usernames exist
        if myStaff is None or not myStaff.checkPassword(typed_password):
            self.field_password.setText('')
            self.showMessage('The username or the password is not correct.', True)
            return

        self.field_password.setText('')
        self.showMessage('Welcome, ' + myStaff.getFullName() + ' ('
                         + myStaff.getAccessLevel() + ').', False)

        if self.main_window is not None:
            self.main_window.start_session(myStaff)


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)

    # the first admin account is created when the staff table holds no record
    database_manager.create_default_data()

    # create the window of the login form
    window = LoginForm()
    window.resize(420, 180)
    window.show()

    app.exec()


# the form is started alone only when this module is the one executed
if __name__ == '__main__':
    main()
