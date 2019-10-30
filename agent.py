import sqlite3
import sys
import datetime
import time
from datetime import date

# clears the screen
def clear_screen():
    print('----------------------------------------------------------------------------------------------')
    print('\n\n\n\n')

# raises an assertion if value is not alphabetical
def assertAlpha(value):
    if not value.isalpha():
        raise AssertionError('*** CAN ONLY BE ALPHABETICAL CHARACTERS ***')

# raises an assertion if the length of value is not within the
# length bounds of its corresponding value in the database
def assertLength(value, length):
    if len(value) > length or len(value) <= 0:
        raise AssertionError('*** MUST BE BETWEEN 1 AND %d CHARACTERS ***' % (length))

# prompts for a name and returns it
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

# prompts for a date and returns it
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
            print('*** INVALID DATE FORMAT ***')
        except IndexError:
            print('*** CANNOT BE IN THE FUTURE ***')
        else:
            break
    return date

# prompts for a birth place and returns it
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

# prompts for an address and returns it
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

# prompts for a phone number and returns it
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
                    raise AssertionError('*** MUST BE 12 CHARACTERS ***')
        except AssertionError as error:
            print(error)
        else:
            break
    return phone  

# the agent menu, showing the operations that agents can choose from
# and allows them to logout or exit
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
        clear_screen()

# contains the functionality for option 1
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
                raise AssertionError('*** MUST BE 1 CHARACTER ***')
            assertAlpha(gender)
            if gender.lower() == 'm' or gender.lower() == 'f':
                break
            else:
                raise AssertionError('*** GENDER MUST BE M OR F ***')
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
   
# contains the functionality for option 2
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

# contains the functionality for option 3
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
            print('*** MUST BE AN INTEGER ***')
        else:
           # get regno from db
            c.execute('SELECT * FROM registrations WHERE regno = :num;', {'num':num})
            registration = c.fetchone()
    
            # if regno is not in system
            if registration == None:
                print('*** That registration number is not in our system. Please try again. ***')
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
    
    while True:
        try:
            vin = input("Enter VIN: ")
            if vin.lower() == "quit":
                return

            c.execute("SELECT * FROM registrations WHERE vin = ? COLLATE NOCASE;", (vin,))
            if len(c.fetchall()) == 0:
                raise AssertionError("*** VIN DOES NOT EXIST ***")
        except AssertionError as error:
            print(error)
        else:
            break

    sf_name = input("Enter current owner's first name: ")
    if sf_name.lower() == "quit":
        return

    sl_name = input("Enter current owner's last name: ")
    if sl_name.lower() == "quit":
        return
    bf_name = input("Enter buyer's first name: ")
    if bf_name.lower() == "quit":
        return
    bl_name = input("Enter buyer's last name: ")
    if bl_name.lower() == "quit":
        return
    plate = input("Enter the plate number: ")
    if plate.lower() == "quit":
        return

    #Retrieving first name of current owner of car
    c.execute("SELECT R.regno, R.fname, R.lname FROM vehicles V, registrations R WHERE V.vin = R.vin AND R.vin=? COLLATE NOCASE ORDER BY regdate DESC LIMIT 1;", (vin,))
    current_owner = c.fetchone()

    #Check if current owner's name is the same as seller's name
    if current_owner[1] != sf_name or current_owner[2] != sl_name:
        print("*** You are not the current owner of the car! Dialing 911... ***")
        garbage = input('Press Enter to Continue')
        return
    
    # Check if the new owner is in the persons table
    c.execute('SELECT * FROM persons WHERE fname = ? and lname = ?;', (bf_name, bl_name))
    if len(c.fetchall()) == 0:
        print("*** The new owner does not exist in our database ***")
        garbage = input('Press Enter to Continue')
        return

    #Update the expiry date of the current owner's car registration to current date
    current_date = datetime.date.today()
    c.execute('''UPDATE registrations SET expiry=? WHERE regno = ?;''', (current_date, current_owner[0]))

    #Select the most recent registration number
    c.execute("SELECT regno FROM registrations ORDER BY regno DESC")
    new_regno = c.fetchone()[0] + 1

    #Insert new owner's information
    new_expiry = current_date.replace(year = current_date.year + 1)
    new_reg = (new_regno, current_date, new_expiry, plate, vin, bf_name, bl_name)
    c.execute("INSERT INTO registrations (regno, regdate, expiry, plate, vin, fname, lname) VALUES (?,?,?,?,?,?,?);", new_reg)
    connection.commit()

