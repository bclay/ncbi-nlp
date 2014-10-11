#imports
from nltk.tokenize import RegexpTokenizer

#initialize

#create an array of tokens
def create_tokens(str):
	tokenizer = RegexpTokenizer(r'\w+')
	words = tokenizer.tokenize(str)
	lc_words = [w.lower() for w in words]
	return lc_words

print create_tokens("This is a sentence.")
	