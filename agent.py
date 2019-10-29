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
            if name.lower() == "quit":
                break
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
            if date.lower() == "quit":
                break
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
            if bplace.lower() == "quit":
                break
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
            if address.lower() == "quit":
                break
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
            if phone.lower() == "quit":
                break
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
        #elif choice == '6':
            #a6(c, connection)
        else:
            print('You must enter either a number from the list of choices, \"exit\", or \"logout\"')
        clear_screen()

def a1(c, connection, user):
    cur_date = datetime.date.today()
    
    # get all user input
    print('Please provide the following information for the birth: ')
    print('If you want to quit the operation, enter \"quit\" at any time')
    fname = getName('First name: ', 12)
    if fname.lower() == "quit":
        return
    lname = getName('Last name: ', 12)
    if lname.lower() == "quit":
        return

    while True:
        try:
            gender = input('Gender (M or F): ')
            if gender.lower() == "quit":
                return
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
    if bdate.lower() == "quit":
        return
    bplace = getBPlace('Birth Place: ', 20, 0)
    if bplace.lower() == "quit":
        return           
    f_fname = getName('Father\'s first name: ', 12)
    if f_fname.lower() == "quit":
        return
    f_lname = getName('Father\'s last name: ', 12)
    if f_lname.lower() == "quit":
        return
    m_fname = getName('Mother\'s first name: ', 12)
    if m_fname.lower() == "quit":
        return
    m_lname = getName('Mother\'s last name: ', 12)
    if m_lname.lower() == "quit":
        return
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
        print('If you do not want to provide a certain value, hit enter to skip that value')
        m_bdate = getDate('Birth date (YYYY-MM-DD): ', cur_date, 1)
        if m_bdate == "quit":
            return
        m_bplace = getBPlace('Birth place: ', 20, 1)
        if m_bplace == "quit":
            return
        address = getAddress('Address: ', 30, 1)
        if address == "quit":
            return
        phone = getPhone('Phone number (123-456-7890): ', 12, 1)
        if phone == "quit":
            return
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
        print('If you do not want to provide a certain value, hit enter to skip that value')
        f_bdate = getDate('Birth date (YYYY-MM-DD): ', cur_date, 1)
        if f_bdate == "quit":
            return
        f_bplace = getBPlace('Birth place: ', 20, 1)
        if f_bplace == "quit":
            return
        f_address = getAddress('Address: ', 30, 1)
        if f_address == "quit":
            return
        f_phone = getPhone('Phone number (123-456-7890): ', 12, 1)
        if f_phone == "quit":
            return
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
    
def a2(c, connection, user):
    cur_date = datetime.date.today()

    # get partner names
    print('Please provide the following information for the marriage: ')
    print('If you want to quit the operation, enter \"quit\" at any time')
    p1_fname = getName('Partner 1\'s first name: ', 12)
    if p1_fname == "quit":
        return
    p1_lname = getName('Partner 1\'s last name: ', 12)    
    if p1_lname == "quit":
        return
    p2_fname = getName('Partner 2\'s first name: ', 12)
    if p2_fname == "quit":
        return
    p2_lname = getName('Partner 2\'s last name: ', 12)
    if p2_lname == "quit":
        return   

    # check if partner 1 is in db
    c.execute('SELECT * FROM persons WHERE fname = :fname COLLATE NOCASE and lname = :lname COLLATE NOCASE;', {'fname':p1_fname, 'lname':p1_lname})
    partner1 = c.fetchone()

    # get partner 1 info if not in db
    if partner1 == None:
        print('Please provide the following information about %s: ' % (p1_fname+' '+p1_lname))
        print('If you do not want to provide a certain value, just hit enter to skip that value')
        p1_bdate = getDate('Birth date (YYYY-MM-DD): ', cur_date, 1)
        if p1_bdate == "quit":
            return
        p1_bplace = getBPlace('Birth place: ', 20, 1)
        if p1_bplace == "quit":
            return
        p1_address = getAddress('Address: ', 30, 1)
        if p1_address == "quit":
            return
        p1_phone = getPhone('Phone number (123-456-7890): ', 12, 1)
        if p1_phone == "quit":
            return
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
        if p2_bdate == "quit":
            return
        p2_bplace = getBPlace('Birth place: ', 20, 1)
        if p2_bplace == "quit":
            return
        p2_address = getAddress('Address: ', 30, 1)
        if p2_address == "quit":
            return
        p2_phone = getPhone('Phone number (123-456-7890): ', 12, 1)
        if p2_phone == "quit":
            return
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
    
def a3(c, connection, user):
    print('Please provide the following information for the vehicle registration renewal: ')
    print('If you want to quit the operation, enter \"quit\" at any time')
    cur_date = datetime.date.today()
    while True:
        try:
            num = input('Registration number: ')
            if num == "quit":
                return
            # check input
            num = int(num)
        except ValueError:
            print('Must enter a number')
        else:
           # break
           # get regno from db
            c.execute('SELECT * FROM registrations WHERE regno = :num;', {'num':num})
            registration = c.fetchone()
    
            # if regno is not in system
            if registration == None:
                print('That registration number is not in our system. Please try again.')
            # regno in system
            else:
                break

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
    print('Registration successfully renewed. New expiry is', new_expiry)
    time.sleep(2)

