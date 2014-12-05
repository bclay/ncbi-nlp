#imports
import requests
import xml.etree.ElementTree as ET
from Bio import Medline

def get_request():
	#get a list of pubmed ids
	db = 'pubmed'
	query = 'asthma[mesh]+AND+leukotrienes[mesh]+AND+2009[pdat]'
	base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
	url = base+'esearch.fcgi?db='+db+'&term='+query+'&usehistory=y'
	r = requests.get(url)
	#print "Search"
	#print r.text
	#get abstracts from the pubmed ids

	pid = '20113659'
	url = base+'efetch.fcgi?db='+db+'&id='+pid+'&rettype=medline'
	r2 = requests.get(url)
	print r2.text
	record = Medline.read(r2.text)


	print record
	#r2json = json.loads(r2.text)
	#print r2json






	#root2 = ET.fromstring(r2.text)
	#for abst in root2.iter('abstract'):
	#	for sec in abst.iter('sec'):
	#		for child in sec:
				#print child.tag
	#			if child.tag == 'p':
	#				print child.text

	#iterate through ids and return abstracts
	#root = ET.fromstring(r.text)
	#for pubid in root.iter('Id'):
		#print pubid.text




get_request()