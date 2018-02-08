import sqlite3
import sys
import math
import nltk
from nltk.stem import *
from nltk.stem.porter import *


def cosine(query, doc_tokens, N, c):
    sum_tf = 0
    sum_df = 0
    for word in query:
        tf = get_term_frequency(word, doc_tokens)
        df = get_doc_frequency(word, c)

    return


def tf_idf(tf, df, N):
    # use math.log10(x)
    tf_idf = (1 + math.log10(tf)) * math.log10(N / df)
    return tf_idf


def get_number_docs(c):
    c.execute('''
    SELECT COUNT(DISTINCT doc_id)
    FROM Posting;
    ''')

    num = c.fetchone()
    return num[0]


def get_doc_tokens(doc_id, c):
    c.execute('''
    SELECT t.token
    FROM token t, posting p
    WHERE t.token_id = p.token_id
    AND p.doc_id = ?;
    ''', (doc_id,))

    tokens = []
    for token in c.fetchall():
        tokens.append(token[0])

    return tokens


def get_doc_frequency(term, c):
    term = PorterStemmer().stem(term.lower())  # compare stemmed tokens

    c.execute('''
    SELECT SUM(Count)
    FROM (SELECT COUNT(p.token_id) AS Count
    FROM Token t, Posting p
    WHERE t.token_id = p.token_id
    AND t.token = ?
    GROUP BY (p.doc_id));
    ''', (term,))

    freq = c.fetchone()
    return freq[0]


def get_term_frequency(term, doc_tokens):
    term = PorterStemmer().stem(term.lower())  # compare stemmed tokens

    count = 0
    for token in doc_tokens:
        if term == token:
            count += 1

    return count


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

    scores = {}                  # dict of docs and their score
    magnitudes = {}              # dict of magnitudes of each vector
    doc_tokens = []

    N = get_number_docs(c)       # get number of docs in index
    for doc_id in range(N):
        # magic happens here
        doc_tokens = get_doc_tokens(doc_id, c)    # retrieve doc tokens as list
        print(doc_tokens)
        magnitudes[doc_id] = len(doc_tokens)

        scores[doc_id] = cosine(query, doc_tokens, N, c)

    #printing happens here

    conn.close()


if __name__ == '__main__':
    main()
