#imports
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

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
	for d in dict_arr:
		final_dict = {}
		for key in d:
			if key in overall_dict:
				if key in final_dict:
					del final_dict[key]
				print "repeats"
				print key
				repeats_dict[key] = 1
			else:
				if key not in repeats_dict:
					final_dict[key] = 1
					overall_dict[key] = 1
				else:
					if key in final_dict:
						del final_dict[key]
		temp_dict_arr.append(final_dict)
	final_arr = []
	for d in temp_dict_arr:
		temp_dict = {}
		for key in d:
			if key not in repeats_dict:
				temp_dict[key] = 1
			#temp_dict[key] = 1
			#for rep in repeats_dict:
				#if rep in key:
					#if key in temp_dict:
						#del temp_dict[key]
		final_arr.append(temp_dict)
	return final_arr

#the over-arching steps that bring together all the functions
def final_steps(para_arr_col):
	dict_arr = []
	for para_arr in para_arr_col:
		tok_arr = []
		for para in para_arr:
			tok_arr.extend(create_tokens(para))
		stopless_dict = rm_words(tok_arr)
		stopless_dict
		dict_arr.append(stopless_dict)
	print "REMOVE OVERLAP"
	print rm_overlap(dict_arr)

#sample paragraphs
ins = "After removal of the precursor signal peptide, proinsulin is post-translationally cleaved into three peptides: the B chain and A chain peptides, which are covalently linked via two disulfide bonds to form insulin, and C-peptide. Binding of insulin to the insulin receptor (INSR) stimulates glucose uptake. A multitude of mutant alleles with phenotypic effects have been identified. There is a read-through gene, INS-IGF2, which overlaps with this gene at the 5' region and with the IGF2 gene at the 3' region. Alternative splicing results in multiple transcript variants. [provided by RefSeq, Jun 2010]"
pdx1 = "The protein encoded by this gene is a transcriptional activator of several genes, including insulin, somatostatin, glucokinase, islet amyloid polypeptide, and glucose transporter type 2. The encoded nuclear protein is involved in the early development of the pancreas and plays a major role in glucose-dependent regulation of insulin gene expression. Defects in this gene are a cause of pancreatic agenesis, which can lead to early-onset insulin-dependent diabetes mellitus (NIDDM), as well as maturity onset diabetes of the young type 4 (MODY4). [provided by RefSeq, Jul 2008]"
#f2
amy2 = "alpha-amylase, putative / 1,4-alpha-D-glucan glucanohydrolase, putative, strong similarity to alpha-amylase GI:7532799 from (Malus x domestica);contains Pfam profile PF00128: Alpha amylase, catalytic domain. Predicted to be secreted based on SignalP analysis."
bmp7 = "The bone morphogenetic proteins (BMPs) are a family of secreted signaling molecules that can induce ectopic bone growth. Many BMPs are part of the transforming growth factor-beta (TGFB) superfamily. BMPs were originally identified by an ability of demineralized bone extract to induce endochondral osteogenesis in vivo in an extraskeletal site. Based on its expression early in embryogenesis, the BMP encoded by this gene has a proposed role in early development and possible bone inductive activity. [provided by RefSeq, Jul 2008]"
cel = "The protein encoded by this gene is a glycoprotein secreted from the pancreas into the digestive tract and from the lactating mammary gland into human milk. The physiological role of this protein is in cholesterol and lipid-soluble vitamin ester hydrolysis and absorption. This encoded protein promotes large chylomicron production in the intestine. Also its presence in plasma suggests its interactions with cholesterol and oxidized lipoproteins to modulate the progression of atherosclerosis. In pancreatic tumoral cells, this encoded protein is thought to be sequestrated within the Golgi compartment and is probably not secreted. This gene contains a variable number of tandem repeat (VNTR) polymorphism in the coding region that may influence the function of the encoded protein. [provided by RefSeq, Jul 2008]"
ela = "Elastases form a subfamily of serine proteases that hydrolyze many proteins in addition to elastin. Humans have six elastase genes which encode the structurally similar proteins elastase 1, 2, 2A, 2B, 3A, and 3B. Unlike other elastases, pancreatic elastase 1 is not expressed in the pancreas. To date, elastase 1 expression has only been detected in skin keratinocytes. Clinical literature that describes human elastase 1 activity in the pancreas or fecal material is actually referring to chymotrypsin-like elastase family, member 3B. [provided by RefSeq, May 2009]"
f2 = [amy2, bmp7, cel, ela]
#f3
hdac1 = "Histone acetylation and deacetylation, catalyzed by multisubunit complexes, play a key role in the regulation of eukaryotic gene expression. The protein encoded by this gene belongs to the histone deacetylase/acuc/apha family and is a component of the histone deacetylase complex. It also interacts with retinoblastoma tumor-suppressor protein and this complex is a key element in the control of cell proliferation and differentiation. Together with metastasis-associated protein-2, it deacetylates p53 and modulates its effect on cell growth and apoptosis. [provided by RefSeq, Jul 2008]"
sst = "The hormone somatostatin has active 14 aa and 28 aa forms that are produced by alternate cleavage of the single preproprotein encoded by this gene. Somatostatin is expressed throughout the body and inhibits the release of numerous secondary hormones by binding to high-affinity G-protein-coupled somatostatin receptors. This hormone is an important regulator of the endocrine system through its interactions with pituitary growth hormone, thyroid stimulating hormone, and most hormones of the gastrointestinal tract. Somatostatin also affects rates of neurotransmission in the central nervous system and proliferation of both normal and tumorigenic cells. [provided by RefSeq, Jul 2008]"
f3 = [hdac1, sst]

#executed code
final_steps([f2,f3])