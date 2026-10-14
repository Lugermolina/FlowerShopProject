# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Sep 20, 2026, updated Oct 10, 2026 for iteration 2
Algorithm:
Class: Python Teams online class
Inputs: person_id, last_name, first_name, address, phone, email, delivery_address, status,
position, username, password, access_level
Processing: getter and setter methods, format_phone() applied by the constructor
and by setPhone(), getRole() overridden in the child classes, hash_password() applied
by setPassword() and checkPassword()
Outputs: printed person information through printPersonInfo()
"""
import hashlib

# updated: three access levels of the staff accounts, the manager is new
ACCESS_ADMIN = 'Admin'
ACCESS_MANAGER = 'Manager'
ACCESS_CLERK = 'Clerk'

# two customers' possible states
CUSTOMER_ACTIVE = 'Active'
CUSTOMER_INACTIVE = 'Inactive'


# one single phone format in the whole system
def format_phone(phone_text):
    if phone_text is None:
        return None

    digits = ''
    for character in phone_text:
        if character.isdigit():
            digits = digits + character

    if len(digits) == 11 and digits[0] == '1':
        digits = digits[1:]

    if len(digits) == 10:
        return digits[0:3] + '-' + digits[3:6] + '-' + digits[6:10]

    return phone_text


# a phone number is valid when it holds ten digits
def is_valid_phone(phone_text):
    digits = ''
    for character in phone_text:
        if character.isdigit():
            digits = digits + character

    if len(digits) == 11 and digits[0] == '1':
        digits = digits[1:]

    return len(digits) == 10


# a basic structural check on an email address
def is_valid_email(email_text):
    if email_text.count('@') != 1:
        return False

    local_part = email_text.split('@')[0]
    domain_part = email_text.split('@')[1]

    if len(local_part) == 0 or len(domain_part) == 0:
        return False

    return '.' in domain_part and not domain_part.endswith('.')


# new function to hash a password with SHA-256, so staff.txt never holds the real password
def hash_password(password_text):
    return hashlib.sha256(password_text.encode('utf-8')).hexdigest()


# Super/parent class
class Person:
    def __init__(self, person_id=None, last_name=None, first_name=None, address=None,
                 phone=None, email=None):
        self.__person_id = person_id
        self.__last_name = last_name
        self.__first_name = first_name
        self.__address = address
        self.__phone = format_phone(phone)
        self.__email = email

    def getPersonId(self):
        return self.__person_id

    def getLastName(self):
        return self.__last_name

    def getFirstName(self):
        return self.__first_name

    def getFullName(self):
        return self.getLastName() + ' ' + self.getFirstName()

    def getAddress(self):
        return self.__address

    def getPhone(self):
        return self.__phone

    def getEmail(self):
        return self.__email

    def setPersonId(self, person_id):
        self.__person_id = person_id

    def setLastName(self, last_name):
        self.__last_name = last_name

    def setFirstName(self, first_name):
        self.__first_name = first_name

    def setAddress(self, address):
        self.__address = address

    # the phone is reformatted so that every record holds the same format
    def setPhone(self, phone):
        self.__phone = format_phone(phone)

    def setEmail(self, email):
        self.__email = email

    def getRole(self):
        return 'Person'

    def printPersonInfo(self):
        print(self.getPersonId(), '//', self.getFullName(), '//', self.getAddress(), '//',
              self.getPhone(), '//', self.getEmail())


# Sub/child class
class Customer(Person):
    def __init__(self, person_id=None, last_name=None, first_name=None, address=None,
                 phone=None, email=None, delivery_address=None, status=CUSTOMER_ACTIVE):
        super().__init__(person_id, last_name, first_name, address, phone, email)
        self.__delivery_address = delivery_address
        # new data attribute to deactivate a customer without erasing their order history
        self.__status = status

    def getDeliveryAddress(self):
        return self.__delivery_address

    def setDeliveryAddress(self, delivery_address):
        self.__delivery_address = delivery_address

    def getStatus(self):
        return self.__status

    def setStatus(self, status):
        self.__status = status

    # new method to tell whether the customer can still place an order
    def isActive(self):
        return self.getStatus() == CUSTOMER_ACTIVE

    def getRole(self):
        return 'Customer'

    def printPersonInfo(self):
        print(self.getPersonId(), '//', self.getFullName(), '//', self.getAddress(), '//',
              self.getPhone(), '//', self.getEmail(), '//', self.getDeliveryAddress())


# Sub/child class
class Staff(Person):
    def __init__(self, person_id=None, last_name=None, first_name=None, address=None,
                 phone=None, email=None, position=None, username=None, password_hash=None,
                 access_level=ACCESS_CLERK):
        super().__init__(person_id, last_name, first_name, address, phone, email)
        self.__position = position
        # the employee log in
        self.__username = username
        self.__password_hash = password_hash
        self.__access_level = access_level

    def getPosition(self):
        return self.__position

    def setPosition(self, position):
        self.__position = position

    def getUsername(self):
        return self.__username

    def getPasswordHash(self):
        return self.__password_hash

    def getAccessLevel(self):
        return self.__access_level

    def setUsername(self, username):
        self.__username = username

    def setAccessLevel(self, access_level):
        self.__access_level = access_level

    # new method to store a password: only its hash is kept, never the typed text
    def setPassword(self, password_text):
        self.__password_hash = hash_password(password_text)

    # new method to check the password typed in the login form against the stored hash
    def checkPassword(self, password_text):
        return hash_password(password_text) == self.getPasswordHash()

    # new method to open the admin menus only to an admin account
    def isAdmin(self):
        return self.getAccessLevel() == ACCESS_ADMIN

    # new method to open the catalog maintenance and the management reports to a
    # manager and to an admin
    def canManage(self):
        return self.getAccessLevel() == ACCESS_MANAGER or self.isAdmin()

    def getRole(self):
        return 'Staff'

    def printPersonInfo(self):
        print(self.getPersonId(), '//', self.getFullName(), '//', self.getAddress(), '//',
              self.getPhone(), '//', self.getEmail(), '//', self.getPosition())

