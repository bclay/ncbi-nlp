#imports
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

#create an array of tokens
def create_tokens(str):
	tokenizer = RegexpTokenizer(r'\w+')
	words = tokenizer.tokenize(str)
	lc_words = [w.lower() for w in words]
	return lc_words

def remove_words(arr):
	clean_arr = []
	stop = stopwords.words('english')
	for w in arr:
		if w not in stop:
			clean_arr.append(w)
	return clean_arr

tok_arr = create_tokens("This is a sentence.")
print remove_words(tok_arr)	