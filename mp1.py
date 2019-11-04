import sqlite3
import time
import sys
import getpass

from agent import *
from officer import *

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

def login():
    global connection, c

    clear_screen()

    print('Please enter your UID and PWD')
    print('Enter "exit" to exit')


    uid = None
    password = None

    while True:
        try:
            input_uid = input('UID: ')
            if input_uid == 'exit':
                sys.exit()
            input_pass = getpass.getpass('Password: ')
            if input_pass == 'exit':
                sys.exit()
            c.execute ("SELECT * FROM users WHERE uid = :uid COLLATE NOCASE and pwd = :pwd;", {"uid":input_uid, "pwd":input_pass})
            user = c.fetchall()

            if len(user) == 0:
                raise AssertionError("*** Invalid Credentials ***")
        
        except AssertionError as error:
            print(error)

        else:
            user = user[0]
            break

    clear_screen()

    if str(user[2]) == 'a':
        agent_menu(user, c, connection)
    if str(user[2]) == 'o':
        officer_menu(user, c, connection)
        
    
def homescreen():
    clear_screen()
    print('Welcome to Service Alberta')
    print('Please select an option by inputting a number:')
    print('1 - Login')
    print('2 - Exit')
    user_choice = input('Choice: ')

    if user_choice == '1' or user_choice == 1:
        login()
    if user_choice == '2' or user_choice == 2:
        clear_screen()
        print('Service Alberta is now exiting')
        sys.exit()

def main():
    global connection, c

    connect(sys.argv[1]) # connect the database
    
    leave = False
    
    while leave == False:
        homescreen()

main()
