import sqlite3
import sys
import heapq
import nltk
from nltk.stem import *
from nltk.stem.porter import *


def get_scores(query, k, c):
    N = get_num_docs(c)
    scores = {}

    print("Gathering scores...")
    for doc_id in range(N+1):                         # doc_ids start at 0
        for term in query:
            tf, mle = get_tf_mle(doc_id, term, c)     # get the tf and mle of term
            if tf > 0:
                try:
                    scores[doc_id] *= mle
                except:
                    scores[doc_id] = mle

    return scores


def get_num_docs(c):
    c.execute('''
    SELECT MAX(doc_id)
    FROM MLE;
    ''')

    N = c.fetchone()

    return N[0]


def get_tf_mle(doc_id, term, c):
    token = PorterStemmer().stem(term.lower())      # stem the term

    c.execute('''
    SELECT m.tf, m.mle
    FROM MLE m, Token t
    WHERE t.token_id = m.token_id
        AND m.doc_id = ?
        AND t.token = ?;
    ''', (doc_id, token,))

    result = c.fetchone()

    if result is None:                 # in case term is not in doc
        return 0,1

    return result[0], result[1]



def print_top_k(scores, k):
    largest = heapq.nlargest(k, scores, key=scores.get)     # sort scores

    print(" Rank | Doc | Score ")
    for i in range(k):
        try:
            print(' ', i+1, '\t', largest[i], "\t%.5f" %scores[largest[i]])
        except:
            continue        # in case k is larger than N
    return


def main():
    try:
        db = sys.argv[1]
        k = int(sys.argv[2])

        i = 3
        query = []
        while i < len(sys.argv):
            query.append(sys.argv[i])           # get query terms
            i+=1

    except:
        print("Error with command line args, exiting.")
        sys.exit()

    conn = sqlite3.connect(db)
    c = conn.cursor()

    scores = get_scores(query, k, c)
    print_top_k(scores, k)

    conn.close()


if __name__ == '__main__':
    main()
