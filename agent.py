# for all the functionalities of the agent
import sqlite3
import sys
import datetime
import time
from datetime import date

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
        if choice == '2':
            a2(c, connection)
        if choice == '3':
            a3(c, connection)
        if choice == '4':
            a4(c, connection)
        if choice == '5':
            a5(c, connection)
        if choice == '6':
            a6(c, connection)

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

def a4(c, connection):

    vin = input("Enter VIN: ")
    sf_name = input("Enter seller's first name: ")
    sl_name = input("Enter seller's last name: ")
    bf_name = input("Enter buyer's first name: ")
    bl_name = input("Enter buyer's last name: ")
    plate = input("Enter the plate number: ")

    c.execute("SELECT R.fname FROM vehicles V, registrations R WHERE V.vin = R.vin AND vin=? ORDER BY regdate DESC LIMIT 1;", (vin))
    cf_name = fetchone()
    c.execute("SELECT R.lname FROM vehicles V, registrations R WHERE V.vin = R.vin AND vin=? ORDER BY regdate DESC LIMIT 1;", (vin))
    cl_name = fetchone()

    if cf_name != sf_name or cl_name != sl_name:
        raise AssertionError("You are not the current owner of the car! Dialing 911...")

    current_date = datetime.date.today()
    c.execute('''UPDATE registrations SET expiry=? WHERE registrations.fname=? AND registrations.lname=?;''', (current_date, cf_name, cl_name))

    c.execute("SELECT regno FROM registrations ORDER BY regno DESC")
    new_regno = fetchone()
    new_reg = (new_regno+1, current_date, plate, vin, bf_name, bl_name)
    c.execute("INSERT INTO registrations () VALUES (?,?, DATE('now', +1 year),?,?,?,?);", new_reg)

def a5(c, connection):

    tno = input("Enter ticket number: ")

    try:
        int(tno)
    except ValueError as error:
        print(error)

    c.execute("SELECT fine FROM tickets, payments WHERE tickets.tno = payments.tno AND tno=?;", (tno))
    fine = fetchone()
    pdate = datetime.date.today()
    amount = input("Enter ticket number: ")
    payment = (tno, pdate, amount)
    c.execute("INSERT INTO payments (tno, pdate, amount) VALUES (?,?,?);", payment)

    if (len(fine) == 0):
        raise AssertionError("You must enter a valid ticket number.")

    while ((fine - amount) != 0):
        try:
            tno = input("Enter ticket number: ")
            amount = input("Enter amount: ")
            pdate = datetime.date.today()
            payment = (tno, pdate, amount)
            c.execute("INSERT INTO payments (tno, pdate, amount) VALUES (?,?,?);", payment)

        except AssertionError as error:
            print(error)

def a6(c, connection):

    fname = input("Enter your first name: ")
    lname = input("Enter your last name: ")
    option = input("Press 't' if you would like to see your tickets ordered from latest to oldest")

    if lower.option() == "t":
        c.execute("SELECT tickets.tno FROM tickets, registrations WHERE tickets.fname = registrations.fname AND tickets.lname = registrations.lname ORDER BY tno DESC")

    c.execute("SELECT COUNT(T.tno) FROM tickets, registrations WHERE tickets.fname = registrations.fname AND tickets.lname = registrations.lname")
    num_tkts = c.fetchone()
    c.execute("SELECT COUNT(*) FROM demeritNotices D, registrations WHERE D.fname = registrations.fname AND D.lname = registrations.lname")
    num_dem = c.fetchone()
    c.execute("SELECT D.SUM(points) FROM demeritNotices D, registrations WHERE D.fname = registrations.fname AND D.lname = registrations.lname AND DATE('')")
    pts_2 = c.fetchone()
    c.execute("SELECT D.SUM(points) FROM demeritNotices D, registrations WHERE D.fname = registrations.fname AND D.lname = registrations.lname AND DATE('')")
    pts_life = c.fetchone()


Get a driver abstract.The user should be able to enter a first name and a last name and get a driver abstract, 
which includes the number of tickets, the number of demerit notices, the total number of demerit points received both within 
the past two years and within the lifetime. The user should be given the option to see the tickets ordered from the latest to 
the oldest. For each ticket, you will report the ticket number, the violation date, the violation description, the fine, the 
registration number and the make and model of the car for which the ticket is issued. If there are more than 5 tickets, at most 5 
tickets will be shown at a time, and the user can select to see more.


persons(fname, lname, bdate, bplace, address, phone)
births(regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname)
marriages (regno, regdate, regplace, p1_fname, p1_lname, p2_fname, p2_lname)
vehicles(vin,make,model,year,color)
registrations(regno, regdate, expiry, plate, vin, fname, lname)
tickets(tno,regno,fine,violation,vdate)
demeritNotices(ddate, fname, lname, points, desc)
payments(tno, pdate, amount) 
users(uid, pwd, utype, fname, lname, city)