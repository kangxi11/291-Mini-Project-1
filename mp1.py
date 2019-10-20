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

def officer_menu(user):
    print('Hello Officer', user[4])
    print('Please choose a task: ')

    print('1. Issue a Ticket')
    print('2. Find a Car Owner')
    choice = input('Choice: ')

    clear_screen()

    if choice == '1':
        o1(c, connection)

def agent_menu(user):
    print('You have successfully logged')
    print(user)
    

def login():
    global connection, c

    clear_screen()

    print('Please enter your UID and PWD')


    uid = None
    password = None

    while True:
        try:
            input_uid = input('UID: ')
            input_pass = getpass.getpass('Password: ')
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
        agent(user)
    if str(user[2]) == 'o':
        officer_menu(user)
        
    
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
