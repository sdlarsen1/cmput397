import sqlite3
import os
import sys
import re
import sqlite3
import nltk
from nltk.stem import *
from nltk.stem.porter import *
nltk.download('punkt')


def optimize_query(query):
	query_opt = query.split()
	valid_terms = ["AND", "OR", "NOT", ]
	#print(query_opt)
	boolean_list = []
	phrase_list = []

	stemmed_words = []

	stemmer = PorterStemmer()
	punctuation = [',', '.', ';', ':', "'", '"']
	
	if len(query_opt) == 1:
		# query is only 1 word
		if query_opt[0] in punctuation:                  # ignore punctuation
			print("Single punct. not allowed. Please enter a valid boolean phrase.")
			return (None, None, -1) #error return code
			
		term = stemmer.stem(query_opt[0].lower())
		stemmed_words.append(term)
		return (None, stemmed_words, 1) # 1 as last item in Tuple means ONE entry
	
		# query cannot begin with capital or, not, and
	else:
		for word in valid_terms:
			if (query_opt[0] == word or query_opt[-1] == word): # if first or last word is a query term.
				print("Please enter a valid boolean entry. The first or last word cannot be a boolean phrase")
				return (None, None, -1) #error return code 
		#else:
		for i in range(1, len(query_opt)-2):
			if query_opt[i] in valid_terms:
				if (query_opt[i-i] in valid_terms or query_opt[i+1] in valid_terms):
					print("Cannot have 2 consecutive boolean entries")
					return (None, None, -1) #error return code
					
		# this loop needs modifications, does not account for everything. FIXME
				
	# code to be added for validating other boolean entries: FIXME
		#result = re.search(r'.()' query)
		
	for word in query_opt:
		if word in valid_terms: 
			boolean_list.append(word)
		else:
			phrase_list.append(word)
			
	#print(boolean_list, "\n", phrase_list)

	for term in phrase_list:
		if term in punctuation:                    # ignore punctuation
			continue
		term = stemmer.stem(term.lower())
		stemmed_words.append(term)
		
	print(boolean_list, stemmed_words)
	return (boolean_list, stemmed_words, 2) # 2 as last item in Tuple means more than one entry
	
	
def boolean_search(data_tup, conn):
	# must account for phrase queries in boolean search...	
	c = conn.cursor()
	print (data_tup)
	
	if data_tup[2] == -1:
		return -1 #failure
	
	if data_tup[2] == 1:
		query = "SELECT distinct p1.doc_id FROM posting p1, token t1 WHERE t1.token = ? AND p1.token_id = t1.token_id;" 
		c.execute(query, (data_tup[1][0],) ) 
		rows = c.fetchall()
		print(rows)
		print(query)
	
		for each in rows:
			print("DocID:", each[0])
		return 0 #success
			
	boolean = data_tup[0]
	word = data_tup[1]
		
	for bool_entry in boolean:
		if bool_entry == 'AND' or bool_entry == 'OR':
			#query = "SELECT distinct p1.doc_id FROM posting p1, posting p2, token t1, token t2 WHERE t1.token = ? " + bool_entry + " t2.token = ?"  + " AND p1.token_id = t1.token_id AND p2.token_id = t2.token_id AND p1.doc_id = p2.doc_id;" 
			#c.execute(query, (word[0], word[1]))
			query = "SELECT * FROM posting p1"
			c.execute(query)
			conn.commit()
			
			print(word)
			rows = c.fetchall()
			print(rows)
			print(query)
	
			for each in rows:
				print("DocID:", each[0])
			return 0 #success
			
		#else: #need to implement NOT here
		#	query = "SELECT distinct p1.doc_id FROM posting p1, token t1 WHERE t1.token <> ? "  + " AND p1.token_id = t1.token_id;"
		#	c.execute(query, (word[2]), )
	
	

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
	#print(query)	
	
	data = optimize_query(query)
	boolean_search(data, conn)
		
	conn.close()



if __name__ == '__main__':
	main()
