import os
import sys
import sqlite3


def create_table():
    try:   # super temporary schema
        c.execute('''CREATE TABLE inverted_index(
                        term TEXT,
                        doc INT,
                        pos INT)''')
    except:
        print("Table already exists, continuing...")

def main():
    conn = sqlite3.connect("a1.db")  # open / create db
    c = conn.cursor()

    try:
        directory = sys.argv[1]                  # find and open directory
        dirList = os.listdir(directory)

    except:
        print("Must specify an existing directory.")
        sys.exit()

    create_table()                         # create the index table

    for file in dirList:
        if ".txt" not in file:
            print(file)

if __name__ == '__main__':
    main()
