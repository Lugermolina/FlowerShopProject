# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Oct 25, 2026 for iteration 3
Algorithm:
Class: Python Teams online class
Inputs: one supplier, two restocks, one staff account made inactive, the demo data of
the MySQL database flowershopdb just after flowershopdb.sql is run
Processing: unit tests of the new classes (calculateCost(), isActive() of a staff
account), integration tests of the database_manager module: the records read back as
objects, the rules that block a delete, the open orders, the bill of an order, the
totals calculated by MySQL with GROUP BY compared with the same totals calculated in
Python from the objects
Outputs: printed results, each test with the value obtained, the value expected and OK
or NOT OK; nothing is written to the database, so the demo data is never changed
"""
from person_template import Staff, ACCESS_CLERK, ACCESS_INACTIVE
from supplier_template import Supplier, Restock
from billing_template import CHARGE_SUBTOTAL
import database_manager

# the number of tests that failed, shown at the end
failed_tests = []


def check(description, obtained, expected):
    if obtained == expected:
        result = 'OK'
    else:
        result = 'NOT OK'
        failed_tests.append(description)
    print(result, '//', description, '// obtained:', obtained, '// expected:', expected)


def main():
    print('Flower Shop Project, Phase III: unit and integration tests in the console')

    # ---------- unit tests: the classes alone, without the database ----------
    print('\nUnit tests of the new classes')
    mySupplier = Supplier(3001, 'Laurentian Greenhouses', 'Sophie Lavoie', '450-555-0131',
                          'orders@laurentiangreenhouses.ca',
                          '1400 Chemin du Lac, Saint-Sauveur, QC J0R 1R0')
    mySupplier.printSupplierInfo()

    myRestock1 = Restock(7001, 'B001', 3001, '2026-10-05', 10, 22.50)
    myRestock2 = Restock(7004, 'B003', 3001, '2026-10-13', 20, 15.50)
    myRestock1.printRestockInfo()
    myRestock2.printRestockInfo()
    check('cost of restock 7001, 10 x 22.50', format(myRestock1.calculateCost(), '.2f'), '225.00')
    check('cost of restock 7004, 20 x 15.50', format(myRestock2.calculateCost(), '.2f'), '310.00')

    myStaff = Staff(2002, 'Piara', 'Lucie', '12 Rue Ontario, Montreal, QC H2L 1N8',
                    '5145550188', 'lucie.piara@flowershop.com', 'Counter clerk', 'lucie',
                    None, ACCESS_CLERK)
    myStaff.setPassword('tulips99')
    check('clerk account active', myStaff.isActive(), True)
    myStaff.setAccessLevel(ACCESS_INACTIVE)
    check('account after the level Inactive', myStaff.isActive(), False)
    check('inactive account keeps its password', myStaff.checkPassword('tulips99'), True)
    check('inactive account opens management menus', myStaff.canManage(), False)

    # ---------- integration tests: the classes with the database_manager module ----------
    print('\nIntegration tests with the database flowershopdb (demo data)')
    check('number of customers', len(database_manager.load_customers()), 5)
    check('number of orders', len(database_manager.load_orders()), 16)
    check('number of suppliers', len(database_manager.load_suppliers()), 3)

    myStaffRead = database_manager.find_staff_by_username('lucie')
    check('login of lucie with tulips99', myStaffRead.checkPassword('tulips99'), True)
    check('login of lucie with tulips98', myStaffRead.checkPassword('tulips98'), False)

    # the rules that refuse a delete
    check('restocks of item B001 (delete refused)', database_manager.count_product_restocks('B001'), 1)
    check('restocks of item B002 (delete allowed)', database_manager.count_product_restocks('B002'), 0)
    check('restocks of supplier 3001 (delete refused)',
          database_manager.count_supplier_restocks(3001), 2)

    # the order follow-up only reads the orders that are not completed
    open_list = []
    for myOrder in database_manager.load_open_orders():
        open_list.append(myOrder.getOrderId())
    check('open orders', open_list, [5003])

    # the total of the bill is the last line, even though its number 101 is lower
    bill_list = database_manager.load_order_bill(5002)
    check('lines of the bill of order 5002', len(bill_list), 5)
    check('last line of the bill of order 5002', format(bill_list[-1].getAmount(), '.2f'), '198.91')

    # the totals of MySQL (GROUP BY) against the same totals calculated in Python
    print('\nThe totals of the analytics: MySQL GROUP BY against a loop in Python')
    total_python = 0.0
    for myBillDetail in database_manager.load_bill_details():
        if myBillDetail.getChargeNo() == CHARGE_SUBTOTAL:
            total_python = total_python + myBillDetail.getAmount()
    total_month = 0.0
    for row in database_manager.load_sales_by_month():
        total_month = total_month + float(row[3])
    total_category = 0.0
    for row in database_manager.load_sales_by_category():
        total_category = total_category + float(row[1])
    check('sales by month against the bills', format(total_month, '.2f'), format(total_python, '.2f'))
    check('sales by category against the bills', format(total_category, '.2f'),
          format(total_python, '.2f'))
    check('sales of the paid orders', format(total_python, '.2f'), '1458.50')

    cost_python = 0.0
    for myRestock in database_manager.load_restocks():
        cost_python = cost_python + myRestock.calculateCost()
    cost_supplier = 0.0
    for row in database_manager.load_restock_cost_by_supplier():
        cost_supplier = cost_supplier + float(row[2])
    check('restock cost by supplier against calculateCost()', format(cost_supplier, '.2f'),
          format(cost_python, '.2f'))
    check('total cost of the restocks', format(cost_python, '.2f'), '811.00')

    low_count = 0
    for row in database_manager.load_stock_levels():
        if row[2] <= 5:
            low_count = low_count + 1
    check('items with a stock of 5 or less', low_count, 4)

    print('\n' + str(len(failed_tests)) + ' test(s) NOT OK')
    for description in failed_tests:
        print('NOT OK:', description)


main()
