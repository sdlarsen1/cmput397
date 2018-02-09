import sqlite3
import sys
import math
import heapq
import nltk
from nltk.stem import *
from nltk.stem.porter import *


def cosine(query, scores, N, c):

    magnitude = {}             # used to normalize the scores

    for word in query:
        # print(word)
        # print("-------"+word+"--------")
        df_d = df_q = get_doc_frequency(word, c)      # df_q and df_d are the same, but for clarity
        tf_q = get_term_frequency_query(word, query)  # w.r.t. the query
        w_q = tf_idf(tf_q, df_q, N)                   # tf_idf of word in query

        valid_docs = get_valid_docs(word, c)      # narrow down the docs we need to look at
        # print(valid_docs)

        for doc_id in valid_docs:
            # print("-----"+str(doc_id)+"-----")

            doc_tokens = get_doc_tokens(doc_id, c)
            # print(doc_tokens)

            # magnitude[doc_id] = len(doc_tokens)

            tf_d = get_term_frequency(word, doc_tokens)   # w.r.t. the document

            w_d = tf_idf(tf_d, df_d, N)                   # tf_idf of word in doc

            try:
                scores[doc_id] += w_d * w_q
            except:
                scores[doc_id] = w_d * w_q

    # normalization step
    for word in query:
        # print(word)
        for key in scores.keys():
            # print(token, key)
            tf_token = get_term_frequency(word, get_doc_tokens(key, c))
            df_token = get_doc_frequency(word, c)

            try:
                magnitude[key] += tf_idf(tf_token, df_token, N)**2
            except:
                magnitude[key] = tf_idf(tf_token, df_token, N)**2


    # normalize scores
    for key in scores.keys():
        scores[key] /= math.sqrt(magnitude[key])
        # scores[key] /= magnitude[key]

    return scores


def tf_idf(tf, df, N):
    # use math.log10(x)
    if (tf > 0) and (df > 0):
        tf_idf = (1 + math.log10(tf)) * math.log10(N / df)
    else:
        tf_idf = 0

    # print("tf =", tf, "df =", df, "tf_idf =", tf_idf)
    return tf_idf


def get_number_docs(c):                 # returns number of docs in corpus
    c.execute('''
    SELECT COUNT(DISTINCT doc_id)
    FROM Posting;
    ''')

    num = c.fetchone()
    return num[0]


def get_all_tokens(c):                  # returns all tokens in posting list
    c.execute('''
    SELECT token
    FROM Token;
    ''')

    tokens = []
    for token in c.fetchall():
        tokens.append(token[0])

    return tokens


def get_doc_tokens(doc_id, c):          # returns all tokens in a specific doc
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


def get_doc_frequency(term, c):         # returns doc freq. of a term
    term = PorterStemmer().stem(term.lower())  # compare stemmed tokens

    c.execute('''
    SELECT SUM(Count)
    FROM (SELECT COUNT(DISTINCT p.doc_id) AS Count
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


def get_term_frequency(term, doc_tokens):   # returns term frequency
    term = PorterStemmer().stem(term.lower())  # compare stemmed tokens

    count = 0
    for token in doc_tokens:
        if term == token:
            count += 1

    return count


def get_term_frequency_query(term, query):  # returns term frequency within a query
    count = 0
    for word in query:
        if term == word:
            count += 1

    return count


def get_valid_docs(term, c):            # returns only docs the term is in
    term = PorterStemmer().stem(term.lower())  # compare stemmed tokens
    docs = []

    c.execute('''
    SELECT DISTINCT p.doc_id
    FROM posting p, token t
    WHERE t.token_id = p.token_id
    AND t.token = ?;
    ''', (term,))

    for doc_id in c.fetchall():
        docs.append(doc_id[0])

    return docs


def print_k_highest(scores, k, print_scores):
    largest = heapq.nlargest(k, scores, key=scores.get)

    for i in range(k):
        try:
            print(largest[i], "\t", end="")
            if print_scores == 'y':
                print(scores[largest[i]])
            else:
                print()
        except:
            continue        # in case k is larger than N
    return


def main():
    try:
        index = sys.argv[1]
        conn = sqlite3.connect(index)
        c = conn.cursor()

        k = int(sys.argv[2])
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

    #printing happens here
    print_k_highest(scores, k, print_score)

    conn.close()


if __name__ == '__main__':
    main()
