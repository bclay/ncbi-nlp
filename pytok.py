#imports
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

#create an array of tokens
def create_tokens(str):
	tokenizer = RegexpTokenizer(r"\w+(-\w+)*")
	words = tokenizer.tokenize(str)
	lc_words = [w.lower() for w in words]
	return lc_words

#remove stop words
def rm_words(word_arrs):
	d = {}
	stop = stopwords.words('english')
	for w in word_arr:
		if w not in stop:
			if w in d:
				d[w] += 1
			else:
				d[w] = 1
	return d

#remove words that overlap between paragraphs
def rm_overlap(para_arr):
	print 1

#the over-arching steps that bring together all the functions
def final_steps(para_arr_col):
	for para_arr in para_arr_col:
		tok_arr = []
		for para in para_arr:
			tok_arr = create_tokens(para)
		stopless_dict = rm_words(tok_arr)
	print stopless_arr
	print "REMOVE OVERLAP"
	print rm_overlap(stopless_arr)

#executed code
para1 = "After removal of the precursor signal peptide, proinsulin is post-translationally cleaved into three peptides: the B chain and A chain peptides, which are covalently linked via two disulfide bonds to form insulin, and C-peptide. Binding of insulin to the insulin receptor (INSR) stimulates glucose uptake. A multitude of mutant alleles with phenotypic effects have been identified. There is a read-through gene, INS-IGF2, which overlaps with this gene at the 5' region and with the IGF2 gene at the 3' region. Alternative splicing results in multiple transcript variants. [provided by RefSeq, Jun 2010]"
para2 = "The protein encoded by this gene is a transcriptional activator of several genes, including insulin, somatostatin, glucokinase, islet amyloid polypeptide, and glucose transporter type 2. The encoded nuclear protein is involved in the early development of the pancreas and plays a major role in glucose-dependent regulation of insulin gene expression. Defects in this gene are a cause of pancreatic agenesis, which can lead to early-onset insulin-dependent diabetes mellitus (NIDDM), as well as maturity onset diabetes of the young type 4 (MODY4). [provided by RefSeq, Jul 2008]"
#final_steps([[para1],[para2]])
tok_arr = create_tokens(para1)
print rm_words(tok_arr)