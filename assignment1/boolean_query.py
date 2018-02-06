def main():
    conn = sqlite3.connect("a1.db")     # open / create db
    c = conn.cursor()                   # set up cursor

    try:
        directory = sys.argv[1]                  # find and open directory
        file_list = os.listdir(directory)

    except:
        print("Must specify an existing directory:", directory)
        sys.exit()
		
		# boolean queries handling here

    conn.close()



if __name__ == '__main__':
    main()
