# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Starting on Oct 13, 2026
Algorithm:
Class: Python Teams online class
Inputs: one customer, one walk-in order, one staff account with its password, one
delivery order with two lines, the charges of the bill
Processing: hash_password() and checkPassword(), isAdmin() and canManage() on the
three access levels, calculateLineTotal() and calculateSubtotal() of the orders,
calculateAmount() of each charge, instantiation of one BillDetail object per charge,
isActive() of the order before and after its payment and completion
Outputs: printed results only; no text file is read or written, so the data of the
application is never changed by this test
"""
from person_template import (Customer, Staff, ACCESS_ADMIN, ACCESS_MANAGER, ACCESS_CLERK,
                             CUSTOMER_INACTIVE)
from order_template import (Order, OrderItem, ORDER_PICKUP, ORDER_DELIVERY,
                            STATUS_COMPLETED, PAYMENT_PAID)
from billing_template import (Charge, BillDetail, CHARGE_PERCENT, CHARGE_FIXED,
                              CHARGE_SUBTOTAL, CHARGE_TOTAL, CHARGE_GST, CHARGE_QST,
                              CHARGE_DELIVERY)


def main():
    print('Flower Shop Project, Phase II: test of the new classes in the console')

    # the staff accounts and their passwords
    print('\nThe staff accounts: the password is stored as a SHA-256 hash')
    myStaff1 = Staff(2001, 'Administrator', 'Shop', 'Flower Shop, Montreal, QC',
                     '514-555-0100', 'admin@flowershop.com', 'Owner', 'admin', None,
                     ACCESS_ADMIN)
    myStaff1.setPassword('admin123')
    myStaff2 = Staff(2002, 'Piara', 'Lucie', '12 Rue Ontario, Montreal, QC H2L 1N8',
                     '5145550188', 'lucie.piara@flowershop.com', 'Counter clerk', 'lucie',
                     None, ACCESS_CLERK)
    myStaff2.setPassword('tulips99')
    myStaff3 = Staff(2003, 'Nasser', 'Marc', '12 Rue Ontario, Montreal, QC H2L 1N8',
                     '5145550155', 'marc.nasser@flowershop.com', 'Shop manager', 'marc',
                     None, ACCESS_MANAGER)
    myStaff3.setPassword('roses2026')

    print('Stored hash of the admin password:', myStaff1.getPasswordHash())
    print('Login of admin with admin123:', myStaff1.checkPassword('admin123'))
    print('Login of admin with admin124:', myStaff1.checkPassword('admin124'))

    print('\nThe three access levels')
    for myStaff in [myStaff1, myStaff3, myStaff2]:
        print(myStaff.getFullName(), '//', myStaff.getAccessLevel(), '// admin menus:',
              myStaff.isAdmin(), '// catalog and management reports:', myStaff.canManage())

    # a registered customer and the status of the record
    print('\nA registered customer and the status of the record')
    myCustomer1 = Customer(1001, 'Tremblay', 'Marie', '450 Rue Sherbrooke, Montreal, QC H2X 1Y4',
                           '514-555-0142', 'marie.tremblay@gmail.com',
                           '1200 Rue Saint-Denis, Montreal, QC H1M 2P8')
    print(myCustomer1.getFullName(), '// status:', myCustomer1.getStatus(),
          '// can order:', myCustomer1.isActive())
    myCustomer1.setStatus(CUSTOMER_INACTIVE)
    print(myCustomer1.getFullName(), '// status:', myCustomer1.getStatus(),
          '// can order:', myCustomer1.isActive())

    # a delivery order with two lines; the name and the prices are copied at the sale
    print('\nA delivery order with two lines')
    myOrder1 = Order(5002, 1001, 2002, '2026-10-11', '2026-10-17', ORDER_DELIVERY,
                     '1200 Rue Saint-Denis, Montreal, QC H1M 2P8')
    myOrder1.addItem(OrderItem(5002, 'O001', 'Sympathy arrangement', 1, 75.00, 0.00))
    myOrder1.addItem(OrderItem(5002, 'B002', 'Spring mixed bouquet', 2, 38.50, 5.00))
    myOrder1.printOrderInfo()
    for myItem in myOrder1.getItemList():
        myItem.printItemInfo()
    print('Subtotal of the order:', format(myOrder1.calculateSubtotal(), '.2f'), '$')

    # a walk-in order: no customer record, pickup at the counter
    print('\nA walk-in order, without a customer record')
    myOrder2 = Order(5003, None, 2002, '2026-10-11', '2026-10-17', ORDER_PICKUP)
    myOrder2.addItem(OrderItem(5003, 'B001', 'Red rose bouquet', 1, 45.00, 5.00))
    myOrder2.printOrderInfo()
    print('Delivery:', myOrder2.isDelivery(), '// subtotal:',
          format(myOrder2.calculateSubtotal(), '.2f'), '$')

    # the bill of the delivery order, calculated as the billing form does it
    print('\nThe bill of order 5002')
    mySubtotal = Charge(CHARGE_SUBTOTAL, 'Subtotal', 100.0, CHARGE_PERCENT)
    myDelivery = Charge(CHARGE_DELIVERY, 'Delivery fee', 11.00, CHARGE_FIXED)
    myGst = Charge(CHARGE_GST, 'GST', 5.0, CHARGE_PERCENT)
    myQst = Charge(CHARGE_QST, 'QST', 9.975, CHARGE_PERCENT)
    myTotal = Charge(CHARGE_TOTAL, 'Total', 100.0, CHARGE_PERCENT)
    for myCharge in [mySubtotal, myGst, myQst, myDelivery, myTotal]:
        myCharge.printChargeInfo()

    subtotal = round(myOrder1.calculateSubtotal(), 2)
    delivery_fee = myDelivery.calculateAmount(subtotal)
    taxable_base = round(subtotal + delivery_fee, 2)
    gst = myGst.calculateAmount(taxable_base)
    qst = myQst.calculateAmount(taxable_base)
    total = round(taxable_base + gst + qst, 2)

    bill_list = [BillDetail(5002, CHARGE_SUBTOTAL, subtotal, 100.0, subtotal, 10, 2026),
                 BillDetail(5002, CHARGE_DELIVERY, subtotal, 11.00, delivery_fee, 10, 2026),
                 BillDetail(5002, CHARGE_GST, taxable_base, 5.0, gst, 10, 2026),
                 BillDetail(5002, CHARGE_QST, taxable_base, 9.975, qst, 10, 2026),
                 BillDetail(5002, CHARGE_TOTAL, total, 100.0, total, 10, 2026)]
    print('\nThe lines of the bill: order // charge // base // rate // amount // month // year')
    for myBillDetail in bill_list:
        myBillDetail.printBillInfo()

    # an order stays active until it is completed and paid
    print('\nThe order is active until it is completed and paid')
    print('Before the payment:', myOrder1.getOrderStatus(), '//', myOrder1.getPaymentStatus(),
          '// active:', myOrder1.isActive())
    myOrder1.setPaymentStatus(PAYMENT_PAID)
    print('After the payment:', myOrder1.getOrderStatus(), '//', myOrder1.getPaymentStatus(),
          '// active:', myOrder1.isActive())
    myOrder1.setOrderStatus(STATUS_COMPLETED)
    print('After the completion:', myOrder1.getOrderStatus(), '//', myOrder1.getPaymentStatus(),
          '// active:', myOrder1.isActive())


main()
