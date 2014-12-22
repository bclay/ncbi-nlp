#imports
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import operator
import requests
import xml.etree.ElementTree as ET
import pickle
import math

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
	stopless_dict = []
	doc_count = 0
	for fig in para_arr_col:
		tok_arr = []
		for p in fig:
			#tok_arr.append(create_tokens(p))
			stopless_dict.append(rm_words(create_tokens(p)))
			doc_count += 1
		#stopless_dict = rm_words(tok_arr)
		#print_dict(stopless_dict, 'tf3.txt')
		#print_dict(stopless_dict)
		cd = compact_dict(stopless_dict)
		dict_arr.append(cd)
	#idf
	#for doc in dict_arr:
	#arrs = []
	#for doc in dict_arr:
		#arrs.append(doc.keys())
	res = []
	#print arrs
	idf = get_idf(dict_arr, doc_count)
	print_dict_idf(idf, 'idf5.txt')
	for docc in dict_arr:
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
	f = open('sum_results5.txt','w')
	for li in final:
		f.write('\t\t\tNEW FIGURE \n')
		for w in li:
			line = w[0] + ' : ' + str(w[1]) + '\n'
			f.write(line)
	f.close()


#safe parsing
parser = ET.XMLParser()
parser.entity["nbsp"] = unichr(160)

