import sqlite3
import sys
import math
import nltk
from nltk.stem import *
from nltk.stem.porter import *


def cosine(query, scores, N, c):

    length = {}             # dict of lengths for each vector

    for word in query:
        print("-------"+word+"--------")
        df_d = df_q = get_doc_frequency(word, c)      # df_q and df_d are the same, but for clarity
        tf_q = get_term_frequency_query(word, query)        # w.r.t. the query
        w_q = tf_idf(tf_q, df_q, N)

        for doc_id in range(N):
            print("-----"+str(doc_id)+"-----")

            doc_tokens = get_doc_tokens(doc_id, c)
            print(doc_tokens)

            length[doc_id] = len(doc_tokens)

            tf_d = get_term_frequency(word, doc_tokens)   # w.r.t. the document

            w_d = tf_idf(tf_d, df_d, N)

            try:
                scores[doc_id] += w_d * w_q
            except:
                scores[doc_id] = w_d * w_q

    for doc_id in range(N):
        scores[doc_id] /= length[doc_id]

    return scores


def tf_idf(tf, df, N):
    # use math.log10(x)
    print("tf =", tf, "df =", df)
    if (tf > 0) and (df > 0):
        tf_idf = (1 + math.log10(tf)) * math.log10(N / df)
    else:
        tf_idf = 0

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
    if freq[0] is None:
        return 0
    else:
        return freq[0]


def get_term_frequency(term, doc_tokens):
    term = PorterStemmer().stem(term.lower())  # compare stemmed tokens

    count = 0
    for token in doc_tokens:
        if term == token:
            count += 1

    return count


def get_term_frequency_query(term, query):
    count = 0
    for word in query:
        if term == word:
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
    doc_tokens = []

    N = get_number_docs(c)       # get number of docs in index
    scores = cosine(query, scores, N, c)
    print(scores)
    # for doc_id in range(N):
    #     # magic happens here
    #     doc_tokens = get_doc_tokens(doc_id, c)    # retrieve doc tokens as list
    #     print(doc_tokens)
    #     magnitudes[doc_id] = len(doc_tokens)
    #
    #     scores = cosine(query, scores, N, c)

    #printing happens here

    conn.close()


if __name__ == '__main__':
    main()
