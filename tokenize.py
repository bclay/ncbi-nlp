#imports
from nltk.tokenize import RegexpTokenizer

#initialize

#create an array of tokens
def create_tokens(string):
	tokenizer = RegexpTokenizer(r'\w+')
	words = tokenizer.tokenize(string)
	lc_words = [w.lower() for w in words]
	return lc_words

create_tokens("This is a sentence")
	