def a4(c, connection):

    vin = input("Enter VIN: ")
    sf_name = input("Enter seller's first name: ")
    sl_name = input("Enter seller's last name: ")
    bf_name = input("Enter buyer's first name: ")
    bl_name = input("Enter buyer's last name: ")
    plate = input("Enter the plate number: ")

    #Retrieving first name of current owner of car
    c.execute("SELECT R.fname FROM vehicles V, registrations R WHERE V.vin = R.vin AND vin=? ORDER BY regdate DESC LIMIT 1;", (vin))
    cf_name = c.fetchone()

    #Retrieving last name of current owner of car
    c.execute("SELECT R.lname FROM vehicles V, registrations R WHERE V.vin = R.vin AND vin=? ORDER BY regdate DESC LIMIT 1;", (vin))
    cl_name = c.fetchone()

    #Check if current owner's name is the same as seller's name
    if cf_name != sf_name or cl_name != sl_name:
        raise AssertionError("You are not the current owner of the car! Dialing 911...")

    #Update the expiry date of the current owner's car registration to current date
    current_date = datetime.date.today()
    c.execute('''UPDATE registrations SET expiry=? WHERE registrations.fname=? AND registrations.lname=?;''', (current_date, cf_name, cl_name))

    #Select the most recent registration number
    c.execute("SELECT regno FROM registrations ORDER BY regno DESC")
    new_regno = c.fetchone()

    #Insert new owner's information
    new_reg = (new_regno+1, current_date, plate, vin, bf_name, bl_name)
    c.execute("INSERT INTO registrations () VALUES (?,?, DATE('now', +1 year),?,?,?,?);", new_reg)

def a5(c, connection):

    tno = input("Enter ticket number: ")

    #Ticket number may only contain numbers
    try:
        int(tno)
    except ValueError as error:
        print(error)

    #Retrieve fine amount from ticket issued
    c.execute("SELECT fine FROM tickets, payments WHERE tickets.tno = payments.tno AND tno=?;", (tno))
    fine = c.fetchone()

    #Check if ticket is valid
    if (len(fine) == 0):
        raise AssertionError("You must enter a valid ticket number.")

    pdate = datetime.date.today()
    amount = input("Enter ticket number: ")

    #Insert new information of amount paid
    payment = (tno, pdate, amount)
    c.execute("INSERT INTO payments (tno, pdate, amount) VALUES (?,?,?);", payment)

    #If the full amount is not paid off, user can choose to pay in lump payments
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
    vin = input("Enter VIN of car you would like to see information: ")
    
    #Retrieves number of tickets user has
    c.execute("SELECT COUNT(T.tno) FROM tickets T, registrations R WHERE T.fname = R.fname AND T.lname = R.lname AND fname = ? AND lname = ?", (fname, lname))
    num_tkts = c.fetchone()

    #Retrieves number of demerit notices user has
    c.execute("SELECT COUNT(D.desc) FROM demeritNotices D, registrations R WHERE D.fname = R.fname AND D.lname = R.lname AND fname = ? AND lname = ?", (fname, lname))
    num_dem = c.fetchone()

    #Retrieves sum of demerit points in the part 2 years
    c.execute("SELECT SUM(D.points) FROM demeritNotices D, registrations R WHERE D.fname = R.fname AND D.lname = R.lname AND fname = ? AND lname = ? AND DATE('now', '-2 years')", (fname, lname))
    pts_2 = c.fetchone()

    #Retrieves sum of demerit points during lifetime
    c.execute("SELECT SUM(D.points) FROM demeritNotices D, registrations R WHERE D.fname = R.fname AND D.lname = R.lname AND fname = ? AND lname = ? AND DATE('')", (fname, lname))
    pts_life = c.fetchone()

    print("#Tickets: ", (num_tkts))
    print("#DemeritNotices: ", (num_dem))
    print("Total Demerit Pts. (2Years): ", (pts_2))
    print("Total Demerit Pts. (Life): ", (pts_life))

    #Ordering tickets from latest -> oldest
    option = input("Press 't' if you would like to see your tickets ordered from latest to oldest")
    if option.lower() == "t":
        c.execute("SELECT T.*, V.make, V.model FROM tickets T, registrations R, vehicles V WHERE T.fname = R.fname AND T.lname = R.lname AND R.vin = V.vin AND fname = ? AND lname = ? AND vin = ? ORDER BY tno DESC", (fname, lname, vin))
        all_tkts = c.fetchall()
    
    #Check to see if there are more than 5 tickets
    if len(all_tkts) > 5:
        c.execute("SELECT T.*, V.make, V.model FROM tickets T, registrations R, vehicles V WHERE T.fname = R.fname AND T.lname = R.lname AND R.vin = V.vin AND fname = ? AND lname = ? AND vin = ? ORDER BY tno DESC LIMIT 5", (fname, lname, vin))
        all_tkts = c.fetchall()

    #Printing information of tickets
    for ticket in all_tkts:
        tno = ticket[0]
        vdate = ticket[4]
        violation = ticket[3]
        fine = ticket[2]
        regno = ticket[1]
        make = ticket[5]
        model = ticket[6]
        print("| %d | %Y%d%d | %s | %f | %d | %s | %s |\n", (tno, vdate, violation, fine, regno, make, model))
