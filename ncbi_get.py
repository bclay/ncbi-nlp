#imports
import requests
import xml.etree.ElementTree as ET

base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
fetch = 'efetch.fcgi?db='
idq = '&id='
ret = '&rettype=xml'
search = 'esearch.fcgi?db='
term = '&term='

def get_request():
	#get a list of pubmed ids
	db = 'gene'
	gid = '1056'
	
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
	db = 'gene'
	organism = '+AND+("Homo%20sapiens"[porgn:__txid9606])+&usehistory=y'

	for in_arr in arr:
		for gene in in_arr:
			url = base+search+db+term+gene+organism
			r = requests.get(url)
			root = ET.fromstring(r.text)
			string = "\t\t\t\t\t"+gene
			print string
			for gid in root.iter('Id'):
				print gid.text

				url2 = base+fetch+db+idq+gid.text+ret
				r2 = requests.get(url2)
				root2 = ET.fromstring(r2.text.encode('ascii', 'ignore'))
				for loc in root2.iter('Gene-ref_locus'):
					if gene.lower() == loc.text.lower():
						print loc.text.lower()
				for ref in root2.iter('Gene-ref_syn'):
					for refe in ref.iter('Gene-ref_syn_E'):
						if gene.lower() == refe.text.lower():
							print refe.text.lower()

get_entrez([['amy2','cel'],['cmyc']])