#f2
amy2 = "alpha-amylase, putative / 1,4-alpha-D-glucan glucanohydrolase, putative, strong similarity to alpha-amylase GI:7532799 from (Malus x domestica);contains Pfam profile PF00128: Alpha amylase, catalytic domain. Predicted to be secreted based on SignalP analysis."
bmp7 = "The bone morphogenetic proteins (BMPs) are a family of secreted signaling molecules that can induce ectopic bone growth. Many BMPs are part of the transforming growth factor-beta (TGFB) superfamily. BMPs were originally identified by an ability of demineralized bone extract to induce endochondral osteogenesis in vivo in an extraskeletal site. Based on its expression early in embryogenesis, the BMP encoded by this gene has a proposed role in early development and possible bone inductive activity. [provided by RefSeq, Jul 2008]"
cel = "The protein encoded by this gene is a glycoprotein secreted from the pancreas into the digestive tract and from the lactating mammary gland into human milk. The physiological role of this protein is in cholesterol and lipid-soluble vitamin ester hydrolysis and absorption. This encoded protein promotes large chylomicron production in the intestine. Also its presence in plasma suggests its interactions with cholesterol and oxidized lipoproteins to modulate the progression of atherosclerosis. In pancreatic tumoral cells, this encoded protein is thought to be sequestrated within the Golgi compartment and is probably not secreted. This gene contains a variable number of tandem repeat (VNTR) polymorphism in the coding region that may influence the function of the encoded protein. [provided by RefSeq, Jul 2008]"
cpa1 = "Three different forms of human pancreatic procarboxypeptidase A have been isolated. This gene encodes a monomeric pancreatic exopeptidase involved in zymogen inhibition. [provided by RefSeq, Jan 2009]"
ctrl = "pancreatic digestive serine protease"
dll1 = "DLL1 is a human homolog of the Notch Delta ligand and is a member of the delta/serrate/jagged family. It plays a role in mediating cell fate decisions during hematopoiesis. It may play a role in cell-to-cell communication. [provided by RefSeq, Jul 2008]"
ela = "Elastases form a subfamily of serine proteases that hydrolyze many proteins in addition to elastin. Humans have six elastase genes which encode the structurally similar proteins elastase 1, 2, 2A, 2B, 3A, and 3B. Unlike other elastases, pancreatic elastase 1 is not expressed in the pancreas. To date, elastase 1 expression has only been detected in skin keratinocytes. Clinical literature that describes human elastase 1 activity in the pancreas or fecal material is actually referring to chymotrypsin-like elastase family, member 3B. [provided by RefSeq, May 2009]"
nr5a2 = "an orphan nuclear receptor that may bind DNA and activate gene transcription [RGD, Feb 2006]"
p2rx1 = "The protein encoded by this gene belongs to the P2X family of G-protein-coupled receptors. These proteins can form homo-and heterotimers and function as ATP-gated ion channels and mediate rapid and selective permeability to cations. This protein is primarily localized to smooth muscle where binds ATP and mediates synaptic transmission between neurons and from neurons to smooth muscle and may being responsible for sympathetic vasoconstriction in small arteries, arterioles and vas deferens. Mouse studies suggest that this receptor is essential for normal male reproductive function. This protein may also be involved in promoting apoptosis. [provided by RefSeq, Jun 2013]"
pnlip = "This gene is a member of the lipase gene family. It encodes a carboxyl esterase that hydrolyzes insoluble, emulsified triglycerides, and is essential for the efficient digestion of dietary fats. This gene is expressed specifically in the pancreas. [provided by RefSeq, Jul 2008]"
prss1 = "This gene encodes a trypsinogen, which is a member of the trypsin family of serine proteases. This enzyme is secreted by the pancreas and cleaved to its active form in the small intestine. It is active on peptide linkages involving the carboxyl group of lysine or arginine. Mutations in this gene are associated with hereditary pancreatitis. This gene and several other trypsinogen genes are localized to the T cell receptor beta locus on chromosome 7. [provided by RefSeq, Jul 2008]"
ptpn6 = "The protein encoded by this gene is a member of the protein tyrosine phosphatase (PTP) family. PTPs are known to be signaling molecules that regulate a variety of cellular processes including cell growth, differentiation, mitotic cycle, and oncogenic transformation. N-terminal part of this PTP contains two tandem Src homolog (SH2) domains, which act as protein phospho-tyrosine binding domains, and mediate the interaction of this PTP with its substrates. This PTP is expressed primarily in hematopoietic cells, and functions as an important regulator of multiple signaling pathways in hematopoietic cells. This PTP has been shown to interact with, and dephosphorylate a wide spectrum of phospho-proteins involved in hematopoietic cell signaling. Multiple alternatively spliced variants of this gene, which encode distinct isoforms, have been reported. [provided by RefSeq, Jul 2008]"
rbpj = "The protein encoded by this gene is a transcriptional regulator important in the Notch signaling pathway. The encoded protein acts as a repressor when not bound to Notch proteins and an activator when bound to Notch proteins. It is thought to function by recruiting chromatin remodeling complexes containing histone deacetylase or histone acetylase proteins to Notch signaling pathway genes. Several transcript variants encoding different isoforms have been found for this gene, and several pseudogenes of this gene exist on chromosome 9. [provided by RefSeq, Oct 2013]"
rbpjl = "This gene encodes a member of the suppressor of hairless protein family. A similar protein in mouse is a transcription factor that binds to DNA sequences almost identical to that bound by the Notch receptor signaling pathway transcription factor recombining binding protein J. The mouse protein has been shown to activate transcription in concert with Epstein-Barr virus nuclear antigen-2. Alternative splicing results in multiple transcript variants. [provided by RefSeq, Jul 2013]"
rhov = "ras homolog gene family, member V"

f2 = [amy2, bmp7, cel, cpa1, ctrl, dll1, ela, nr5a2, p2rx1, pnlip, prss1, ptpn6, rbpj, rbpjl, rhov]

