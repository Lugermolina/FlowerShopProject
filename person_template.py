# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Sep 20, 2026
Algorithm:
Class: Python Teams online class
Inputs: person_id, last_name, first_name, address, phone, email, delivery_address, position
Processing: getter and setter methods, format_phone() applied by the constructor
and by setPhone(), getRole() overridden in the child classes
Outputs: printed person information through printPersonInfo()
"""


# Returning function: keeps one single phone format in the whole system
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


# Returning function: a phone number is valid when it holds ten digits
def is_valid_phone(phone_text):
    digits = ''
    for character in phone_text:
        if character.isdigit():
            digits = digits + character

    if len(digits) == 11 and digits[0] == '1':
        digits = digits[1:]

    return len(digits) == 10


# Returning function: a basic structural check on an email address
def is_valid_email(email_text):
    if email_text.count('@') != 1:
        return False

    local_part = email_text.split('@')[0]
    domain_part = email_text.split('@')[1]

    if len(local_part) == 0 or len(domain_part) == 0:
        return False

    return '.' in domain_part and not domain_part.endswith('.')

# Super/parent class
class Person:
    def __init__(self, person_id=None, last_name=None, first_name=None, address=None,
                 phone=None, email=None):
        self.__person_id = person_id  # private data attributes because of underscore (__)
        self.__last_name = last_name
        self.__first_name = first_name
        self.__address = address
        self.__phone = format_phone(phone)
        self.__email = email

    # accessor (getter) methods
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

    # mutator (setter) methods
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

    # concrete methods
    def getRole(self):
        return 'Person'

    def printPersonInfo(self):
        print(self.getPersonId(), '//', self.getFullName(), '//', self.getAddress(), '//',
              self.getPhone(), '//', self.getEmail())


# Sub/child class
class Customer(Person):
    def __init__(self, person_id=None, last_name=None, first_name=None, address=None,
                 phone=None, email=None, delivery_address=None):
        super().__init__(person_id, last_name, first_name, address, phone, email)
        self.__delivery_address = delivery_address

    def getDeliveryAddress(self):
        return self.__delivery_address

    def setDeliveryAddress(self, delivery_address):
        self.__delivery_address = delivery_address

    def getRole(self):
        return 'Customer'

    def printPersonInfo(self):
        print(self.getPersonId(), '//', self.getFullName(), '//', self.getAddress(), '//',
              self.getPhone(), '//', self.getEmail(), '//', self.getDeliveryAddress())


# Sub/child class
class Staff(Person):
    def __init__(self, person_id=None, last_name=None, first_name=None, address=None,
                 phone=None, email=None, position=None):
        super().__init__(person_id, last_name, first_name, address, phone, email)
        self.__position = position

    def getPosition(self):
        return self.__position

    def setPosition(self, position):
        self.__position = position

    def getRole(self):
        return 'Staff'

    def printPersonInfo(self):
        print(self.getPersonId(), '//', self.getFullName(), '//', self.getAddress(), '//',
              self.getPhone(), '//', self.getEmail(), '//', self.getPosition())

