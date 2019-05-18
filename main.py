import sys
import os
import time
import sqlite3
from prettytable import from_db_cursor
from subprocess import call


def connect_db():
    clear()
    connection = sqlite3.connect('af.db')
    print('Database connected successfully!')
    time.sleep(1)
    return connection


def clear():
    tmp = call('clear' if os.name == 'posix' else 'cls', shell=True)


def main_menu():
    clear()
    print('*****Main Menu*****', '\n')
    print('Please select:')
    choice = input("""\nA: Manipulate Data \nB: Reports\n\n0: Exit\n""")

    if choice == 'A' or choice == 'a':
        mdata_menu()
    elif choice == 'B' or choice == 'b':
        reports_menu()
    elif choice == '0':
        clear()
        print('if you want to exit, type Yes:')
        ex = input()
        if ex == 'Yes':
            clear()
            sys.exit()
        else:
            main_menu()
    else:
        retry()
        main_menu()


def mdata_menu():
    clear()
    print('*****Manipulate Data Menu*****')
    print('Please select:')
    choice = input("""\nA: Items\nB: Staffs\nC: Store Houses\nD: Stock\n\n0: Back\n""")
    if choice == 'A' or choice == 'a':
        items_menu()
    elif choice == 'B' or choice == 'b':
        staffs_menu()
    elif choice == 'C' or choice == 'c':
        house_menu()
    elif choice == 'D' or choice == 'd':
        stock_menu()
    elif choice == '0':
        main_menu()
    else:
        retry()
        mdata_menu()


def items_menu():
    clear()
    print('*****Items Menu*****')
    print('Please select:')
    choice = input("""\nA: Add Item\nB: Delete Item\n\n0: Back\n\n""")
    if choice == 'A' or choice == 'a':
        add_item()
    elif choice == 'B' or choice == 'b':
        del_item()
    elif choice == '0':
        mdata_menu()
    else:
        retry()
        items_menu()


def add_item():
    clear()
    name = input('Name: ')
    price = float(input('Price: '))
    conn.execute('insert into Items (Name, Price) values (\'%s\',%.2f)' % (name, price))
    clear()
    print('%s with price %.2f added successfully!' % (name, price))
    conn.commit()
    time.sleep(2)
    items_menu()


def del_item():
    items_menu()


def staffs_menu():
    clear()
    print('*****Staffs Menu*****')
    print('Please select:')
    choice = input("""\nA: Add Staff\nB: Delete Staff\n\n0: Back\n\n""")
    if choice == 'A' or choice == 'a':
        add_staff()
    elif choice == 'B' or choice == 'b':
        del_staff()
    elif choice == '0':
        mdata_menu()
    else:
        retry()
        staffs_menu()


def add_staff():
    clear()
    name = input('Name: ')
    conn.execute('insert into Staffs (Name) values (\'%s\')' % name)
    clear()
    print('%s added successfully!' % name)
    conn.commit()
    time.sleep(2)
    staffs_menu()


def del_staff():
    staffs_menu()


def house_menu():
    clear()
    print('*****Store House Menu*****')
    print('Please select:')
    choice = input("""\nA: Add Store House\nB: Delete Store House\n\n0: Back\n\n""")
    if choice == 'A' or choice == 'a':
        add_house()
    elif choice == 'B' or choice == 'b':
        del_house()
    elif choice == '0':
        mdata_menu()
    else:
        retry()
        house_menu()


def add_house():
    clear()
    city = ''
    while len(city) <= 0:
        clear()
        city = input('City: ')
    clear()
    mid = ''
    while mid == '':
        clear()
        for stf in conn.execute('select * from Staffs'):
            print(stf, end='\t')
        mid = input('\nManagement ID: ')
    mid = int(mid)
    conn.execute('insert into StoreHouses (City, MID) values (\'%s\',%d)' % (city, mid))
    clear()
    print('Store House in %s with Management ID %d added successfully!' % (city, mid))
    conn.commit()
    time.sleep(2)
    house_menu()


