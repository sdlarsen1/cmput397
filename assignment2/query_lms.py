import sqlite3
import sys
import nltk
from nltk.stem import *
from nltk.stem.porter import *


def main():
    # print(len(sys.argv))
    try:
        db = sys.argv[1]
        K = sys.argv[2]

        i = 3
        query = []
        while i < len(sys.argv):
            query.append(sys.argv[i])
            i+=1
    except:
        print("Error with command line args, exiting.")
        sys.exit()

    # print(query)




if __name__ == '__main__':
    main()
