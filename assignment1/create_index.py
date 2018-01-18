import os
import sys
import sqlite3
import nltk


def create_table():
    try:   # super temporary schema
        c.execute('''CREATE TABLE inverted_index(
                        term TEXT,
                        doc INT,
                        pos INT)''')
    except:
        print("Table already exists, continuing...")


def parse_file(filename):
    try:
        infile = open(filename, 'r')
        content = infile.read()
        tokens = nltk.word_tokenize(content)
        infile.close()
    except:
        print("Error opening file.")


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

    for file in dirList:                   # start parsing directory
        if ".txt" in file:
            # print(directory+file)
            parse_file(directory+file)

if __name__ == '__main__':
    main()
