#imports
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import operator
import requests
import xml.etree.ElementTree as ET
import pickle

base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
fetch = 'efetch.fcgi?db='
idq = '&id='
ret = '&rettype=xml'
search = 'esearch.fcgi?db='
term = '&term='

#takes in a 2d array of gene names
#returns an array of dictionaries of arrays
#outer array should have 4 dicts, represent the groups/figures
#keys are gene names
#values are arrays of entrez ids representing each gene name
def get_entrez(arr):
	eids_out = []
	report = []
	db = 'gene'
	organism = '+AND+("Homo%20sapiens"[porgn:__txid9606])+&usehistory=y'

	f = open('report1.txt','w')

	for in_arr in arr:
		reporting_dict = {}
		for gene in in_arr:
			print gene
			eid_arr = []
			url = base+search+db+term+gene+organism
			r = requests.get(url)
			root = ET.fromstring(r.text)
			for gid in root.iter('Id'):
				print gid.text
				url2 = base+fetch+db+idq+gid.text+ret
				r2 = requests.get(url2)
				root2 = ET.fromstring(r2.text.encode('ascii', 'ignore'))
				for loc in root2.iter('Gene-ref_locus'):
					if gene.lower() == loc.text.lower():
						 eid_arr.append(gid.text)
				for ref in root2.iter('Gene-ref_syn'):
					for refe in ref.iter('Gene-ref_syn_E'):
						if gene.lower() == refe.text.lower():
							eid_arr.append(gid.text)
			reporting_dict[gene] = eid_arr
			print eid_arr
			line = gene+'\t'+str(len(eid_arr))+'\n'
			f.write(line)
		eids_out.append(reporting_dict)
	f.close()
	return eids_out

#keeps track of structure for getting abstracts
#returns a file of similar structure, and array of dictionaries of arrays
def abstr_wrapper(entrez):
	outer = []
	for fig in entrez:
		d = {}
		for gname in fig:
			abstracts = []
			for gid in gname:
				abstracts.append(get_abstr(gid))
			d[gname] = abstracts

#takes in a gene entrez id
#returns all related pubmed abstracts
def get_abstr(gid):
	#get a list of pubmed ids
	db = 'gene'
	url = base+fetch+db+idq+gid+ret
	r = requests.get(url)
	pubids = []
	root = ET.fromstring(r.text)
	for comm in root.iter('Entrezgene_comments'):
		for c1 in comm.iter('Gene-commentary'):
			for c2 in c1.iter('Gene-commentary_type'):
				if c2.text == '254':
					for c5 in c1.iter('PubMedId'):
						pubids.append(c5.text)

	#get abstracts from the pubmed ids
	out_arr = []
	db = 'pubmed'
	for pid in pubids:
		url = base+fetch+db+idq+pid+ret
		r2 = requests.get(url)
		root2 = ET.fromstring(r2.text.encode('ascii', 'ignore'))
		for abst in root2.iter('Abstract'):
			for sec in abst.iter('AbstractText'):
				out_arr.append(sec.text)

	return out_arr


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

#runs all the code together, saving parts in the middle
#with pickle
#take in a 2D array of gene names
#return 42
def gene_to_keywords(input_arr):
	#creates an array with dictionaries for figures
	#and gene names in each category
	entrez = get_entrez(input_arr)
	abstr = abstr_wrapper(entrez)
	return 42

#step-by-step to be used with pickle
def gene_to_kw_pickle():
	pass

#preparing input
f2 = ['amy2', 'bmp7', 'cel', 'cpa1', 'ctrl', 'dll1', 'ela', 'nr5a2', 'p2rx1', 'pnlip', 'prss1', 'ptpn6', 'rbpj', 'rbpjl', 'rhov']
f3 = ['cmyc', 'hdac1', 'insm1', 'irx1', 'irx2', 'mnx1', 'myt1', 'neurod2', 'phox2b', 'smad7', 'sst', 'tm4sf4']
f4 = ['atf2', 'atf3', 'egr1', 'foxo1', 'g6pc2', 'glp1r', 'rbp4', 'slc2a2']
f5 = ['ccna2', 'ccnd2', 'cdk4', 'chgb', 'dnmt1a', 'foxm1', 'ia2', 'irs2', 'mecp2', 'nfatc1', 'slc30a8', 'tnfa']


#code that's actually run
with open('pic_get_entrez.txt','wb') as fi:
	pickle.dump(gene_to_keywords([f2,f3,f4,f5]),fi)