#f3
cmyc = "The protein encoded by this gene is a multifunctional, nuclear phosphoprotein that plays a role in cell cycle progression, apoptosis and cellular transformation. It functions as a transcription factor that regulates transcription of specific target genes. Mutations, overexpression, rearrangement and translocation of this gene have been associated with a variety of hematopoietic tumors, leukemias and lymphomas, including Burkitt lymphoma. There is evidence to show that alternative translation initiations from an upstream, in-frame non-AUG (CUG) and a downstream AUG start site result in the production of two isoforms with distinct N-termini. The synthesis of non-AUG initiated protein is suppressed in Burkitt's lymphomas, suggesting its importance in the normal function of this gene. [provided by RefSeq, Jul 2008]"
hdac1 = "Histone acetylation and deacetylation, catalyzed by multisubunit complexes, play a key role in the regulation of eukaryotic gene expression. The protein encoded by this gene belongs to the histone deacetylase/acuc/apha family and is a component of the histone deacetylase complex. It also interacts with retinoblastoma tumor-suppressor protein and this complex is a key element in the control of cell proliferation and differentiation. Together with metastasis-associated protein-2, it deacetylates p53 and modulates its effect on cell growth and apoptosis. [provided by RefSeq, Jul 2008]"
insm1 = "Insulinoma-associated 1 (INSM1) gene is intronless and encodes a protein containing both a zinc finger DNA-binding domain and a putative prohormone domain. This gene is a sensitive marker for neuroendocrine differentiation of human lung tumors. [provided by RefSeq, Jul 2008]"
irx1 = "This gene encodes a member of the Iroquois homeobox protein family. Homeobox genes in this family are involved in pattern formation in the embryo. The gene product has been identified as a tumor suppressor in gastric (PMID: 21602894, 20440264) and head and neck cancers (PMID: 18559491). A pseudogene of this gene is located on chromosome 13. [provided by RefSeq, Dec 2011]"
irx2 = "IRX2 is a member of the Iroquois homeobox gene family. Members of this family appear to play multiple roles during pattern formation of vertebrate embryos.[supplied by OMIM, Apr 2004]"
mnx1 = "This gene encodes a nuclear protein, which contains a homeobox domain and is a transcription factor. Mutations in this gene result in Currarino syndrome, an autosomic dominant congenital malformation. Alternatively spliced transcript variants encoding different isoforms have been found for this gene. [provided by RefSeq, Sep 2009]"
myt1 = "The protein encoded by this gene is a member of a family of neural specific, zinc finger-containing DNA-binding proteins. The protein binds to the promoter regions of proteolipid proteins of the central nervous system and plays a role in the developing nervous system. [provided by RefSeq, Jul 2008]"
neurod2 = "This gene encodes a member of the neuroD family of neurogenic basic helix-loop-helix (bHLH) proteins. Expression of this gene can induce transcription from neuron-specific promoters, such as the GAP-43 promoter, which contain a specific DNA sequence known as an E-box. The product of the human gene can induce neurogenic differentiation in non-neuronal cells in Xenopus embryos, and is thought to play a role in the determination and maintenance of neuronal cell fates. [provided by RefSeq, Jul 2008]"
phox2b = "The DNA-associated protein encoded by this gene is a member of the paired family of homeobox proteins localized to the nucleus. The protein functions as a transcription factor involved in the development of several major noradrenergic neuron populations and the determination of neurotransmitter phenotype. The gene product is linked to enhancement of second messenger-mediated activation of the dopamine beta-hydroylase, c-fos promoters and several enhancers, including cyclic amp-response element and serum-response element. [provided by RefSeq, Jul 2008]"
smad7 = "The protein encoded by this gene is a nuclear protein that binds the E3 ubiquitin ligase SMURF2. Upon binding, this complex translocates to the cytoplasm, where it interacts with TGF-beta receptor type-1 (TGFBR1), leading to the degradation of both the encoded protein and TGFBR1. Expression of this gene is induced by TGFBR1. Variations in this gene are a cause of susceptibility to colorectal cancer type 3 (CRCS3). Several transcript variants encoding different isoforms have been found for this gene. [provided by RefSeq, Jun 2010]"
sst = "The hormone somatostatin has active 14 aa and 28 aa forms that are produced by alternate cleavage of the single preproprotein encoded by this gene. Somatostatin is expressed throughout the body and inhibits the release of numerous secondary hormones by binding to high-affinity G-protein-coupled somatostatin receptors. This hormone is an important regulator of the endocrine system through its interactions with pituitary growth hormone, thyroid stimulating hormone, and most hormones of the gastrointestinal tract. Somatostatin also affects rates of neurotransmission in the central nervous system and proliferation of both normal and tumorigenic cells. [provided by RefSeq, Jul 2008]"
tm4sf4 = "The protein encoded by this gene is a member of the transmembrane 4 superfamily, also known as the tetraspanin family. Most of these members are cell-surface proteins that are characterized by the presence of four hydrophobic domains. The proteins mediate signal transduction events that play a role in the regulation of cell development, activation, growth and motility. This encoded protein is a cell surface glycoprotein that can regulate cell proliferation.[provided by RefSeq, Mar 2011]"
f3 = [cmyc, hdac1, insm1, irx1, irx2, mnx1, myt1, neurod2, phox2b, smad7, sst, tm4sf4]

