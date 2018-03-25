# Use naives bayes algorithm to classify a set of test email data and accurately predict whether or not it is: 
# SPAM or HAM
# Train your program to correctly identify SPAM vs HAM using the training data and SPAM/HAM indexes, and use that + NB Algo. to:
# Accurately predict test email data and whether its SPAM / HAM.

import sys
import os, os.path
import re
from html.parser import HTMLParser
import codecs
import nltk
from nltk.stem import *
from nltk.stem.porter import *

class MLStripper(HTMLParser):
	def __init__(self):
		super().__init__()
		self.reset()
		self.fed = []
	   
	def handle_data(self, d):
		self.fed.append(d)
		
	def get_data(self):
		return ''.join(self.fed)
		
# all credit for the HTML Parser goes to: 
# https://stackoverflow.com/questions/11061058/using-htmlparser-in-python-3-2
# https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python

def main():
	classes = ("SPAM", "HAM",)
	num_classes = len(classes)
	print(num_classes)
	
	# find and open directory for both training and testing
	try:
		train_dir = sys.argv[1]                
		test_dir = sys.argv[2]
		
	# if two directories are not listed as command line arguments, exit
	except: 
		print("Missing or improper directories listed, exiting.")
		sys.exit()
		
	# finally : for checking if directories actually exist (LATER: FIXME)	
	
	# train_dir, test_dir are directories with all the documents required for both training() and testing
		
	print(train_dir, test_dir)
	
	num_docs = len(os.listdir(train_dir)) # os.listdir(dir_name) returns a list of every single file in dir_name directory

	#side snippet: 
	"""
	x = 0
	for name in os.listdir(train_dir):
		if not os.path.isfile(name):
			x+=1
	
	print(x)
	
	"""			
	# print(x) prints num_docs. This is because these are not "actual"" files, at least in python3 on mac OS
	
	num_docs-=1 # remove index file from doc_num 
	print(num_docs)
	
	# count num of docs in each class:
	
	train_idx_file = open((train_dir + '/' + 'index'), 'r') # index file
	train_idx_text = train_idx_file.read()
	
	#test_idx_file = open(test_dir + '/' + 'index')
	
	prior_prob = {"spam": 0, "ham": 0}
	
	num_docs_spam = len(re.findall("spam", train_idx_text))
	print(num_docs_spam)
	
	num_docs_ham = num_docs - num_docs_spam
	print(num_docs_ham)
	
	prior_prob["spam"] = num_docs_spam/num_docs
	prior_prob["ham"] = num_docs_ham/num_docs
	
	print(prior_prob)
	
	spam_files_l = re.findall("spam (.+)", train_idx_text)
	ham_files_l = re.findall("ham (.+)", train_idx_text)

	# Vocabulary accumulation 
	
	vocab = []
	spam_vocab = []
	ham_vocab = []
	
	directory = os.fsencode(train_dir)
	# TESTING HOW MANY FILES WERE PARSED: 
	#i = 0
	
	"""
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		if (filename != "index"): 
			with codecs.open((train_dir + '/' + filename), 'r', encoding='utf-8', errors='ignore') as email_file:  # e.g. read trec-397/data/train/inmail.1, .../inmail.2, and so on 
			# ignores all characters that are NOT utf-8 type
				email_f_text = email_file.read()
			
				# removing HTML from emails: 
				s = MLStripper()
				s.feed(email_f_text)
				text_no_HTML = s.get_data()
				vocab.append(text_no_HTML.split()) # split HTML-less text without spaces
				# TESTING how many files were parsed: 
				#i+=1 
	"""
	
	#SPAM CLASS
	for spam_file in spam_files_l:
		with codecs.open((train_dir + '/' + spam_file), 'r', encoding='utf-8', errors='ignore') as email_file:  # e.g. read trec-397/data/train/inmail.1, .../inmail.2, and so on 
		 #ignores all characters that are NOT utf-8 type
		 email_f_text = email_file.read()
		# removing HTML from emails: 
		s = MLStripper()
		s.feed(email_f_text)
		text_no_HTML = s.get_data()
		# spam_vocab.append(text_no_HTML.split()) # split HTML-less text without spaces (list of lists method)
		email_no_HTML = text_no_HTML.split() # split HTML-less text without spaces
		for word in email_no_HTML:
			spam_vocab.append(word) # (list of words method)
		
		
	#HAM CLASS	
	for ham_file in ham_files_l:
		with codecs.open((train_dir + '/' + ham_file), 'r', encoding='utf-8', errors='ignore') as email_file:  # e.g. read trec-397/data/train/inmail.1, .../inmail.2, and so on 
		 #ignores all characters that are NOT utf-8 type
		 email_f_text = email_file.read()
		# removing HTML from emails: 
		s = MLStripper()
		s.feed(email_f_text)
		text_no_HTML = s.get_data()
		# spam_vocab.append(text_no_HTML.split()) # split HTML-less text without spaces (list of lists method)
		email_no_HTML = text_no_HTML.split() # split HTML-less text without spaces
		for word in email_no_HTML:
			ham_vocab.append(word) # (list of words method)
		
	vocab = spam_vocab + ham_vocab
	
	print(len(vocab), len(spam_vocab), len(ham_vocab)) # each vocab (vocab, spam_vocab, ham_vocab) is a list of lists:
	# each element of the main list is a list of all words in the particular document it was for; if required, I can track which document correlates to which text.
	# Should I remove the puncuation from vocab?? (using parser from assignment1 ?)
	#print(ham_vocab)
	
	len_vocab = len(vocab)
	len_vocab_no_dupl = set(vocab)
	
	unique_vocab_size = len(len_vocab_no_dupl)
	print(unique_vocab_size)
	
	
	
	"""
	stemmed_tokens = []
	for content in ham_vocab:
		for word in content:
			#tokens = nltk.word_tokenize(word)
			stemmer = PorterStemmer()
			punctuation = [',', '.', ';', ':', "'", '"']
			
	
			if word in punctuation:                    # ignore punctuation
				continue

			word = stemmer.stem(word.lower())         # using Porter stemmer
			stemmed_tokens.append(word)

	print(len(stemmed_tokens)) 
	
	#tokens = nltk.word_tokenize(word) increases # of words... just reduces efficiency and time
	#e.g. 2162977 - 1708230 more words with this code with tokens = nltk.word_tokenize(word)
	# 1708230 - 1696138 less words with this code with no tokens = nltk.word_tokenize(word)
	(for ham_vocab)
	
	i=0
	for lis in ham_vocab:
		for word in lis:
			i+=1
	print(i)
	"""
	
	term_count_dic = {}
	
	# list of lists method term_count
	"""for specific_email in ham_vocab:
		for word in specific_email:
			for s_email in vocab:
				for w in s_email:
					if word == w:
						if word in term_count_dic:
							print(word, term_count_dic[word])
							term_count_dic[word]+=1
						else:
							term_count_dic[word] = 0
			
	print(term_count_dic) """
	
		
	# list of words method term_count
	ham_tc_dic = {}
	for word in ham_vocab:
		if word in ham_tc_dic:
			ham_tc_dic[word]+=1
			print(word, ham_tc_dic[word])
		else:
			ham_tc_dic[word] = 0
			print(word, ham_tc_dic[word])
		
	spam_tc_dic = {}
	for word in spam_vocab:
		if word in spam_tc_dic:
			spam_tc_dic[word]+=1
			print(word, spam_tc_dic[word])
		else:
			spam_tc_dic[word] = 0
			print(word, spam_tc_dic[word])		
			
	cond_prob_ham = {}
	cond_prob_spam = {}
	
	for word in ham_tc_dic:
		cond_prob_ham[word] = (ham_tc_dic[word] + 1)/((len_vocab)+unique_vocab_size)
	
	for word in spam_tc_dic:
		cond_prob_spam[word] = (spam_tc_dic[word] + 1)/((len_vocab)+unique_vocab_size)
	
	#print(cond_prob_ham)	
	
	
		
			
			
	# Multiline comment a test		
	"""
	test = open((train_dir + '/' + 'inmail.1'), 'r')
	testt = test.read()
	#print(testt)

	s = MLStripper()
	s.feed(testt)
	text_no_HTML = s.get_data()
	print(text_no_HTML)
	
	vocab.append(text_no_HTML.split())
	"""
	
	# TESTING how many files were parsed: 
	#print(i)
	
	#print(vocab)
		

		
	
	train_idx_file.close()
	
if __name__ == "__main__":
	main()