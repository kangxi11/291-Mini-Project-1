# for all the functionalities of the officer
import sqlite3
import time
import datetime
import sys

def clear_screen():
    print('----------------------------------------------------------------------------------------------')
    print('\n\n\n\n')

def officer_menu(user, c, connection):
    logout = False
    
    while logout == False:
        clear_screen()
        
        print('Hello Officer', user[4])
        print('Please choose a task: ')

        print('\nEnter "exit" to exit or "logout" to logout')
        print('1. Issue a Ticket')
        print('2. Find a Car Owner')
        choice = input('Choice: ')

        clear_screen()

        if choice == 'exit':
            sys.exit()
        if choice == 'logout':
            return
        if choice == '1':
            o1(c, connection)
        if choice == '2':
            o2(c, connection)

def o1(c, connection):

    print('Please provide the following information to issue a ticket: ')
    print('If you want to quit the operation, enter \"quit\" at any time')

    while True:
        try:
            uRegno = input('Registration Number: ')
            if uRegno.lower() == "quit":
                return
            c.execute ("SELECT * FROM registrations WHERE regno = ?;", (uRegno, ))
            reg = c.fetchall()

            if len(reg) == 0:
                raise AssertionError("*** Registration Number Not Found ***")
        
        except AssertionError as error:
            print(error)

        else:
            reg = reg[0]
            break
    
    c.execute("SELECT * FROM vehicles WHERE vin = ? COLLATE NOCASE;", (reg[4], ))
    vehicle = c.fetchone()

    print(reg[5], reg[6], '|', vehicle[1], '|', vehicle[2], '|', vehicle[3], '|', vehicle[4])

    # find a unique ticket number
    c.execute("SELECT tno FROM tickets;")
    temp = c.fetchall()
    tnoUsed = []
    for x in temp:
        tnoUsed.append(x[0])

    tno = 1
    while True:
        if tno in tnoUsed:
            tno = tno + 1
        else:
            break

    regno = reg[0] # registration number of car we're ticketing

    # get a violation date, if None put todays date

    while True:
        try:
            vdate = input('Violation Date (YYYY-MM-DD): ')
            if vdate.lower() == "quit":
                return

            if vdate == '':
                vdate = time.strftime("%Y-%m-%d")

            datetime.datetime.strptime(vdate, '%Y-%m-%d')

            year, month, day = vdate.split('-')

            if datetime.datetime.strptime(vdate, '%Y-%m-%d') > datetime.datetime.strptime(time.strftime("%Y-%m-%d"), '%Y-%m-%d'):
                raise AssertionError('*** CANNOT BE IN THE FUTURE ***')

        except AssertionError as error:
            print(error)

        except ValueError:
            print("*** INVALID DATE FORMAT ***")

        else:
            break

    # get a violation text
    violation = input('Violation Text: ')
    if violation.lower() == "quit":
        return

    # get a fine amount that is greater than 0 and an integer
    while True:
        try:
            fine = input('Fine Amount: ')
            if fine.lower() == "quit":
                return
            test = int(fine)

            if int(fine) <= 0:
                raise AssertionError('*** FINE MUST BE GREATER THAN 0$ ***')

        except ValueError:
            print('*** FINE MUST BE AN INTEGER ***')
        
        except AssertionError as error:
            print(error)

        else:
            break

    ticket = (tno, regno, fine, violation, vdate)
    c.execute('INSERT INTO tickets (tno, regno, fine, violation, vdate) VALUES (?,?,?,?,?);', ticket) 
    connection.commit()

    print('\nTicket: (',tno,'|',regno,'|',fine,'|',violation,'|',vdate,') successfully added')
    garbage = input('Press Enter to Continue')



