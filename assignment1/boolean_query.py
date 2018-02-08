import sqlite3
import os
import sys
import re

def optimize_query(query):
	query_opt = query.split()
	valid_terms = ["AND", "OR", "NOT", ]
	print(query_opt)
	
	if len(query_opt) == 1:
		# query is only 1 word
		dum = 0
	
		# query cannot begin with capital or, not, and
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
			X = 0
	
# must account for phrase queries in boolean search...	


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
	
	optimize_query(query)
		
	conn.close()



if __name__ == '__main__':
	main()
