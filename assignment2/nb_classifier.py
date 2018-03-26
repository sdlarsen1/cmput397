# Use naives bayes algorithm to classify a set of test email data and accurately predict whether or not it is: 
# SPAM or HAM
# Train your program to correctly identify SPAM vs HAM using the training data and SPAM/HAM indexes, and use that + NB Algo. to:
# Accurately predict test email data and whether its SPAM / HAM.

import sys
import os, os.path
import re
from html.parser import HTMLParser
import codecs
import math

# all credit for the HTML Parser goes to: 
# https://stackoverflow.com/questions/11061058/using-htmlparser-in-python-3-2
# https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python

class MLStripper(HTMLParser):
	def __init__(self):
		super().__init__()
		self.reset()
		self.fed = []
	   
	def handle_data(self, d):
		self.fed.append(d)
		
	def get_data(self):
		return ''.join(self.fed)

def main():
	classes = ("SPAM", "HAM",)
	num_classes = len(classes)
	#print(num_classes)
	
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
		
	#print(train_dir, test_dir)
	
	num_docs = len(os.listdir(train_dir)) 
	#os.listdir(dir_name) returns a list of every single file in dir_name directory

	#side snippet (ignore):
	"""
	x = 0
	for name in os.listdir(train_dir):
		if not os.path.isfile(name):
			x+=1
	
	print(x)
	
	# print(x) prints num_docs. This is because these are not "actual"" files, at least in python3 on mac OS
	"""			
	
	num_docs-=1 # remove index file from num_of_docs
	#print(num_docs)
	
	# count num of docs in each class:
	
	train_idx_file = open((train_dir + '/' + 'index'), 'r') # index file
	train_idx_text = train_idx_file.read()
	
	#test_idx_file = open(test_dir + '/' + 'index')
	
	############################ NB TRAINING #########################
	
	#Calculating prior probabilities:
	prior_prob = {"spam": 0, "ham": 0}
	
	
	num_docs_spam = len(re.findall("spam", train_idx_text))
	#print(num_docs_spam)
	
	num_docs_ham = num_docs - num_docs_spam
	#print(num_docs_ham)
	
	prior_prob["spam"] = num_docs_spam/num_docs
	prior_prob["ham"] = num_docs_ham/num_docs
	
	#print(prior_prob)
	
	#List of spam files, ham files and all files in the train directory
	spam_files_l = re.findall("spam (.+)", train_idx_text)
	ham_files_l = re.findall("ham (.+)", train_idx_text)
	
	train_all_files_l = re.findall("(spam|ham) (.+)", train_idx_text)
	#print(train_all_files_l)

	# Vocabulary accumulation
	
	vocab = []
	spam_vocab = []
	ham_vocab = []
	
	
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
	
	#print(len(vocab), len(spam_vocab), len(ham_vocab)) 
	# each vocab (vocab, spam_vocab, ham_vocab) is a list of words for vocab, spam, and ham respectively
	
	len_vocab = len(vocab)
	vocab_no_dupl = set(vocab) # set() removes duplicates from the list of words in vocab
	
	unique_vocab_size = len(vocab_no_dupl) # size of unique_vocab 
	#print(unique_vocab_size)
		
	# list of words method term_count
	ham_tc_dic = {}
	
	for word in ham_vocab:
		if word in ham_tc_dic:
			ham_tc_dic[word]+=1
			#print(word, ham_tc_dic[word])
		else:
			ham_tc_dic[word] = 1
			#print(word, ham_tc_dic[word])
		
	spam_tc_dic = {}
	for word in spam_vocab:
		if word in spam_tc_dic:
			spam_tc_dic[word]+=1
			#print(word, spam_tc_dic[word])
		else:
			spam_tc_dic[word] = 1
			#print(word, spam_tc_dic[word])		
			
	cond_prob_ham = {}
	cond_prob_spam = {}
	
	#Computing denominators in conditional probability formula
	#Essentially the total length of all tokens of spam/ham vocab lists + the number of unique terms in the vocab
	
	ham_denom = 0
	for word in vocab_no_dupl:
		if word in ham_tc_dic:
			ham_denom+=ham_tc_dic[word]
		ham_denom+=1
		
	spam_denom = 0
	for word in vocab_no_dupl:
		if word in spam_tc_dic:
			spam_denom+=spam_tc_dic[word]
		spam_denom+=1
	
	# COMPUTATION OF COND_PROB: 
	
	for word in ham_tc_dic:
		#cond_prob_ham[word] = (ham_tc_dic[word] + 1)/((len_vocab)+unique_vocab_size)
		cond_prob_ham[word] = (ham_tc_dic[word] + 1)/(ham_denom)
	
	for word in spam_tc_dic:
		#cond_prob_spam[word] = (spam_tc_dic[word] + 1)/((len_vocab)+unique_vocab_size)
		cond_prob_spam[word] = (spam_tc_dic[word] + 1)/(spam_denom)
		
		
	
				############################################### TESTING ###################################
	
	
	
	# #################### TESTING FOR TRAIN FOLDER ###################################
	
	
	NB_results = []
	for a_file_tuple in train_all_files_l:
		ham_score = math.log(prior_prob["ham"], 10) # SCORE FOR HAM
		spam_score = math.log(prior_prob["spam"], 10) # SCORE FOR SPAM
		doc_vocab = []
		
		with codecs.open((train_dir + '/' + a_file_tuple[1]), 'r', encoding='utf-8', errors='ignore') as email_file:  # e.g. read trec-397/data/train/inmail.1, ../inmail.2, and so on 
			#ignores all characters that are NOT utf-8 type
			email_f_text = email_file.read()
			# removing HTML from emails: 
			s = MLStripper()
			s.feed(email_f_text)
			text_no_HTML = s.get_data()
			# spam_vocab.append(text_no_HTML.split()) # split HTML-less text without spaces (list of lists method)
			email_no_HTML = text_no_HTML.split() # split HTML-less text without spaces
			for word in email_no_HTML:
				doc_vocab.append(word) # (list of words method)
		
		for word in doc_vocab:
			if word in cond_prob_ham:
				ham_score+=math.log(cond_prob_ham[word],10) 
	
			# else do nothing
		for word in doc_vocab:
			if word in cond_prob_spam:
				spam_score+=math.log(cond_prob_spam[word],10)
			# else do nothing
				
		if ham_score < spam_score:
			NB_results.append((a_file_tuple[0], a_file_tuple[1], "ham",))
		else:
			NB_results.append((a_file_tuple[0], a_file_tuple[1], "spam",))
			
		# assigning classes according to NB algorithm	
		
		# concatenating a_file_tuple with whether the document is supposed to be "ham" or "spam" according to the Naive Bayes algorithm
		# therefore:
		# a_file_tuple[0] = whether or not the file is actually HAM/SPAM
		# a_file_tuple[1] = the file 
		# a_file_tuple[2] = what NB algorithm determines the file to be
		
	accuracy_counter = 0
	#print(NB_results)
		
	for a_file_tuple in NB_results:
		if (a_file_tuple[0] == a_file_tuple[2]):
			accuracy_counter+=1
		# else do nothing
		#else:
			#print(a_file_tuple[0], a_file_tuple[2])
	
	#print(len(NB_results), len(train_all_files_l))
		
	accuracy = (accuracy_counter/(len(train_all_files_l)))
	print("Training accuracy:", '%.2f' % float(accuracy*100), "%") 
	
	
	
	#################### TESTING FOR TEST FOLDER #########################################
	
	
	
	test_idx_file = open((test_dir + '/' + 'index'), 'r') # index file
	test_idx_text = test_idx_file.read()
	test_all_files_l = re.findall("(spam|ham) (.+)", test_idx_text)
	NB_results_test = []
	
	for a_file_tuple in test_all_files_l:
		ham_score = math.log(prior_prob["ham"], 10)
		spam_score = math.log(prior_prob["spam"], 10)
		doc_vocab = []
		
		with codecs.open((test_dir + '/' + a_file_tuple[1]), 'r', encoding='utf-8', errors='ignore') as email_file:  # e.g. read trec-397/data/train/inmail.1, ../inmail.2, and so on 
			#ignores all characters that are NOT utf-8 type
			email_f_text = email_file.read()
			# removing HTML from emails: 
			s = MLStripper()
			s.feed(email_f_text)
			text_no_HTML = s.get_data()
			# spam_vocab.append(text_no_HTML.split()) # split HTML-less text without spaces (list of lists method)
			email_no_HTML = text_no_HTML.split() # split HTML-less text without spaces
			for word in email_no_HTML:
				doc_vocab.append(word) # (list of words method)
		
		for word in doc_vocab:
			if word in cond_prob_ham:
				ham_score+=math.log(cond_prob_ham[word],10)
			# else do nothing
			
		for word in doc_vocab:
			if word in cond_prob_spam:
				spam_score+=math.log(cond_prob_spam[word],10)
			# else do nothing
				
		if ham_score < spam_score:
			NB_results_test.append((a_file_tuple[0], a_file_tuple[1], "ham",))
		else:
			NB_results_test.append((a_file_tuple[0], a_file_tuple[1], "spam",))
			
		# assigning classes according to NB algorithm	
		
		# concatenating a_file_tuple with whether the document is supposed to be "ham" or "spam" according to the Naive Bayes algorithm
		# therefore:
		# a_file_tuple[0] = whether or not the file is actually HAM/SPAM
		# a_file_tuple[1] = the file 
		# a_file_tuple[2] = what NB algorithm determines the file to be
		
	accuracy_counter = 0
	#print(NB_results)
		
	for a_file_tuple in NB_results_test:
		if (a_file_tuple[0] == a_file_tuple[2]):
			accuracy_counter+=1
		# else do nothing
		#else:
			#print(a_file_tuple[0], a_file_tuple[2])
	
	#print(len(NB_results_test), len(test_all_files_l))
		
	accuracy = (accuracy_counter/(len(test_all_files_l)))
	print("Test accuracy:", '%.2f' % float(accuracy*100), "%") 
				
	
	train_idx_file.close()
	test_idx_file.close()
	
if __name__ == "__main__":
	main()