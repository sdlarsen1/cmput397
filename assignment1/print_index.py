import sqlite3
import sys
import os

def get_num_tokens(c):
    c.execute('''
    SELECT COUNT(token_id)
    FROM Token;
    ''')

    N = c.fetchone()
    return N[0]


def get_posting(token_id, c):
    c.execute('''
    SELECT t.token, p.doc_id, p.offset
    FROM token t, posting p
    WHERE t.token_id = p.token_id
    AND t.token_id = ?;
    ''', (token_id,))

    posting = c.fetchall()
    return posting


def print_posting(posting):
    index = {}
    term = posting[0][0]
    index[term] = {}
    for tuple in posting:
        try:
            index[term][tuple[1]].append(str(tuple[2]))
        except:
            index[term][tuple[1]] = [str(tuple[2])]

    print(term, "\t", end="")
    for doc_id in index[term]:
        print(str(doc_id)+":"+",".join(index[term][doc_id])+"; ", end="")

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
        N = get_num_tokens(c)               # number of tokens
    except:
        print("Invalid DB file or no index was created.")
        choice = input("Would you like to remove the invalid DB? (y/n) ")
        if choice == 'y':
            os.system("rm "+db)
            print("DB removed")
        sys.exit()

    for token_id in range(N):
        posting = get_posting(token_id, c)
        print_posting(posting)

    conn.close()


if __name__ == '__main__':
    main()
