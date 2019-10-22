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

def getName(prompt, length):
    while True:
        try:
            name = input(prompt)
            assertAlpha(name)
            assertLength(name, length)
        except AssertionError as error:
            print(error)
        else:
            break
    return name

# allowNull is a bool, 1 if the date is allowed to be null, 0 otherwise
def getDate(prompt, cur_date, allowNull):
    while True:
        try:
            date = input(prompt)
            if allowNull and len(date) == 0:
                date = None
            else:
                if datetime.datetime.strptime(date, '%Y-%m-%d').date() > cur_date:
                    raise IndexError()
        except ValueError:
            print('Invalid Date Format')
        except IndexError:
            print('Date cannot be in the future')
        else:
            break
    return date

def getBPlace(prompt, length, allowNull):
    while True:
        try:
            bplace = input(prompt)
            if allowNull and len(bplace) == 0:
                bplace = None
            else:
                assertLength(bplace, length)
        except AssertionError as error:
            print(error)
        else:
            break
    return bplace

def getAddress(prompt, length):
     while True:
        try:
            address = input(prompt)
            if allowNull and len(address) == 0:
                address = None
            else:
                assertLength(address, length)
        except AssertionError as error:
            print(error)
        else:
            break
        return address

def getPhone(prompt, length):
    while True:
        try:
            phone = input(prompt)
            if allowNull and len(phone) == 0:
                phone = None
            else:
                if len(phone) != 12:
                    raise AssertionError('Must be 12 characters')
        except AssertionError as error:
            print(error)
        else:
            break
    return phone
   

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
    fname = getName('First name: ', 12)
    lname = getName('Last name: ', 12)

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

    bdate = getDate('Birth date (YYYY-MM-DD): ', cur_date, 0)
    bplace = getBPlace('Birth Place: ', 20, 0)
            
    f_fname = getName('Father\'s first name: ', 12)
    f_lname = getName('Father\'s last name: ', 12)
    m_fname = getName('Mother\'s first name: ', 12)
    m_lname = getName('Mother\'s last name: ', 12)

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
        print('If you do not want to provide a certain value, just hit enter to skip that value')
        m_bdate = getDate('Birth date (YYYY-MM-DD): ', cur_date, 1)
        m_bplace = getBPlace('Birth place: ', 20, 1)
        address = getAddress('Address: ', 30)
        phone = getPhone('Phone number: ', 12)
        
    # give newborn the mother's address and phone
    else:
        mother = mother[0]  # extract tuple from list of tuple
        address = mother[4]
        phone = mother[5]

    
    c.execute('SELECT * FROM persons WHERE fname = :fname COLLATE NOCASE and lname = :lname COLLATE NOCASE;', {'fname':m_fname, 'lname':m_lname})
    mother = c.fetchall()





