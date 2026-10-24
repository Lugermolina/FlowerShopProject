# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Starting on Oct 10, 2026, updating started on Oct 24, 2026 for iteration 3
Algorithm:
Class: Python Teams online class
Inputs: staff number, last name, first name, address, phone, email, position, username,
password, access level, the button pressed
Processing: validation of the entered values, duplicate username check, hashing of the
password by the Staff class, add, search, update and delete of a record through the
database_manager module, rules that protect the account in use and the last admin account
Outputs: the staff record added to, changed in or removed from the staff table, the record
found displayed in the fields, a confirmation or an error message displayed on the form
"""
import sys

from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QComboBox, QGridLayout, QHBoxLayout, QMessageBox)

import database_manager
from eye_icon import make_eye_icon
from person_template import (Staff, is_valid_phone, is_valid_email, ACCESS_ADMIN,
                             ACCESS_MANAGER, ACCESS_CLERK, ACCESS_INACTIVE)

PASSWORD_MIN_LENGTH = 6


class StaffForm(QWidget):
    # the employee who logged in is received as a parameter, because an account
    # cannot delete itself or change its own access level
    def __init__(self, current_staff=None):
        super().__init__()
        self.setWindowTitle('Flower Shop, staff')
        self.current_staff = current_staff

        # the number of the employee displayed after a search, None while the form
        # is empty; update and delete only act on this employee
        self.loaded_staff_id = None

        self.label_title = QLabel('Staff')
        self.label_title.setObjectName('title')
        self.label_staff_id = QLabel('Staff number:')
        self.label_last_name = QLabel('Last name:')
        self.label_first_name = QLabel('First name:')
        self.label_address = QLabel('Address:')
        self.label_phone = QLabel('Phone:')
        self.label_email = QLabel('Email:')
        self.label_position = QLabel('Position:')
        self.label_username = QLabel('Username:')
        self.label_password = QLabel('Password:')
        self.label_access_level = QLabel('Access level:')
        self.label_message = QLabel('')

        self.field_staff_id = QLineEdit()
        self.field_last_name = QLineEdit()
        self.field_first_name = QLineEdit()
        self.field_address = QLineEdit()
        self.field_phone = QLineEdit()
        self.field_email = QLineEdit()
        self.field_position = QLineEdit()
        self.field_username = QLineEdit()
        self.field_password = QLineEdit()
        self.field_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.field_staff_id.setPlaceholderText('type a number to search; a new employee '
                                               'gets a number automatically')
        self.field_phone.setPlaceholderText('514-555-0142')
        self.field_email.setPlaceholderText('name@flowershop.com')
        self.field_position.setPlaceholderText('Florist')
        self.field_password.setPlaceholderText('at least ' + str(PASSWORD_MIN_LENGTH)
                                               + ' characters')

        # the eye is crossed by a line while the password is hidden
        self.button_show_password = QPushButton()
        self.button_show_password.setIcon(make_eye_icon(False))
        self.button_show_password.setCheckable(True)
        self.button_show_password.setFixedWidth(40)
        self.button_show_password.setToolTip('Show the password')

        self.combo_access_level = QComboBox()
        self.combo_access_level.addItem(ACCESS_CLERK)
        self.combo_access_level.addItem(ACCESS_MANAGER)
        self.combo_access_level.addItem(ACCESS_ADMIN)
        self.combo_access_level.addItem(ACCESS_INACTIVE)

        self.button_add = QPushButton('Add')
        self.button_search = QPushButton('Search')
        self.button_update = QPushButton('Update')
        self.button_delete = QPushButton('Delete')
        self.button_clear = QPushButton('Clear')

        self.buildLayout()

        # connect the signal (event) to the slot (action) method of this class
        self.button_show_password.clicked.connect(self.showPasswordChanged)
        self.button_add.clicked.connect(self.addStaff)
        self.button_search.clicked.connect(self.searchStaff)
        self.button_update.clicked.connect(self.updateStaff)
        self.button_delete.clicked.connect(self.deleteStaff)
        self.button_clear.clicked.connect(self.clearForm)

    def buildLayout(self):
        grid = QGridLayout()
        grid.setColumnStretch(1, 1)

        grid.addWidget(self.label_title, 0, 0, 1, 2)
        grid.addWidget(self.label_staff_id, 1, 0)
        grid.addWidget(self.field_staff_id, 1, 1)
        grid.addWidget(self.label_last_name, 2, 0)
        grid.addWidget(self.field_last_name, 2, 1)
        grid.addWidget(self.label_first_name, 3, 0)
        grid.addWidget(self.field_first_name, 3, 1)
        grid.addWidget(self.label_address, 4, 0)
        grid.addWidget(self.field_address, 4, 1)
        grid.addWidget(self.label_phone, 5, 0)
        grid.addWidget(self.field_phone, 5, 1)
        grid.addWidget(self.label_email, 6, 0)
        grid.addWidget(self.field_email, 6, 1)
        grid.addWidget(self.label_position, 7, 0)
        grid.addWidget(self.field_position, 7, 1)
        grid.addWidget(self.label_username, 8, 0)
        grid.addWidget(self.field_username, 8, 1)
        grid.addWidget(self.label_password, 9, 0)
        grid.addWidget(self.field_password, 9, 1)
        grid.addWidget(self.button_show_password, 9, 2)
        grid.addWidget(self.label_access_level, 10, 0)
        grid.addWidget(self.combo_access_level, 10, 1)

        row_buttons = QHBoxLayout()
        row_buttons.addWidget(self.button_add)
        row_buttons.addWidget(self.button_search)
        row_buttons.addWidget(self.button_update)
        row_buttons.addWidget(self.button_delete)
        row_buttons.addWidget(self.button_clear)
        row_buttons.addStretch()

        grid.addLayout(row_buttons, 11, 1)
        grid.addWidget(self.label_message, 12, 0, 1, 3)
        grid.setRowStretch(13, 1)

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

    def clearFields(self):
        self.loaded_staff_id = None
        self.field_staff_id.setText('')
        self.field_last_name.setText('')
        self.field_first_name.setText('')
        self.field_address.setText('')
        self.field_phone.setText('')
        self.field_email.setText('')
        self.field_position.setText('')
        self.field_username.setText('')
        self.field_password.setText('')
        self.field_password.setPlaceholderText('at least ' + str(PASSWORD_MIN_LENGTH)
                                               + ' characters')
        self.button_show_password.setChecked(False)
        self.showPasswordChanged()
        self.combo_access_level.setCurrentIndex(0)

    def clearForm(self):
        self.clearFields()
        self.showMessage('', False)

    # counting the admin accounts, because the last one cannot be deleted or lowered
    def countAdmins(self):
        total_admins = 0
        for myStaff in database_manager.load_staff():
            if myStaff.isAdmin():
                total_admins = total_admins + 1
        return total_admins

    # reading and validating the fields; the method returns a Staff object, or None
    # after displaying the error. An empty password is accepted only on an update,
    # where it means that the current password is kept
    def readStaff(self, person_id, current_password_hash):
        new_last_name = self.field_last_name.text().strip()
        new_first_name = self.field_first_name.text().strip()
        new_address = self.field_address.text().strip()
        new_phone = self.field_phone.text().strip()
        new_email = self.field_email.text().strip()
        new_position = self.field_position.text().strip()
        new_username = self.field_username.text().strip()
        new_password = self.field_password.text()
        new_access_level = self.combo_access_level.currentText()

        if (new_last_name == '' or new_first_name == '' or new_address == ''
                or new_phone == '' or new_email == '' or new_position == ''
                or new_username == ''):
            self.showMessage('All the fields are required.', True)
            return None

        if not is_valid_phone(new_phone):
            self.showMessage('The phone number must hold ten digits, for example 514-555-0142.', True)
            return None

        if not is_valid_email(new_email):
            self.showMessage('The email address is not valid, for example name@flowershop.com.', True)
            return None

        sameUsernameStaff = database_manager.find_staff_by_username(new_username)
        if sameUsernameStaff is not None and sameUsernameStaff.getPersonId() != person_id:
            self.showMessage('The username ' + new_username + ' already belongs to employee '
                             + str(sameUsernameStaff.getPersonId()) + ', '
                             + sameUsernameStaff.getFullName() + '.', True)
            return None

        if new_password == '' and current_password_hash is None:
            self.showMessage('Enter a password for the new account.', True)
            return None

        if new_password != '' and len(new_password) < PASSWORD_MIN_LENGTH:
            self.showMessage('The password must hold at least ' + str(PASSWORD_MIN_LENGTH)
                             + ' characters.', True)
            return None

        myStaff = Staff(person_id, new_last_name, new_first_name, new_address, new_phone,
                        new_email, new_position, new_username, current_password_hash,
                        new_access_level)
        if new_password != '':
            myStaff.setPassword(new_password)
        return myStaff

    def addStaff(self):
        if self.loaded_staff_id is not None:
            self.showMessage('This employee is already registered. Use Update to change the '
                             'record, or Clear to add a new employee.', True)
            return

        # updated: the next number comes from the highest one in the staff table
        new_person_id = database_manager.next_staff_id()

        myStaff = self.readStaff(new_person_id, None)
        if myStaff is None:
            return

        database_manager.save_staff(myStaff)

        self.clearFields()
        self.showMessage('Employee ' + str(myStaff.getPersonId()) + ', '
                         + myStaff.getFullName() + ', added with the username '
                         + myStaff.getUsername() + ' (' + myStaff.getAccessLevel() + ').', False)

    def searchStaff(self):
        try:
            typed_id = int(self.field_staff_id.text())
        except ValueError:
            self.showMessage('Type the staff number, for example 2001.', True)
            return

        myStaff = database_manager.find_staff(typed_id)
        if myStaff is None:
            self.clearFields()
            self.showMessage('There is no employee with the number ' + str(typed_id) + '.', True)
            return

        self.loaded_staff_id = myStaff.getPersonId()
        self.field_staff_id.setText(str(myStaff.getPersonId()))
        self.field_last_name.setText(myStaff.getLastName())
        self.field_first_name.setText(myStaff.getFirstName())
        self.field_address.setText(myStaff.getAddress())
        self.field_phone.setText(myStaff.getPhone())
        self.field_email.setText(myStaff.getEmail())
        self.field_position.setText(myStaff.getPosition())
        self.field_username.setText(myStaff.getUsername())
        self.combo_access_level.setCurrentText(myStaff.getAccessLevel())

        # the stored hash cannot be turned back into the password, so the field
        # stays empty
        self.field_password.setText('')
        self.field_password.setPlaceholderText('leave empty to keep the current password')

        self.showMessage('Employee ' + str(myStaff.getPersonId()) + ' found.', False)

    # update and delete are refused when the number in the field is not the one of
    # the employee displayed, so a record is never changed by mistake
    def isStaffLoaded(self):
        if (self.loaded_staff_id is None
                or self.field_staff_id.text().strip() != str(self.loaded_staff_id)):
            self.showMessage('Search the employee by number first.', True)
            return False
        return True

    def isCurrentStaff(self):
        return (self.current_staff is not None
                and self.current_staff.getPersonId() == self.loaded_staff_id)

    def updateStaff(self):
        if not self.isStaffLoaded():
            return

        oldStaff = database_manager.find_staff(self.loaded_staff_id)
        myStaff = self.readStaff(self.loaded_staff_id, oldStaff.getPasswordHash())
        if myStaff is None:
            return

        if myStaff.getAccessLevel() != oldStaff.getAccessLevel():
            if self.isCurrentStaff():
                self.showMessage('The access level of the account in use cannot be changed.', True)
                return
            if oldStaff.isAdmin() and self.countAdmins() == 1:
                self.showMessage('The last admin account must keep the Admin access level.', True)
                return

        # updated: one UPDATE of the staff row replaces the rewriting of the whole file
        database_manager.update_staff(myStaff)

        password_changed = self.field_password.text() != ''
        self.field_password.setText('')
        if password_changed:
            self.showMessage('Employee ' + str(myStaff.getPersonId()) + ', '
                             + myStaff.getFullName() + ', updated with a new password.', False)
        else:
            self.showMessage('Employee ' + str(myStaff.getPersonId()) + ', '
                             + myStaff.getFullName() + ', updated.', False)

    # an employee cannot be deleted when it is the account in use or the last admin
    # account; an employee recorded on an order is kept and becomes inactive
    def deleteStaff(self):
        if not self.isStaffLoaded():
            return

        staff_id = self.loaded_staff_id

        if self.isCurrentStaff():
            self.showMessage('The account in use cannot be deleted.', True)
            return

        oldStaff = database_manager.find_staff(staff_id)
        if oldStaff.isAdmin() and self.countAdmins() == 1:
            self.showMessage('The last admin account cannot be deleted.', True)
            return

        total_orders = 0
        for myOrder in database_manager.load_orders():
            if myOrder.getStaffId() == staff_id:
                total_orders = total_orders + 1
        if total_orders > 0 and not oldStaff.isActive():
            self.showMessage('Employee ' + str(staff_id) + ' is already inactive.', True)
            return

        answer = QMessageBox.question(self, 'Delete employee',
                                      'Delete employee ' + str(staff_id) + '?')
        if answer != QMessageBox.StandardButton.Yes:
            return

        # updated: an employee who left keeps the row, because the orders refer to it,
        # with the Inactive access level; without orders the row is deleted
        if total_orders > 0:
            oldStaff.setAccessLevel(ACCESS_INACTIVE)
            database_manager.update_staff(oldStaff)
        else:
            database_manager.delete_staff(staff_id)

        self.clearFields()
        if total_orders > 0:
            self.showMessage('Employee ' + str(staff_id) + ' took ' + str(total_orders)
                             + ' order(s): the record is kept and the account is now inactive.',
                             False)
        else:
            self.showMessage('Employee ' + str(staff_id) + ' deleted.', False)


def main():
    # instantiate an object app from QApplication
    app = QApplication(sys.argv)

    # create the window of the staff form
    window = StaffForm()
    window.resize(760, 440)
    window.show()

    app.exec()


# the form is started alone only when this module is the one executed
if __name__ == '__main__':
    main()
