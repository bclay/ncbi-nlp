#imports
import requests
import xml.etree.ElementTree as ET
from Bio import Medline

def get_request():
	#get a list of pubmed ids
	db = 'pubmed'
	#query = 'asthma[mesh]+AND+leukotrienes[mesh]+AND+2009[pdat]'
	base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
	#url = base+'esearch.fcgi?db='+db+'&term='+query+'&usehistory=y'
	url = base + 'esearch.fcgi?LinkName=gene_pubmed&from_uid=1056'
	r = requests.get(url)
	print "Search"
	print r.text
	#get abstracts from the pubmed ids
	#print 'doing something'
	#pid = '20113659'
	#url = base+'efetch.fcgi?db='+db+'&id='+pid+'&rettype=xml'
	#r2 = requests.get(url)
	#print 'through request'
	#print r2.text
	#lines = r2.text.split("\n")
	#for line in lines:
	#	parts = line.split(" ")
	#	print parts[0]
		#parts = line.split()
		#print parts[0]
	#record = Medline.parse(r2.text)


	#print record
	#r2json = json.loads(r2.text)
	#print r2json




# useful pubmed parsing code

	#root2 = ET.fromstring(r2.text)
	#for abst in root2.iter('Abstract'):
	#	for sec in abst.iter('AbstractText'):
	#		print sec.text


	#iterate through ids and return abstracts
	#root = ET.fromstring(r.text)
	#for pubid in root.iter('Id'):
		#print pubid.text




get_request()