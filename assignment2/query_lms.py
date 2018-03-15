import sqlite3
import sys
import nltk
from nltk.stem import *
from nltk.stem.porter import *


def get_mle(query, k, c):
    N = get_doc_ids(c)
    scores = {}

    for term in query:
        for doc in N+1:
            


def get_doc_ids(c):
    c.execute('''
    SELECT MAX(doc_id)
    FROM MLE;
    ''')

    N = c.fetchone()

    return N[0]


def main():
    try:
        db = sys.argv[1]
        k = sys.argv[2]

        i = 3
        query = []
        while i < len(sys.argv):
            query.append(sys.argv[i])           # get query terms
            i+=1

    except:
        print("Error with command line args, exiting.")
        sys.exit()

    # print(query)
    top_k = get_mle(query, k, c)
    print_top(top_k)




if __name__ == '__main__':
    main()
