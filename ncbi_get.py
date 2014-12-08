#imports
import requests
import xml.etree.ElementTree as ET

def get_request():
	#get a list of pubmed ids
	db = 'gene'
	fetch = 'efetch.fcgi?db='
	ret = '&rettype=xml'
	idq = '&id='
	gid = '1056'
	base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
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
	db = 'pubmed'
	for pid in pubids:
		url = base+fetch+db+idq+pid+ret
		r2 = requests.get(url)
		root2 = ET.fromstring(r2.text.encode('ascii', 'ignore'))
		for abst in root2.iter('Abstract'):
			for sec in abst.iter('AbstractText'):
				print sec.text


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

	


	#iterate through ids and return abstracts
	#root = ET.fromstring(r.text)
	#for pubid in root.iter('Id'):
		#print pubid.text

#24062244


#get_request()


def get_entrez(arr):
	pass

get_entrez([['amy2']])