#f4
atf2 = "This gene encodes a transcription factor that is a member of the leucine zipper family of DNA binding proteins. The encoded protein has been identified as a moonlighting protein based on its ability to perform mechanistically distinct functions This protein binds to the cAMP-responsive element (CRE), an octameric palindrome. It forms a homodimer or a heterodimer with c-Jun and stimulates CRE-dependent transcription. This protein is also a histone acetyltransferase (HAT) that specifically acetylates histones H2B and H4 in vitro; thus it may represent a class of sequence-specific factors that activate transcription by direct effects on chromatin components. The encoded protein may also be involved in cell's DNA damage response independent of its role in transcriptional regulation. Several alternatively spliced transcript variants have been found for this gene [provided by RefSeq, Jan 2014]"
atf3 = "This gene encodes a member of the mammalian activation transcription factor/cAMP responsive element-binding (CREB) protein family of transcription factors. This gene is induced by a variety of signals, including many of those encountered by cancer cells, and is involved in the complex process of cellular stress response. Multiple transcript variants encoding different isoforms have been found for this gene. It is possible that alternative splicing of this gene may be physiologically important in the regulation of target genes. [provided by RefSeq, Apr 2011]"
egr1 = "The protein encoded by this gene belongs to the EGR family of C2H2-type zinc-finger proteins. It is a nuclear protein and functions as a transcriptional regulator. The products of target genes it activates are required for differentitation and mitogenesis. Studies suggest this is a cancer suppresor gene. [provided by RefSeq, Jul 2008]"
foxo1 = "This gene belongs to the forkhead family of transcription factors which are characterized by a distinct forkhead domain. The specific function of this gene has not yet been determined; however, it may play a role in myogenic growth and differentiation. Translocation of this gene with PAX3 has been associated with alveolar rhabdomyosarcoma. [provided by RefSeq, Jul 2008]"
g6pc2 = "This gene encodes an enzyme belonging to the glucose-6-phosphatase catalytic subunit family. These enzymes are part of a multicomponent integral membrane system that catalyzes the hydrolysis of glucose-6-phosphate, the terminal step in gluconeogenic and glycogenolytic pathways, allowing the release of glucose into the bloodstream. The family member encoded by this gene is found in pancreatic islets and does not exhibit phosphohydrolase activity, but it is a major target of cell-mediated autoimmunity in diabetes. Several alternatively spliced transcript variants of this gene have been described, but their biological validity has not been determined. [provided by RefSeq, Jul 2008]"
glp1r = "induces insulin secretion; mediates neuroendocrine signaling of feeding behavior; mediates cardiovascular response and increased blood pressure [RGD, Feb 2006]"
rbp4 = "This protein belongs to the lipocalin family and is the specific carrier for retinol (vitamin A alcohol) in the blood. It delivers retinol from the liver stores to the peripheral tissues. In plasma, the RBP-retinol complex interacts with transthyretin which prevents its loss by filtration through the kidney glomeruli. A deficiency of vitamin A blocks secretion of the binding protein posttranslationally and results in defective delivery and supply to the epidermal cells. [provided by RefSeq, Jul 2008]"
slc2a2 = "This gene encodes an integral plasma membrane glycoprotein of the liver, islet beta cells, intestine, and kidney epithelium. The encoded protein mediates facilitated bidirectional glucose transport. Because of its low affinity for glucose, it has been suggested as a glucose sensor. Mutations in this gene are associated with susceptibility to diseases, including Fanconi-Bickel syndrome and noninsulin-dependent diabetes mellitus (NIDDM). Alternative splicing results in multiple transcript variants of this gene. [provided by RefSeq, Jul 2013]"
f4 = [atf2, atf3, egr1, foxo1, g6pc2, glp1r, rbp4, slc2a2]

