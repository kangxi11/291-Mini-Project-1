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
        raise AssertionError('Can only contain alphabetical characters')

def assertLength(value, length):
    if len(value) > length or len(value) <= 0:
        raise AssertionError('Must be between 1 and %d characters' % (length))

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

def getAddress(prompt, length, allowNull):
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

def getPhone(prompt, length, allowNull):
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
        elif choice == 'logout':
            return
        elif choice == '1':
            a1(c, connection, user)
        elif choice == '2':
            a2(c, connection, user)
        elif choice == '3':
            a3(c, connection, user)
        elif choice == '4':
            a4(c, connection)
        elif choice == '5':
            a5(c, connection)
        elif choice == '6':
            a6(c, connection)
        else:
            print('You must enter either a number from the list of choices, \"exit\", or \"logout\"')

def a1(c, connection, user):
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
    mother = c.fetchone()
    
    # prompt user for mother's info
    if mother == None:
        print('Please provide the following information about the mother: ')
        print('If you do not want to provide a certain value, just hit enter to skip that value')
        m_bdate = getDate('Birth date (YYYY-MM-DD): ', cur_date, 1)
        m_bplace = getBPlace('Birth place: ', 20, 1)
        address = getAddress('Address: ', 30, 1)
        phone = getPhone('Phone number (123-456-7890): ', 12, 1)
        # insert her into persons
        c.execute('INSERT INTO persons (fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?);', (m_fname, m_lname, m_bdate, m_bplace, address, phone))
        connection.commit()
        c.execute('SELECT * FROM persons WHERE fname = :fname COLLATE NOCASE and lname = :lname COLLATE NOCASE;', {'fname':m_fname, 'lname':m_lname})
        mother = c.fetchone()        
        
    # give newborn the mother's address and phone
    else:
        address = mother[4]
        phone = mother[5]

    # check if father is in db
    c.execute('SELECT * FROM persons WHERE fname = :fname COLLATE NOCASE and lname = :lname COLLATE NOCASE;', {'fname':f_fname, 'lname':f_lname})
    father = c.fetchone()

    if father == None:
        print('Please provide the following information about the father: ')
        print('If you do not want to provide a certain value, just hit enter to skip that value')
        f_bdate = getDate('Birth date (YYYY-MM-DD): ', cur_date, 1)
        f_bplace = getBPlace('Birth place: ', 20, 1)
        f_address = getAddress('Address: ', 30, 1)
        f_phone = getPhone('Phone number (123-456-7890): ', 12, 1)
        # insert him into persons
        c.execute('INSERT INTO persons (fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?);', (f_fname, f_lname, f_bdate, f_bplace, f_address, f_phone))
        connection.commit()
        # get father's info from db
        c.execute('SELECT * FROM persons WHERE fname = :fname COLLATE NOCASE and lname = :lname COLLATE NOCASE;', {'fname':f_fname, 'lname':f_lname})
        father = c.fetchone()
        
    # put newborn into persons
    c.execute('INSERT INTO persons (fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?);', (fname, lname, bdate, bplace, address, phone))
    # put birth into db
    c.execute('INSERT INTO births (regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname) VALUES (?,?,?,?,?,?,?,?,?,?);', (regno, fname, lname, cur_date, user[5], gender, father[0], father[1], mother[0], mother[1]))
    connection.commit()
    
    print('Birth successfully registered.')
    time.sleep(2)
    clear_screen()
    
