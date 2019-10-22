# for all the functionalities of the agent
import sqlite3
import sys
import datetime
import time

def clear_screen():
    print('----------------------------------------------------------------------------------------------')
    print('\n\n\n\n')

def assertAlpha(value):
    if not value.isalpha():
        raise AssertionError('Error: Can only contain alphabetical characters')

def assertLength(value, length):
    if len(value) > length or len(value) <= 0:
        raise AssertionError('Error: Must be between 1 and %d characters' % (length))



def agent_menu(user, c, connection):
    logout = False
    clear_screen()
    print('Hello Agent', user[4])

    while logout == False:
        print('Please choose a task: ')
        print('\nEnter "exit" to exit or "logout" to logout')
        print('1. Register a birth')
        print('2. Register a marriage')
        print('3. Renew a vehicle registration')
        print('4. Process a bill of sale')
        print('5. Process a payment')
        print('6. Get a driver abstract')
        choice = input('Choice: ')
	
        clear_screen()

        if choice == 'exit':
            sys.exit()
        if choice == 'logout':
            return
        if choice == '1':
            a1(c, connection)

def a1(c, connection):
    cur_date = datetime.date.today()

    # get all user input
    print('Please provide the following information for the birth: ')
    while True:
        try:
            fname = input('First name: ')
            assertAlpha(fname)
            assertLength(fname, 12)
        except AssertionError as error:
            print(error)
        else:
            break

    while True:
        try:
            lname = input('Last name: ')
            assertAlpha(lname)
            assertLength(lname, 12)
        except AssertionError as error:
            print(error)
        else:
            break

    while True:
        try:
            gender = input('Gender (M or F): ')
            if len(gender) != 1:
                raise AssertionError('Must be 1 character')
            assertAlpha(gender)
            if gender.lower() == 'm' or gender.lower() == 'f':
                break
            else:
                raise AssertionError('Gender must be M or F')
        except AssertionError as error:
            print(error)
        else:
            break

    while True:
        try:
            bdate = input('Birth date (YYYY-MM-DD): ')
            if datetime.datetime.strptime(bdate, '%Y-%m-%d').date() > cur_date:
                raise IndexError()
        except ValueError:
            print('Invalid Date Format')
        except IndexError:
            print('Date cannot be in the future')
        else:
            break
            
    while True:
        try:
            bplace = input('Birth place: ')
            assertLength(bplace, 20)
        except AssertionError as error:
            print(error)
        else:
            break

    while True:
        try:
            f_fname = input('Father\'s first name: ')
            assertAlpha(f_fname)
            assertLength(f_fname, 12)
        except AssertionError as error:
            print(error)
        else:
            break

    while True:
        try:
            lname = input('Father\'s last name: ')
            assertAlpha(f_lname)
            assertLength(f_lname, 12)
        except AssertionError as error:
            print(error)
        else:
            break

    while True:
        try:
            m_fname = input('Mother\'s first name: ')
            assertAlpha(m_fname)
            assertLength(m_fname, 12)
        except AssertionError as error:
            print(error)
        else:
            break

    while True:
        try:
            lname = input('Mother\'s last name: ')
            assertAlpha(m_lname)
            assertLength(m_lname, 12)
        except AssertionError as error:
            print(error)
        else:
            break

    # make unique regno
    c.execute('SELECT regno FROM births;')
    temp = c.fetchall()
    used_regno = []
    for num in temp:
        used_regno.append(num[0])

    regno = 1
    while regno in used_regno:
        regno += 1

    # check if mother is in db
    c.execute('SELECT * FROM persons WHERE fname = :fname COLLATE NOCASE and lname = :lname COLLATE NOCASE;', {'fname':m_fname, 'lname':m_lname})
    mother = c.fetchall()
    
    # prompt user for mother's info
    if len(mother) == 0:
        print('Please provide the following information for the mother: ')
        print('If you do not want to provide a certain value, just hit enter')
        m_bdate = input('Birth date: ')
        m_bplace = input
        
    # give newborn the mother's address and phone
    else:
        mother = mother[0]  # extract tuple from list of tuple
        address = mother[4]
        phone = mother[5]



 
