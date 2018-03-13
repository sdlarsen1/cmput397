import sqlite3
import sys
import os
import re   # use regex to remove non-alphanumeric values from tokens before stem?


def init_db(c):
    try:
        # cleanup
        c.execute("DROP TABLE IF EXISTS Token;")
        c.execute("DROP TABLE IF EXISTS MLE;")
        c.execute("DROP INDEX IF EXISTS Token_idx;")

        # start creating tables
        c.execute('''
            CREATE TABLE Token (
            token TEXT,
            token_id INT,
            PRIMARY KEY(token_id)
            );''')

        c.execute('''
            CREATE TABLE MLE (
            token_id INT,
            doc_id INT,
            MLE FLOAT,
            FOREIGN KEY (token_id) REFERENCES Token(token_id)
            );''')

        c.execute('''
            CREATE UNIQUE INDEX Token_idx ON Token(token);''')

    except:
        print("Issue setting up database, exiting.")
        sys.exit()


def main():
    try:
        file_dir = sys.argv[1]                 # find and open directory
        file_list = os.listdir(file_dir)
        db_dir = sys.argv[2]
    except:
        print("Missing or improper directories listed, exiting.")
        sys.exit()

    print("Setting up databse.")
    conn = sqlite3.connect(db_dir+'a2.db')      # connect to db
    c = conn.cursor()
    init_db(c)                                  # initialize the db





if __name__ == '__main__':
    main()
