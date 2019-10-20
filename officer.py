# for all the functionalities of the officer
import sqlite3
import time
import datetime


def clear_screen():
    print('----------------------------------------------------------------------------------------------')
    print('\n\n\n\n')

def o1(c, connection):
    while True:
        try:
            uRegno = input('Registration Number: ')
            c.execute ("SELECT * FROM registrations WHERE regno = ?;", (uRegno, ))
            reg = c.fetchall()

            if len(reg) == 0:
                raise AssertionError("*** Registration Number Not Found ***")
        
        except AssertionError as error:
            print(error)

        else:
            reg = reg[0]
            break
    
    c.execute("SELECT * FROM vehicles WHERE vin = ?;", (reg[4], ))
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

            if vdate == '':
                raise AssertionError("Today's Date")

            datetime.datetime.strptime(vdate, '%Y-%m-%d')

            year, month, day = vdate.split('-')

            if datetime.datetime.strptime(vdate, '%Y-%m-%d') > datetime.datetime.strptime(time.strftime("%Y-%m-%d"), '%Y-%m-%d'):
                raise IndexError()

        except AssertionError as error:
            vdate = time.strftime("%Y-%m-%d")
            break

        except ValueError:
            print("*** INVALID DATE FORMAT ***")

        except IndexError:
            print("*** CANNOT BE IN THE FUTURE ***")

        else:
            break

    # get a violation text
    violation = input('Violation Text: ')

    # get a fine amount that is greater than 0 and an integer
    while True:
        try:
            fine = input('Fine Amount: ')
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





    

    