def a2(c, connection, user):
    cur_date = datetime.date.today()

    # get partner names
    print('Please provide the following information for the marriage: ')
    p1_fname = getName('Partner 1\'s first name: ', 12)
    p1_lname = getName('Partner 1\'s last name: ', 12)    
    p2_fname = getName('Partner 2\'s first name: ', 12)
    p2_lname = getName('Partner 2\'s last name: ', 12)
    
    # check if partner 1 is in db
    c.execute('SELECT * FROM persons WHERE fname = :fname COLLATE NOCASE and lname = :lname COLLATE NOCASE;', {'fname':p1_fname, 'lname':p1_lname})
    partner1 = c.fetchone()

    # get partner 1 info if not in db
    if partner1 == None:
        print('Please provide the following information about %s: ' % (p1_fname+' '+p1_lname))
        print('If you do not want to provide a certain value, just hit enter to skip that value')
        p1_bdate = getDate('Birth date (YYYY-MM-DD): ', cur_date, 1)
        p1_bplace = getBPlace('Birth place: ', 20, 1)
        p1_address = getAddress('Address: ', 30, 1)
        p1_phone = getPhone('Phone number (123-456-7890): ', 12, 1)
        # insert partner 1 into persons
        c.execute('INSERT INTO persons (fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?);', (p1_fname, p1_lname, p1_bdate, p1_bplace, p1_address, p1_phone))
        connection.commit()
        # get partner 1's info from db
        c.execute('SELECT * FROM persons WHERE fname = :fname COLLATE NOCASE and lname = :lname COLLATE NOCASE;', {'fname':p1_fname, 'lname':p1_lname})
        partner1 = c.fetchone()

    # check if partner 2 is in db
    c.execute('SELECT * FROM persons WHERE fname = :fname COLLATE NOCASE and lname = :lname COLLATE NOCASE;', {'fname':p2_fname, 'lname':p2_lname})
    partner2 = c.fetchone()

    # get partner 2 info if not in db
    if partner2 == None:
        print('Please provide the following information about %s: ' % (p2_fname+' '+p2_lname))
        print('If you do not want to provide a certain value, just hit enter to skip that value')
        p2_bdate = getDate('Birth date (YYYY-MM-DD): ', cur_date, 1)
        p2_bplace = getBPlace('Birth place: ', 20, 1)
        p2_address = getAddress('Address: ', 30, 1)
        p2_phone = getPhone('Phone number (123-456-7890): ', 12, 1)
        # insert partner 2 into persons
        c.execute('INSERT INTO persons (fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?);', (p2_fname, p2_lname, p2_bdate, p2_bplace, p2_address, p2_phone))
        connection.commit()
        # get partner 2's info from db
        # this gives case insensitivity when registering same person for 2 different marriages
        c.execute('SELECT * FROM persons WHERE fname = :fname COLLATE NOCASE and lname = :lname COLLATE NOCASE;', {'fname':p2_fname, 'lname':p2_lname})
        partner2 = c.fetchone()        
    
    # make unique regno
    c.execute('SELECT regno FROM marriages;')
    temp = c.fetchall()
    used_regno = []
    for num in temp:
        used_regno.append(num[0])

    regno = 1
    while regno in used_regno:
        regno += 1
        
    # put marriage into db
    c.execute('INSERT INTO marriages (regno, regdate, regplace, p1_fname, p1_lname, p2_fname, p2_lname) VALUES (?,?,?,?,?,?,?);', (regno, cur_date, user[5], partner1[0], partner1[1], partner2[0], partner2[1]))
    connection.commit()

    print('Marriage successfully registered.')
    time.sleep(2)
    clear_screen()
    
def a3(c, connection, user):
    cur_date = datetime.date.today()
    while True:
        try:
            num = input('Please enter the registration number to renew: ')
            # check input
            num = int(num)
        except ValueError:
            print('Must enter a number')
        else:
            break
    # get regno from db
    c.execute('SELECT * FROM registrations WHERE regno = :num;', {'num':num})
    registration = c.fetchone()
    
    # if regno is not in system
    if registration == None:
        print('That registration number is not in our system.\nReturning to menu screen.')
        time.sleep(2)
        clear_screen()
        
    # regno in system
    else:
        old_expiry = datetime.datetime.strptime(registration[2], '%Y-%m-%d').date()
        # set new expiry to one year from now
        if old_expiry <= cur_date:
            new_expiry = cur_date.replace(year = cur_date.year + 1)
            c.execute('UPDATE registrations SET expiry = ? WHERE regno = ?;', (new_expiry, registration[0]))
            connection.commit()
        # set new expiry to one year from current expiry
        else:
            new_expiry = old_expiry.replace(year = old_expiry.year + 1)
            c.execute('UPDATE registrations SET expiry = ? WHERE regno = ?;', (new_expiry, registration[0]))
            connection.commit()            
        print('Registration successfully renewed.')
        time.sleep(2)
        clear_screen()        

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

