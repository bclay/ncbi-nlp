#imports
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import operator
import requests
import xml.etree.ElementTree as ET
import pickle
import math

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

	f = open('report5.txt','w')

	for in_arr in arr:
		reporting_dict = {}
		for gene in in_arr:
			print gene
			eid_arr = []
			url = base+search+db+term+gene+organism
			r = requests.get(url)
			root = ET.fromstring(r.text)
			for gid in root.iter('Id'):
				#print gid.text
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
			line = gene+'\t'+str(len(eid_arr))
			for g in eid_arr:
				line += '\t' + g
			line += '\n'
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
			print gname
			abstracts = []
			for gid in gname:
				abstracts.append(get_abstr(gid))
			d[gname] = abstracts
		outer.append(d)
	return outer

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
	f = open('overlap8.txt','w')
	for d in dict_arr:
		final_dict = {}
		for key in d:
			if key in overall_dict:
				if key in final_dict:
					del final_dict[key]
				kline = key + '\n'
				f.write(kline)
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
		print temp_dict
		sorted_dict = sorted(temp_dict.items(), key=operator.itemgetter(1))
		final_arr.append(sorted_dict)
	return final_arr

#the over-arching steps that bring together all the functions
def final_steps(para_arr_col):
	dict_arr = []
	doc_count = 0
	#print para_arr_col
	for fig in para_arr_col:
		stopless_dict = []
		tok_arr = []
		for gene in fig:
			#print gene
			for group in fig[gene]:
				for title in group:
					if title:
						#print title
						stopless_dict.append(rm_words(create_tokens(title)))
						doc_count += 1

		cd = compact_dict(stopless_dict)
		#print cd
		dict_arr.append(cd)
	idf = get_idf(dict_arr, doc_count)
	print_dict_idf(idf, 'idf_abstr1.txt')
	res = []
	for docc in dict_arr:
		#print docc
		res.append(get_tfidf_top(docc, idf, 30))
	return res

#input an array of dictionaries, where all words have independent doc counts
#combine the dictionaries into one
#don't add the counts, just take 1 per doc
def compact_dict(a):
	cd = {}
	for d in a:
		for k in d:
			if k in cd:
				cd[k] += 1
			else:
				cd[k] = 1
	return cd

	#final_arr = rm_overlap(dict_arr)
	#return final_arr
def print_dict_tf(words, filename):
	final_arr = []
	out = open(filename,'a')
	out.write("\t\tNEW FIGURE\n")
	sorted_dict = sorted(words.items(), key=operator.itemgetter(1))
	final_arr = reversed(sorted_dict)
	for tup in final_arr:
		x, y = tup
		st = x + ' : ' + str(y) + '\n'
		if y > 1:
			out.write(st)
	out.close()

def print_dict_idf(words, filename):
	final_arr = []
	out = open(filename,'w')
	sorted_dict = sorted(words.items(), key=operator.itemgetter(1))
	for tup in sorted_dict:
		x, y = tup
		st = x + ' : ' + str(y) + '\n'
		out.write(st)
	out.close()

def get_tf(itemlist):
  d = {}
  max_count = 1
  for word in itemlist:
    if word in d:
      d[word] += 1
      if d[word] > max_count:
        max_count = d[word]
    else:
      d[word] = 1
  for key in d:
    d[key] = d[key] / float(max_count)
  return d

def get_idf(itemlist, doc_count):
  d = {}
  for doc in itemlist:
    for word in doc:
      if word in d:
        d[word] += doc[word]
      else:
        d[word] = doc[word]
  for key in d:	
    d[key] = math.log1p(float(doc_count) / d[key])
  return d

def get_top(d, k):
  #print d
  sorted_d = sorted(d.items(), key = operator.itemgetter(1))
  #sorted_d = sorted(d, key=lambda tup: tup[1])
  sorted_d.reverse()
  #print sorted_d
  sorted_list = []
  for x in range(k):
    #print x
    sorted_list.append((sorted_d[x]))
  #print sorted_list
  return sorted_list

def get_tfidf(dict1, dict2):
  d = {}
  for key in dict1:
    if key in dict2:
      d[key] = float(dict1[key]) * float(dict2[key])
    else:
      d[key] = 0
  return d

def get_tfidf_top(dict1, dict2, k):
  return get_top(get_tfidf(dict1, dict2), k)

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

def print_pickle(filename):
	abstr = []
	with open(filename, 'rb') as f:
		abstr = pickle.load(f)
	print abstr
	for fig in abstr:
		for k in fig:
			print k
			for a in fig[k]:
				print a

def print_pickle2(filename):
	abstr = []
	with open(filename, 'rb') as f:
		abstr = pickle.load(f)
	print abstr

def pretty_out(final):
	f = open('newidf1.txt','w')
	for li in final:
		f.write('\t\t\tNEW FIGURE \n')
		for w in li:
			line = w[0] + ' : ' + str(w[1]) + '\n'
			f.write(line)
	f.close()


#safe parsing
parser = ET.XMLParser()
parser.entity["nbsp"] = unichr(160)

#preparing input
f2 = ['amy2', 'bmp7', 'cel', 'cpa1', 'ctrl', 'dll1', 'ela', 'nr5a2', 'p2rx1', 'pnlip', 'prss1', 'ptpn6', 'rbpj', 'rbpjl', 'rhov']
f3 = ['cmyc', 'hdac1', 'insm1', 'irx1', 'irx2', 'mnx1', 'myt1', 'neurod2', 'phox2b', 'smad7', 'sst', 'tm4sf4']
f4 = ['atf2', 'atf3', 'egr1', 'foxo1', 'g6pc2', 'glp1r', 'rbp4', 'slc2a2']
f5 = ['ccna2', 'ccnd2', 'cdk4', 'chgb', 'dnmt1a', 'foxm1', 'ia2', 'irs2', 'mecp2', 'nfatc1', 'slc30a8', 'tnfa']

#f2e = {'amy2':[279,280],'bmp7':[655],'cel':[1056],'cpa1':[1357],1506,28514,100506013,2494,5023,5406,5644,11317,171177}
#f3e = [3642,79192,153572]
#f4e = []
#f5e = []
#code that's actually run
#with open('pic_get_entrez5.txt','wb') as fi:
	#pickle.dump(get_entrez([f2,f3,f4,f5]),fi)
#print_pickle('./get_out/pic_get_entrez.txt')

#with open('pic_get_entrez4.txt','rb') as f:
#	entrez = pickle.load(f)
#print 'entrez loaded'
#abstracts = abstr_wrapper(entrez)
#print 'abstr_wrapper run'
#with open('pic_get_abstr5.txt','rb') as fi:
#	pickle.dump(abstracts,fi)
with open('abstr/pic_get_abstr5.txt','rb') as f:
	abstr = pickle.load(f)
##print abstr
final = final_steps(abstr)
###print 'final steps done'
#print final
#with open('pic_get_words8.txt','wb') as fi2:
#	pickle.dump(final,fi2)
#print_pickle2('pic_get_words8.txt')
pretty_out(final)
#d = {'word':11.1,'other':2.5,'brynn':88,'errrrythang':992}
#print get_top(d,3)

