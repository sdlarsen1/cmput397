import sqlite3
import os
import sys
import re

def optimize_query(query):
	query_opt = query.split()
	valid_terms = ["AND", "OR", "NOT", ]
	print(query_opt)
	boolean_list = []
	phrase_list = []

	
	if len(query_opt) == 1:
		# query is only 1 word
		dum = 0
	
		# query cannot begin with capital or, not, and
	else:
		for word in valid_terms:
			if (query_opt[0] == word or query_opt[-1] == word): # if first or last word is a query term.
				print("Please enter a valid boolean entry. The first or last word cannot be a boolean phrase")
				return -1
		#else:
		for i in range(1, len(query_opt)-2):
			if query_opt[i] in valid_terms:
				if (query_opt[i-i] in valid_terms or query_opt[i+1] in valid_terms):
					print("Cannot have 2 consecutive boolean entries")
					return -1
		# this loop needs modifications, does not account for everything.
				
	# code to be added for validating other boolean entries:
		#result = re.search(r'.()' query)
		
	
	for word in query_opt:
		if word in valid_terms: 
			boolean_list.append(word)
		else:
			phrase_list.append(word)
			
	print(boolean_list, "\n", phrase_list)

	return (boolean_list, phrase_list)
	
	
def boolean_search(data_tup, conn):
	# must account for phrase queries in boolean search...	
	c = conn.cursor()
	
	boolean = data_tup[0]
	word = data_tup[1]

		#for i in range(boolean):
		
	query = "SELECT p1.doc_id FROM posting p1, posting p2, token t1, token t2 WHERE t1.token = ? AND" + " t2.token = ?"  + " AND p1.token_id = t1.token_id AND p2.token_id = t2.token_id AND p1.doc_id = p2.doc_id"
		
	c.execute(query, (word[0], word[1]))
	rows = c.fetchall()
	
	print(rows)
	print(query)
	
	for each in rows:
		print("DocID:", each[0])
			
	

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
	
	query = sys.argv[2]
	print(query)	
	
	data = optimize_query(query)
	boolean_search(data, conn)
		
	conn.close()



if __name__ == '__main__':
	main()