def del_house():
    house_menu()


def stock_menu():
    clear()
    print('*****Stock Menu*****')
    print('Please select:')
    choice = input("""\nA: Add Stock\nB: Delete\n\n0: Back\n\n""")
    if choice == 'A' or choice == 'a':
        add_stock()
    elif choice == 'B' or choice == 'b':
        del_stock()
    elif choice == '0':
        mdata_menu()
    else:
        retry()
        stock_menu()


def add_stock():
    clear()
    ID = ''
    while ID == '':
        clear()
        for iid in conn.execute('select ID,Name from Items'):
            print(iid, end='\t')
        ID = input('\nItem ID: ')
    clear()
    ID = int(ID)
    SID = ''
    while SID == '':
        clear()
        for sh in conn.execute('select ID,City from StoreHouses'):
            print(sh, end='\t')
        SID = input('\nStore House ID: ')
    SID = int(SID)
    quantity = ''
    while quantity == '':
        clear()
        quantity = input('Quantity: ')
    quantity = int(quantity)
    conn.execute('insert into Stock values (%d,%d,%d)' % (ID, SID, quantity))
    clear()
    print('%d item %d added to Store House %d successfully!' % (quantity, ID, SID))
    conn.commit()
    time.sleep(2)
    stock_menu()


def del_stock():
    stock_menu()


def reports_menu():
    clear()
    print('*****Reports Menu*****')
    print('Please Select:')
    choice = input(
        """\nA: Number of items available in all store houses\nB: Value of each store house\nC: Staffs\nD: Total items of each city\nE: Total value of items managed by each staff\n\n0: Back\n""")
    if choice == 'A' or choice == 'a':
        report_sum_quan()
    elif choice == 'B' or choice == 'b':
        report_store_value()
    elif choice == 'C' or choice == 'c':
        report_staffs()
    elif choice == 'D' or choice == 'd':
        report_item_city()
    elif choice == 'E' or choice == 'e':
        report_staff_value()
    elif choice == '0':
        main_menu()
    else:
        retry()
        reports_menu()


def report_sum_quan():
    clear()
    print("Number of items available in all store houses:\n")
    print(from_db_cursor(
        conn.execute('select Name,sum(Quantity) from Items join Stock on (Items.ID = Stock.ID) group by Name')))
    tmp = input()
    reports_menu()


def report_store_value():
    clear()
    print('Value of each store house:\n')
    print(from_db_cursor(conn.execute(
        'select StoreHouses.ID,StoreHouses.City,sum(Quantity * Price) as Total from Stock join Items on (Items.ID = Stock.ID) join StoreHouses on (Stock.SID = StoreHouses.ID) group by StoreHouses.ID')))
    tmp = input()
    reports_menu()


def report_staffs():
    clear()
    print('Staffs name and city:\n')
    print(from_db_cursor(
        conn.execute('select Name,City,StoreHouses.ID from Staffs join StoreHouses on (Staffs.ID = StoreHouses.MID)')))
    tmp = input()
    reports_menu()


def report_item_city():
    clear()
    print('Total items of each city:\n')
    print(from_db_cursor(conn.execute(
        'select City,sum(Quantity) from Stock join StoreHouses on (Stock.SID = StoreHouses.ID) group by City')))
    tmp = input()
    reports_menu()


def report_staff_value():
    clear()
    print('Total value of items managed by each staff:\n')
    print(from_db_cursor(conn.execute(
        'select Staffs.Name, sum(Quantity) from Staffs join StoreHouses on (Staffs.ID = StoreHouses.MID) join Stock on (Stock.SID = StoreHouses.ID) group by Staffs.Name')))
    tmp = input()
    reports_menu()


def retry():
    clear()
    print("Try Again!!")
    time.sleep(1)


conn = connect_db()
main_menu()
