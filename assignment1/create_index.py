import os
import sys
import sqlite3
import nltk


def init_db(c):
    try:
        # cleanup
        c.execute("DROP TABLE IF EXISTS token;")
        c.execute("DROP TABLE IF EXISTS posting;")
        c.execute("DROP INDEX IF EXISTS token_idx;")

        # start creating tables
        c.execute('''
            CREATE TABLE token (
            token TEXT,
            token_id INT,
            PRIMARY KEY(token_id)
            );''')

        c.execute('''
            CREATE TABLE posting (
            token_id INT,
            doc_id INT,
            offset INT,
            FOREIGN KEY (token_id) REFERENCES token(token_id)
            );''')

        c.execute('''
            CREATE INDEX token_idx ON token(token);''')

    except:
        print("Issue setting up database.")
        sys.exit()


def parse_file(filename):
    try:
        infile = open(filename, 'r')
        content = infile.read()
        tokens = nltk.word_tokenize(content)
        # do other stuff here
        infile.close()

    except:
        print("Error opening/parsing file:", filename)


def main():
    conn = sqlite3.connect("a1.db")  # open / create db
    c = conn.cursor()                # set up cursor

    try:
        directory = sys.argv[1]                  # find and open directory
        file_list = os.listdir(directory)

    except:
        print("Must specify an existing directory:", directory)
        sys.exit()

    init_db(c)                                # initialize the db

    for file in file_list:                   # start parsing directory
        if ".txt" in file:
            # print(directory+file)
            parse_file(directory+file)

if __name__ == '__main__':
    main()
