import sqlite3
import sys

def main():
    conn = sqlite3.connect("a1.db")     # open / create db
    c = conn.cursor()                   # set up cursor

    try:
        index = sys.argv[1]                  # open index
        conn = sqlite3.connect(index)
        c = conn.cursor()

        num_docs = sys.argv[2]
        score = sys.argv[3]

        i = 4
        terms = []
        while (i < len(sys.argv)):
             terms.append(sys.argv[i])
             i+=1

    except:
        print("Error getting command line args.")
        sys.exit()

    doc = 0
    while (doc < num_docs):
        # do stuff


    conn.close()


if __name__ == '__main__':
    main()
