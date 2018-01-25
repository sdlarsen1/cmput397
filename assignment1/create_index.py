import os
import sys
import sqlite3
import nltk
from nltk.stem import *
from nltk.stem.porter import *


def init_db(c):
    try:
        # cleanup
        c.execute("DROP TABLE IF EXISTS token;")
        c.execute("DROP TABLE IF EXISTS posting;")
        c.execute("DROP INDEX IF EXISTS token_idx;")

        # start creating tables
        c.execute('''
            CREATE TABLE Token (
            token TEXT,
            token_id INT,
            PRIMARY KEY(token_id)
            );''')

        c.execute('''
            CREATE TABLE Posting (
            token_id INT,
            doc_id INT,
            offset INT,
            FOREIGN KEY (token_id) REFERENCES Token(token_id)
            );''')

        c.execute('''
            CREATE UNIQUE INDEX Token_idx ON Token(token);''')

    except:
        print("Issue setting up database.")
        sys.exit()


def parse_file(filename):
    punctuation = [',', '.', ';', ':', "'", '"']

    try:
        infile = open(filename, 'r')
        content = infile.read()

    except:
        print("Error opening/reading file:", filename)

    tokens = nltk.word_tokenize(content)
    stemmer = PorterStemmer()
    stemmed_tokens = []

    for token in tokens:
        if token in punctuation:                    # ignore punctuation
            continue

        token = stemmer.stem(token.lower())         # using Porter stemmer
        stemmed_tokens.append(token)

    infile.close()
    return stemmed_tokens


def index_tokens(c, tokens, doc_id):
    return


def main():
    conn = sqlite3.connect("a1.db")     # open / create db
    c = conn.cursor()                   # set up cursor

    try:
        directory = sys.argv[1]                  # find and open directory
        file_list = os.listdir(directory)

    except:
        print("Must specify an existing directory:", directory)
        sys.exit()

    init_db(c)                               # initialize the db

    for file in file_list:                   # start parsing directory
        if ".txt" in file:
            tokens = parse_file(directory+file)
            # print(tokens)
            filename = file.split('_')          # filename: doc_#_xyz.txt
            doc_id = filename[1]
            index_tokens(c, tokens, doc_id)     # index the file


if __name__ == '__main__':
    main()