def a5(c, connection):

    while True:
            try:
                tno = input("Enter ticket number: ")
                if tno.lower() == "quit":
                    return
                int(tno)
                c.execute("SELECT * FROM tickets WHERE tno = ?;", (tno,))
                if len(c.fetchall()) == 0:
                    raise AssertionError("*** TICKET NUMBER DOES NOT EXIST ***")
            except AssertionError as error:
                print(error)
            except ValueError:
                #Ticket number may only contain numbers
                print("*** TICKET NUMBER CAN ONLY BE INTEGERS ***")
            else:
                break

    #Retrieve fine amount from ticket issued
    c.execute("SELECT amount FROM payments WHERE tno=?;", (tno,))
    temp = c.fetchall()
    fine_total = 0
    for x in temp:
        fine_total = fine_total + int(x[0])
    
    c.execute("SELECT fine FROM tickets WHERE tno = ?;",(tno,))
    fine_remaining = c.fetchone()[0] - fine_total

    if fine_remaining == 0:
        print("*** THIS TICKET HAS ALREADY BEEN PAID OFF ***")
        garbage = input('Press Enter to Continue')
        return

    while True:
        try:
            amount = input("Enter a payment amount: ")
            if amount.lower() == "quit":
                return
            amount = int(amount)

            if amount <= 0:
                raise AssertionError("*** MUST BE GREATER THAN 0 ***")
            if amount > fine_remaining:
                raise AssertionError("*** PAYING MORE THAN FINE REMAINING ($%d) ***" % (fine_remaining))
        
        except ValueError:
            print("*** ONLY INTEGERS ALLOWED ***")
        except AssertionError as error:
            print(error)
        else:
            break

    #Insert new information of amount paid
    pdate = datetime.date.today()
    payment = (tno, pdate, amount)
    try:
        c.execute("INSERT INTO payments (tno, pdate, amount) VALUES (?,?,?);", payment)
        connection.commit()
    except sqlite3.IntegrityError:
        print("*** ALREADY PAID TODAY. PAYMENT REJECTED ***")
        garbage = input('Press Enter to Continue')
    else:
        garbage = input('Press Enter to Continue')

        

    #If the full amount is not paid off, user can choose to pay in lump payments
    #while ((fine - amount) != 0):
    #    try:
    #        tno = input("Enter ticket number: ")
    #        amount = input("Enter amount: ")
     #         pdate = datetime.date.today()
     #       payment = (tno, pdate, amount)
     #       c.execute("INSERT INTO payments (tno, pdate, amount) VALUES (?,?,?);", payment)
    #
     #   except AssertionError as error:
    #        print(error)

def a6(c, connection):

    clear_screen()

    fname = getName('First name: ', 12)
    if fname.lower() == "quit":
        return
    lname = getName('Last name: ', 12)
    if lname.lower() == "quit":
        return
    
    #Retrieves number of tickets user has
    c.execute("SELECT COUNT(*) FROM tickets T, registrations R WHERE R.fname = ? AND R.lname = ? AND R.regno = T.regno;", (fname, lname))
    num_tkts = c.fetchone()[0]

    #Retrieves number of demerit notices user has
    c.execute("SELECT COUNT(*) FROM demeritNotices WHERE fname = ? AND lname = ?;", (fname, lname))
    num_dem = c.fetchone()[0]

    #Retrieves sum of demerit points in the part 2 years
    c.execute("SELECT SUM(points) FROM demeritNotices WHERE fname = ? AND lname = ? AND ddate >= DATE('now', '-2 years');", (fname, lname))
    pts_2 = c.fetchone()[0]

    #Retrieves sum of demerit points during lifetime
    c.execute("SELECT SUM(points) FROM demeritNotices WHERE fname = ? AND lname = ?;", (fname, lname))
    pts_life = c.fetchone()[0]

    print("\nDriver Abstract:\n")
    print('First Name'.ljust(12, ' ') , ' ' , 'Last Name'.ljust(12, ' ') , ' ' , '# of Tickets'.ljust(12, ' ') , ' ' , 'Demerit Count'.ljust(12, ' ') , ' ', 'Dem. Points 2 Years'.ljust(12, ' '), ' ' , 
                'Dem. Points Lifetime'.ljust(12, ' ') + '\n')
    print(fname.ljust(12, ' ') , '|' , lname.ljust(12, ' ') , '|' , str(num_tkts).ljust(12, ' ') , '|' , str(num_dem).ljust(13, ' ') , '|', str(pts_2).ljust(19, ' ')
            , '|' , str(pts_life).ljust(12, ' ') + '\n')

    #Ordering tickets from latest -> oldest
    option = input("Press 't' if you would like to see your tickets ordered from latest to oldest: ")
    if option.lower() == "quit":
        return
    if option.lower() == "t":
        c.execute('''SELECT T.tno, T.vdate, T.violation, T.fine, T.regno, V.make, V.model 
                    FROM tickets T, registrations R, vehicles V 
                    WHERE T.regno = R.regno AND R.vin = V.vin AND R.fname = ? AND R.lname = ? ORDER BY T.vdate DESC;''', (fname, lname))
        all_tkts = c.fetchall()
    
        i = 0
        j = 0
        while (i < len(all_tkts)):
            j = 0
            print('\n\n\nTicket Num'.ljust(12, ' ') , ' ' , 'Vio. Date'.ljust(12, ' ') , ' ' , 'Vio. Descrip'.ljust(25, ' ') , ' ' , 'Fine'.ljust(12, ' ') , ' ' , 'Reg. Num.'.ljust(12, ' ') , ' ', 'Make'.ljust(12, ' '), ' ' , 
                'Model'.ljust(12, ' ') + '\n')
            while (j < 5 and i < len(all_tkts)):
                print(str(all_tkts[i][0]).ljust(12, ' ') , '|' , all_tkts[i][1].ljust(12, ' ') , '|' , '%.25s'%(all_tkts[i][2].ljust(25, ' ')) , '|' , str(all_tkts[i][3]).ljust(12, ' ') , '|', str(all_tkts[i][4]).ljust(12, ' ')
                        , '|' , all_tkts[i][5].ljust(12, ' '), '|' , all_tkts[i][6].ljust(12, ' '))
                j = j+1
                i = i+1
            
            if (i < len(all_tkts)):
                garbage = input("Press ''t'' to see more tickets: ")

                if garbage.lower() != 't':
                    garbage = input('Press Enter to Continue to the home screen')
                    return
    garbage = input('Press Enter to Continue')

