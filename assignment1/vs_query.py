import sqlite3
import sys
import math


def cosine(query, document, c):
    return


def tf_idf(term, document):
    return


def get_number_docs(c):
    c.execute('''
    SELECT COUNT(DISTINCT doc_id)
    FROM Posting;
    ''')

    num = c.fetchone()
    return num[0]


def main():
    try:
        index = sys.argv[1]
        conn = sqlite3.connect(index)
        c = conn.cursor()

        print_num = sys.argv[2]
        print_score = sys.argv[3]

        i = 4
        query = []
        while (i < len(sys.argv)):
             query.append(sys.argv[i])
             i+=1

    except:
        print("Error getting command line args.")
        sys.exit()

    scores = {}

    N = get_number_docs(c)       # get number of docs in index
    for doc in range(N):
        # magic happens here
        scores[doc] = cosine(query, doc, c)

    #printing happens here

    conn.close()


if __name__ == '__main__':
    main()
