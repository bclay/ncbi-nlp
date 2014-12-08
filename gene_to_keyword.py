#imports
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import operator

#create an array of tokens
#input: string
#output: array of tokens (words)
def create_tokens(str):
	tokenizer = RegexpTokenizer(r"\w+(-\w+)*")
	words = tokenizer.tokenize(str)
	lc_words = [w.lower() for w in words]
	return lc_words

#remove stop words
#input: a large token array representing multiple summaries
#output: dictionary with words counts
def rm_words(word_arr):
	d = {}
	stop = stopwords.words('english')
	for w in word_arr:
		if w not in stop:
			if not w.isdigit():
				if w in d:
					d[w] += 1
				else:
					d[w] = 1
	return d

#remove words that overlap between paragraphs
#input: array of dictionaries
#output: only words not repeated between dictionaries
def rm_overlap(dict_arr):
	temp_dict_arr = []
	overall_dict = {}
	repeats_dict= {}
	f = open('overlap1.txt','w')
	for d in dict_arr:
		final_dict = {}
		for key in d:
			if key in overall_dict:
				if key in final_dict:
					del final_dict[key]
				f.write(key)
				repeats_dict[key] = 1
			else:
				if key not in repeats_dict:
					final_dict[key] = d[key]
					overall_dict[key] = d[key]
				else:
					if key in final_dict:
						del final_dict[key]
		temp_dict_arr.append(final_dict)
	f.close()
	final_arr = []
	for d in temp_dict_arr:
		temp_dict = {}
		for key in d:
			if key not in repeats_dict:
				temp_dict[key] = d[key]
			#temp_dict[key] = 1
			#for rep in repeats_dict:
				#if rep in key:
					#if key in temp_dict:
						#del temp_dict[key]
		sorted_dict = sorted(temp_dict.items(), key=operator.itemgetter(1))
		rev_arr.append(sorted_dict)
		final_arr = rev_arr.reverse()
	return final_arr

#the over-arching steps that bring together all the functions
def final_steps(para_arr_col):
	dict_arr = []
	for para_arr in para_arr_col:
		tok_arr = []
		for para in para_arr:
			tok_arr.extend(create_tokens(para))
		stopless_dict = rm_words(tok_arr)
		dict_arr.append(stopless_dict)
	final_arr = rm_overlap(dict_arr)
	f = open('get_out/results2.txt','w')
	f.write(final_arr)
	f.close()