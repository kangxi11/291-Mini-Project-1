import sqlite3
import time

connection = None
c = None # cursor

def main():
    database_name = input('Database name: ')
    
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    

    print('success')

main()