def o2 (c, connection):
    print('Please provide the following information to find a car owner: ')
    print('If you want to quit the operation, enter \"quit\" at any time')
  
    while True:
        try:
            make = input('Make of car: ')
            if make.lower() == "quit":
                return
            model = input('Model of car: ')
            if model.lower() == "quit":
                return
            year = input('Year of car: ')
            if year.lower() == "quit":
                return
            
            if year != '':
                test = int(year)

                if int(year) <= 0:
                    raise AssertionError('*** YEAR MUST BE GREATER THAN 0 ***')
            
            color = input('Color of car: ')
            if color.lower() == "quit":
                return
            plate = input('Plate of car: ')
            if plate.lower() == "quit":
                return

            if make != '': # user did not input anything
                make = 'v.make = \'' + make + '\' COLLATE NOCASE'
            if model != '':
                model = 'v.model = \'' + model + '\' COLLATE NOCASE'
            if year != '':
                year = 'v.year = ' + year
            if color != '':
                color = 'v.color = \'' + color + '\' COLLATE NOCASE'
            if plate != '':
                plate = 'r.plate = \'' + plate + '\' COLLATE NOCASE'

            data_string = ''
            a = [make, model, year, color, plate]

            for i in range(len(a)):
                if a[i] != '':
                    if (data_string != ''):
                        data_string = data_string + ' AND '
                    data_string = data_string + a[i]   

            if data_string == '':
                raise AssertionError('*** MUST ENTER AT LEAST ONE ATTRIBUTE ***')
        
        except ValueError:
            print('*** YEAR MUST BE AN INTEGER ***')

        except AssertionError as error:
            print(error)

        else:
            break
    print(data_string)
    
    # get all vehicles that match make, model, year, and color that have no plate
    c.execute("""SELECT DISTINCT v.vin, v.make, v.model, v.year, v.color, '*NO PLATE*' FROM vehicles v, registrations r WHERE %s
                EXCEPT
                SELECT DISTINCT v.vin, v.make, v.model, v.year, v.color, '*NO PLATE*' FROM vehicles v, registrations r
                WHERE v.vin = r.vin AND %s;""" %(data_string, data_string))
    cars = c.fetchall()

    # now get all vehicles that match make, model, year, color, and plate
    c.execute("""SELECT DISTINCT v.vin, v.make, v.model, v.year, v.color, r.plate FROM vehicles v, registrations r
                WHERE v.vin = r.vin AND %s;""" %(data_string))
    reg_cars = c.fetchall()

    for reg_car in reg_cars:
        cars.append(reg_car)

    if len(cars) >= 4:
        while True:
            try:
                clear_screen()
                print('Choose one of the following cars:')
                print('     '+'Make'.ljust(12, ' ') , ' ' , 'Model'.ljust(12, ' ') , ' ' , 'Year'.ljust(12, ' ') , ' ' , 'Color'.ljust(12, ' ') , ' ', 'Plate'.ljust(12, ' ') +'\n')

                for i in range (len(cars)):
                    print( (str(i+1)+'.').ljust(5, ' ') , cars[i][1].ljust(12, ' ') , '|' , cars[i][2].ljust(12, ' ') , '|' , str(cars[i][3]).ljust(12, ' ') , '|' , cars[i][4].ljust(12, ' ') , '|', cars[i][5].ljust(12, ' '))

                choice = input('Choice: ')
                if choice.lower() == "quit":
                    return

                if (int(choice) < 1) or (int(choice) > len(cars)):
                    raise AssertionError('*** CHOICE OUT OF RANGE ***')
            
            except AssertionError as error:
                print(error)

            else:
                cars = ( (cars[int(choice)-1]), )
                break

    # now cars is a tuple with 1-3 tuples
    # want the latest registration of each car

    result = []

    for car in cars:
        # first do cars that are registered
        if car[5] != '*NO PLATE*':
            c.execute('''SELECT v.make, v.model, v.year, v.color, r.plate, r.regdate, r.expiry, r.fname, r.lname
                        FROM vehicles v, registrations r
                        WHERE v.vin = ? and r.vin = v.vin
                        ORDER BY r.regdate DESC
                        limit 1;''', (car[0],))
            result.append(c.fetchone())
        #now do cars with no registration
        else:
            c.execute('''SELECT v.make, v.model, v.year, v.color, '*NO PLATE*', '*NO REG*', '*NO REG*', '*NO OWNER*', '*NO OWNER*'
                        FROM vehicles v
                        WHERE v.vin = ?''', (car[0],))
            result.append(c.fetchone())

    clear_screen()
    if (len(result) > 0):
        print('   '+'Make'.ljust(12, ' ') , ' ' , 'Model'.ljust(12, ' ') , ' ' , 'Year'.ljust(12, ' ') , ' ' , 'Color'.ljust(12, ' ') , ' ', 'Plate'.ljust(12, ' '), ' ' , 
                'Reg. Date'.ljust(12, ' ') , ' ' , 'Expiry Date'.ljust(12, ' ') , ' ' , 'First Name'.ljust(12, ' ') , ' ' , 'Last Name'.ljust(12, ' ') + '\n')
        for i in range (len(result)):
            print(str(i+1)+ '.' , result[i][0].ljust(12, ' ') , '|' , result[i][1].ljust(12, ' ') , '|' , str(result[i][2]).ljust(12, ' ') , '|' , result[i][3].ljust(12, ' ') , '|', result[i][4].ljust(12, ' ')
                    , '|' , result[i][5].ljust(12, ' ') , '|' , str(result[i][6]).ljust(12, ' ') , '|' , str(result[i][7]).ljust(12, ' ') , '|' , str(result[i][8]).ljust(12, ' '))
    else:
        print('*** NO MATCHES ***')
    
    garbage = input('Press Enter to Continue')


    