import sqlite3
import sys
import math


def cosine(query, document, c):
    return


def tf_idf(term, document):
    # use math.log10(x)
    return


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
    AND p.doc_id=?;
    ''', (doc_id,))

    tokens = []
    for token in c.fetchall():
        tokens.append(token[0])

    return tokens


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
    doc_tokens = []

    N = get_number_docs(c)       # get number of docs in index
    for doc_id in range(N):
        # magic happens here
        doc_tokens = get_doc_tokens(doc_id, c)
        print(doc_tokens)
        scores[doc_id] = cosine(query, doc_tokens, c)

    #printing happens here

    conn.close()


if __name__ == '__main__':
    main()
