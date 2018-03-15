import sqlite3
import sys
import os


def get_num_docs(c):
    c.execute('''
    SELECT MAX(doc_id)
    FROM MLE;
    ''')

    N = c.fetchone()
    return N[0]


def get_posting(doc_id, c):
    c.execute('''
    SELECT m.doc_id, t.token, m.mle
    FROM Token t, MLE m
    WHERE t.token_id = m.token_id
    AND m.doc_id = ?;
    ''', (doc_id,))

    posting = c.fetchall()
    return posting


def print_posting(posting):
    index = {}
    doc = posting[0][0]
    index[doc] = {}
    for tuple in posting:
        try:
            index[doc][tuple[1]].append(str(tuple[2]))
        except:
            index[doc][tuple[1]] = [str(tuple[2])]

    print(doc, "\t", end="")
    for term in index[doc]:
        print(term+":%.5f; " % float(index[doc][term][0]), end="")
    print()


def main():
    try:
        db = sys.argv[1]
        conn = sqlite3.connect(db)          # open / create db
        c = conn.cursor()                   # set up cursor

    except:
        print("Error connecting to DB:", db)
        sys.exit()

    try:
        N = get_num_docs(c)               # number of tokens
    except:
        print("Invalid DB file or no index was created.")
        choice = input("Would you like to remove the invalid DB? (y/n) ")
        if choice == 'y':
            os.system("rm "+db)
            print("DB removed")
        sys.exit()

    for doc_id in range(N+1):
        posting = get_posting(doc_id, c)
        print_posting(posting)

    conn.close()


if __name__ == '__main__':
    main()
