import sys
import os
def PATH(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'reaction.networKIN.networKIN':
	ABSPATH = os.path.abspath(PATH('reaction', 'networKIN'))
elif __name__ == 'networKIN.networKIN':
	ABSPATH = os.path.abspath('networKIN')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))

sys.path.append(PATH(ABSPATH, '..'))
#Need to add this for models objects to work
sys.path.append(PATH(ABSPATH, '..', '..'))
sys.path.append(PATH(ABSPATH, '..', '..', '..'))

from uniprotxml import *
import time

SOURCE_ID = 'networKIN'
source = Source()
source.source_id = SOURCE_ID
source.url = 'http://networkin.info/'
source.description = 'NetworKIN is a method for predicting in vivo kinase-substrate relationships, that augments consensus motifs with context for kinases and phosphoproteins.'
source.save()


def parse():
	lines = file(PATH(ABSPATH,'networKIN.tsv'), 'r').readlines()
	headers = lines[0].strip().split('\t')
	b=Browser('www.uniprot.org')
	for l in lines[1:]:
		record = dict(zip(headers, [x.strip() for x in l.strip().split('\t')]))
		substrate_accession_number = record['pELM_id']
		kinase_name = record['description_kinase']
		kinase_gene = record['genesymbol_kinase']
		if not kinase_gene:
			continue
		kinase_ensembl = record['ensemblID_kinase']
		predictor = record['predictor']
		motif_score = record['motif_score']
		context_score = record['context_score']
		#we want to get the uniprot record of the kinase
		#find organism name of substrate so we do a better search
		q = Protein.objects.filter(accession_number=substrate_accession_number)
		if (len(q) > 0):
			psub = q[0]
		else:
			continue
		#use the kinase gene code
		q = Protein.objects.filter(gene_accession_number=kinase_gene, organism_name=Organism(psub.organism_name))
		if (len(q) > 0):
			print 'Skipping', q
			continue
		else:
			print 'Fetching', kinase_gene, psub.organism_name
		#query = 'gene:%s AND organism:"%s" AND name:"%s"' % (kinase_gene, psub.organism_name, kinase_name)
		query = 'gene_exact:%s AND organism:"%s" AND reviewed:yes AND fragment:no' % (kinase_gene, psub.organism_name)
		dom=b.get_page_dom('/uniprot/', params={'query':query, 'force':'yes', 'format':'xml',})
		time.sleep(1)
		#uniprot data
		if not dom.entry:
			print 'Nothing found', kinase_gene, psub.organism_name
			continue
		uniprot_kinase = UniprotEntry(dom=dom.entry)
		uniprot_kinase_name = uniprot_kinase.name()
		print 'Accession', uniprot_kinase.accession()
		uniprot_kinase_name = uniprot_kinase_name.replace(',','').lower()
		kinase_name = kinase_name.replace(',','').lower()
		print uniprot_kinase_name.lower()
		print kinase_name.lower()
		print
		uniprot_kinase.save(reviewed=True, substrate=False, protein_type='K', source=source, comment=uniprot_kinase.comment('function'))

		reaction = Reaction()
		reaction.ki_pho_accession_number = Protein(uniprot_kinase.accession())
		reaction.substrate_accession_number = Protein(substrate_accession_number)
		#networKIN predicts kinases so phosphorylation
		reaction.reaction_type = 'P'
		reaction.reaction_evidence = 'S'
		reaction.reaction_effect = 'A'
		reaction.reaction_score = context_score
		reaction.source = source
		reaction.save()
		#ObjectId_Source(object_id='RC%0.6d'%reaction.reaction_id, source=source).save()		

if __name__ == '__main__':
	parse()



