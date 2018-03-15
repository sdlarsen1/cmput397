import sqlite3
import sys
import os
import nltk
from nltk.stem import *
from nltk.stem.porter import *


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


def parse_file(filename):
    try:
        infile = open(filename, 'r')
        content = infile.read()

    except:
        print("Error opening/reading file:", filename)

    tokens = nltk.word_tokenize(content)
    stemmer = PorterStemmer()
    stemmed_tokens = []

    for token in tokens:
        if not token.isalpha():                    # ignore punctuation, non-alpha
            continue

        token = stemmer.stem(token.lower())         # using Porter stemmer
        stemmed_tokens.append(token)

    infile.close()
    return stemmed_tokens


def index_tokens(c, tokens, doc_id):
    seen = set()                            # keep track of seen tokens with a set
    for token in tokens:
        if token in seen:
            continue                        # skip if we already saw this one
        else:
            seen.add(token)

        token_id = in_index(token, c)       # check if token already indexed in Token table

        if token_id is None:                # if not in index, add it
            token_id = get_highest_id(c)

            if token_id is None:
                token_id = 0        # if this first instance in index, assign id=0
            else:
                token_id += 1       # else incrememnt highest id value

            c.execute('''
                INSERT INTO Token
                VALUES (?,?);''', (token, token_id,))

        # MLE calculated here
        tf = 0
        for x in tokens:
            if token == x:
                tf += 1

        mle = tf / len(tokens)     # MLE for a given token in document

        c.execute('''
            INSERT INTO MLE
            VALUES (?, ?, ?);''', (token_id, doc_id, mle,))


def in_index(token, c):
    c.execute('''
        SELECT token_id
        FROM Token
        WHERE token=?;''', (token,))

    token_id = c.fetchone()

    if token_id is not None:
        return token_id[0]

    return None


def get_highest_id(c):
    c.execute('''SELECT MAX(token_id) FROM Token;''')
    max_id = c.fetchone()

    return max_id[0]


def main():
    try:
        file_dir = sys.argv[1]                 # find and open directory
        file_list = os.listdir(file_dir)
        db_dir = sys.argv[2]
    except:
        print("Missing or improper directories listed, exiting.")
        sys.exit()

    print("Setting up database...")
    conn = sqlite3.connect(db_dir+'a2.db')      # connect to db
    c = conn.cursor()
    init_db(c)                                  # initialize the db

    print("Building index...")
    for file in file_list:
        if "nytimes" in file:
            # TODO parsing for NY Times
            return
        elif ".txt" in file:
            tokens = parse_file(file_dir+file)
            # print(tokens)
            filename = file.split('_')
            doc_id = filename[1]
            index_tokens(c, tokens, doc_id)

    print("Committing changes and closing connection.")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