#f5
ccna2 = "The protein encoded by this gene belongs to the highly conserved cyclin family, whose members are characterized by a dramatic periodicity in protein abundance through the cell cycle. Cyclins function as regulators of CDK kinases. Different cyclins exhibit distinct expression and degradation patterns which contribute to the temporal coordination of each mitotic event. In contrast to cyclin A1, which is present only in germ cells, this cyclin is expressed in all tissues tested. This cyclin binds and activates CDC2 or CDK2 kinases, and thus promotes both cell cycle G1/S and G2/M transitions. [provided by RefSeq, Jul 2008]"
ccnd2 = "The protein encoded by this gene belongs to the highly conserved cyclin family, whose members are characterized by a dramatic periodicity in protein abundance through the cell cycle. Cyclins function as regulators of CDK kinases. Different cyclins exhibit distinct expression and degradation patterns which contribute to the temporal coordination of each mitotic event. This cyclin forms a complex with CDK4 or CDK6 and functions as a regulatory subunit of the complex, whose activity is required for cell cycle G1/S transition. This protein has been shown to interact with and be involved in the phosphorylation of tumor suppressor protein Rb. Knockout studies of the homologous gene in mouse suggest the essential roles of this gene in ovarian granulosa and germ cell proliferation. High level expression of this gene was observed in ovarian and testicular tumors. Mutations in this gene are associated with megalencephaly-polymicrogyria-polydactyly-hydrocephalus syndrome 3 (MPPH3). [provided by RefSeq, Sep 2014]"
cdk4 = "The protein encoded by this gene is a member of the Ser/Thr protein kinase family. This protein is highly similar to the gene products of S. cerevisiae cdc28 and S. pombe cdc2. It is a catalytic subunit of the protein kinase complex that is important for cell cycle G1 phase progression. The activity of this kinase is restricted to the G1-S phase, which is controlled by the regulatory subunits D-type cyclins and CDK inhibitor p16(INK4a). This kinase was shown to be responsible for the phosphorylation of retinoblastoma gene product (Rb). Mutations in this gene as well as in its related proteins including D-type cyclins, p16(INK4a) and Rb were all found to be associated with tumorigenesis of a variety of cancers. Multiple polyadenylation sites of this gene have been reported. [provided by RefSeq, Jul 2008]"
chgb = "This gene encodes a tyrosine-sulfated secretory protein abundant in peptidergic endocrine cells and neurons. This protein may serve as a precursor for regulatory peptides. [provided by RefSeq, Jan 2009]"
dnmt1a = "DNA (cytosine-5-)-methyltransferase 1 has a role in the establishment and regulation of tissue-specific patterns of methylated cytosine residues. Aberrant methylation patterns are associated with certain human tumors and developmental abnormalities. Two transcript variants encoding different isoforms have been found for this gene. [provided by RefSeq, Aug 2008]"
foxm1 = "The protein encoded by this gene is a transcriptional activator involved in cell proliferation. The encoded protein is phosphorylated in M phase and regulates the expression of several cell cycle genes, such as cyclin B1 and cyclin D1. Several transcript variants encoding different isoforms have been found for this gene. [provided by RefSeq, Jul 2011]"
ia2 = "The protein encoded by this gene is a member of the protein tyrosine phosphatase (PTP) family. PTPs are known to be signaling molecules that regulate a variety of cellular processes including cell growth, differentiation, mitotic cycle, and oncogenic transformation. This PTP possesses an extracellular region, a single transmembrane region, and a single catalytic domain, and thus represents a receptor-type PTP. This PTP was found to be an autoantigen that is reactive with insulin-dependent diabetes mellitus (IDDM) patient sera, and thus may be a potential target of autoimmunity in diabetes mellitus. Alternate splicing results in multiple transcript variants.[provided by RefSeq, Dec 2010]"
irs2 = "This gene encodes the insulin receptor substrate 2, a cytoplasmic signaling molecule that mediates effects of insulin, insulin-like growth factor 1, and other cytokines by acting as a molecular adaptor between diverse receptor tyrosine kinases and downstream effectors. The product of this gene is phosphorylated by the insulin receptor tyrosine kinase upon receptor stimulation, as well as by an interleukin 4 receptor-associated kinase in response to IL4 treatment. [provided by RefSeq, Jul 2008]"
mecp2 = "DNA methylation is the major modification of eukaryotic genomes and plays an essential role in mammalian development. Human proteins MECP2, MBD1, MBD2, MBD3, and MBD4 comprise a family of nuclear proteins related by the presence in each of a methyl-CpG binding domain (MBD). Each of these proteins, with the exception of MBD3, is capable of binding specifically to methylated DNA. MECP2, MBD1 and MBD2 can also repress transcription from methylated gene promoters. In contrast to other MBD family members, MECP2 is X-linked and subject to X inactivation. MECP2 is dispensible in stem cells, but is essential for embryonic development. MECP2 gene mutations are the cause of most cases of Rett syndrome, a progressive neurologic developmental disorder and one of the most common causes of mental retardation in females. [provided by RefSeq, Jul 2009]"
nfatc1 = "The product of this gene is a component of the nuclear factor of activated T cells DNA-binding transcription complex. This complex consists of at least two components: a preexisting cytosolic component that translocates to the nucleus upon T cell receptor (TCR) stimulation, and an inducible nuclear component. Proteins belonging to this family of transcription factors play a central role in inducible gene transcription during immune response. The product of this gene is an inducible nuclear component. It functions as a major molecular target for the immunosuppressive drugs such as cyclosporin A. Multiple alternatively spliced transcript variants encoding distinct isoforms have been identified for this gene. Different isoforms of this protein may regulate inducible expression of different cytokine genes. [provided by RefSeq, Jul 2013]"
slc30a8 = "The protein encoded by this gene is a zinc efflux transporter involved in the accumulation of zinc in intracellular vesicles. This gene is expressed at a high level only in the pancreas, particularly in islets of Langerhans. The encoded protein colocalizes with insulin in the secretory pathway granules of the insulin-secreting INS-1 cells. Allelic variants of this gene exist that confer susceptibility to diabetes mellitus, noninsulin-dependent (NIDDM). Several transcript variants encoding different isoforms have been found for this gene.[provided by RefSeq, Mar 2010]"
tnfa = "This gene encodes a multifunctional proinflammatory cytokine that belongs to the tumor necrosis factor (TNF) superfamily. This cytokine is mainly secreted by macrophages. It can bind to, and thus functions through its receptors TNFRSF1A/TNFR1 and TNFRSF1B/TNFBR. This cytokine is involved in the regulation of a wide spectrum of biological processes including cell proliferation, differentiation, apoptosis, lipid metabolism, and coagulation. This cytokine has been implicated in a variety of diseases, including autoimmune diseases, insulin resistance, and cancer. Knockout studies in mice also suggested the neuroprotective function of this cytokine. [provided by RefSeq, Jul 2008]"
f5 = [ccna2, ccnd2, cdk4, chgb, dnmt1a, foxm1, ia2, irs2, mecp2, nfatc1, slc30a8, tnfa]

#executed code
#final_steps([f2,f3,f4,f5])
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
#with open('pic_get_abstr5.txt','rb') as f:
#	abstr = pickle.load(f)
#print abstr
final = final_steps([f2,f3,f4,f5])
#print 'final steps done'
#print final
#with open('pic_get_words8.txt','wb') as fi2:
#	pickle.dump(final,fi2)
#print_pickle2('pic_get_words8.txt')
pretty_out(final)
#d = {'word':11.1,'other':2.5,'brynn':88,'errrrythang':992}
#print get_top(d,3)

