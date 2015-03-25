import sys
import os
#if imported from kinbase

def path(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'kinbase.kinbase':
	ABSPATH = os.path.abspath('kinbase')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(path(ABSPATH, '..'))
#Need to add this for models objects to work
sys.path.append(path(ABSPATH, '..', '..'))
from uniprotxml import *

import time
import re
from Bio import ExPASy

SOURCE_ID = 'kinBase'
source = Source()
source.source_id = SOURCE_ID
source.url = 'http://kinase.com/kinbase/FastaFiles/'
source.description = 'KinBase holds information on over 3000 protein kinase genes found in the genomes of human, and many other sequenced genomes.'
source.save()

#http://kinase.com/kinbase/FastaFiles/
#--------------------------------------------------
# from Bio import SwissProt
# b = Browser('kinase.com')
# dom = b.get_page_dom('/kinbase/FastaFiles/')
# for a in dom.findAll('a', href=re.compile('.*_kinase_protein.fasta')):
# 	if not os.path.isfile(a['href']):
# 		p = b.get_page('/kinbase/FastaFiles/'+a['href'])
# 		file(a['href'], 'w').write(p)
# 	handle = open(a['href'], 'rU') 
# 	for record in SeqIO.parse(handle, 'fasta'):
# 		print record.id
# 		continue
# 		#get complete record from swissprot if not already in database
# 		try:
# 			handle = ExPASy.get_sprot_raw(record.id)
# 			sprot = SwissProt.read(handle)
# 		except:
# 			print "The record with accession number %s was not found in Swissprot" % record.id
# 			continue
#-------------------------------------------------- 

filename_organism = {
	"Bakers_Yeast":"baker's+yeast",
	"Fruit_Fly":"fruit+fly",
	"Human":"human",
	"M.brevicollis":"Monosiga+brevicollis",
	"Mouse":"Mouse",
	"Nematode_worm":"Caenorhabditis+elegans",
	"Sea_Urchin":"Sea+Urchin",
	"Slime_mold":"Dictyostelium+discoideum",
	"Tetrahymena":"Tetrahymena",
}


def parse():
	for (filename, organism) in filename_organism.items():
		try:
			lines = file(path(ABSPATH,'%s_kinase_protein.fasta' % filename), 'r').readlines()
		except Exception, e:
			print "I/O File error. The input is not valid."
			print e
			exit()

		#Get the organism name from file name
		OrgName = filename.replace('_', '')
		for line in lines:
			obj2 = re.match(r'^>\w+',line)
			if obj2 == None:
				continue
			else:
				gene_name = line[1:line.find("_")]
				#Search http://www.expasy.org/cgi-bin/sprot-search-de website to get AC NO.
				handle = ExPASy.sprot_search_de("gene_exact%3A%22+"+gene_name+"%22+AND+organism%3A"+organism+"+reviewed%3Ayes")
				html_results = handle.read()
				acc = re.findall(r'a href="./(\w+)"', html_results) #Fetch accession number from swissprot
				if len(acc) == 0:
					print "Can't find reviewed gene", gene_name, "data in", OrgName, "from swissprot"
					continue
				else:
					acc = acc[0].strip()
				 # If the protein does not exist, add it along with the organism, its GO terms, its Domains and its References.
				if not Protein.objects.filter(accession_number=acc):
					print 'Protein', acc, 'already in db'
					continue
				else:
				 # Fetch the record from uniprot.
					try:
						time.sleep(2)
						prot = UniprotEntry(acc)
						#prot = SwissprotEntry(acc)
					except Exception, e:
						print 'Getting uniprotentry', e
						continue
					try:
						prot.save(source=source, protein_type='K')
					except Exception, e:
						print 'Saving uniprotentry', e
						continue
				print "Success for protein", acc

if __name__ == '__main__':
	parse()

         


