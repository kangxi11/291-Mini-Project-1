import sqlite3
import time
import sys

connection = None
c = None # cursor

def connect(path):
    global connection, c

    connection = sqlite3.connect(path)
    c = connection.cursor()
    c.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

def clear_screen():
    print('----------------------------------------------------------------------------------------------')
    print('\n\n\n\n')

def agent():
    print('You have successfully logged')

# def officer():
    

def login():
    global connection, c

    clear_screen()

    print('Please enter your UID and PWD')


    uid = None
    password = None

    while True:
        try:
            input_uid = input('UID: ')
            input_pass = input('PWD: ')
            c.execute ("SELECT uid, pwd FROM users WHERE uid = :uid;", {"uid":input_uid})
            users = c.fetchone()
           
            if users == None:
                raise AssertionError('\nInvalid UID')
            elif (input_pass != str(users[1])):
                raise AssertionError('\nIncorrect Password')
        
        except AssertionError as error:
            print(error)

        else:
            break
    agent()
        
    
def homescreen():
    clear_screen()
    print('Welcome to Service Alberta')
    print('Please select an option by inputting a number:')
    print('1 - Login')
    print('2 - Logout')
    print('3 - Exit')
    user_choice = input('Choice: ')

    if user_choice == '1':
        login()
    if user_choice == '3':
        clear_screen()
        print('Service Alberta is now exiting')
        time.sleep(1)
        sys.exit()


def main():
    global connection, c

    #database_name = input('Database name: ')

    connect("mp1.db") # connect the database
    homescreen()

main()