import os
import sys
import sqlite3

conn = sqlite3.connect("test.db")  # open / create db

try:
    directory = sys.argv[1]                  # find and open directory
    dirList = os.listdir(directory)
    for file in dirList:
        if ".txt" not in file:
            print(file)
except:
    print("Must specify an existing directory.")
    sys.exit()
