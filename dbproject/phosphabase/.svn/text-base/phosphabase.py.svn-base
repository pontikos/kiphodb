import sys
import os
def path(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'phosphabase.phosphabase':
	ABSPATH = os.path.abspath('phosphabase')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(path(ABSPATH, '..'))
#Need to add this for models objects to work
sys.path.append(path(ABSPATH, '..', '..'))

from uniprotxml import *
import re

SOURCE_ID = 'PhosphaBase'
source = Source()
source.source_id = SOURCE_ID
source.url = 'http://www.bioinf.manchester.ac.uk/phosphabase/'
source.description = 'PhosphaBase (PhB) is a database of protein phosphatases and contains information about their protein sequences. This is essentially a sub-set of the Swiss-Prot/TrEMBL database, which is part of UniProt.'
source.save()

families = (
			'Protein tyrosine phosphatase',
			'Dual-specificity phosphatase',
			'Lipid phosphatase',
			'Serine/threonine phosphatase',
			'Histidine protein phosphatase',
			'Unclassified tyrosine phosphatase',
			'Unclassified ser/thr phosphatase')

#
def download():
	b = Browser('www.bioinf.manchester.ac.uk', debug=True)
	for family in families:
		params = {
			'search':'advanced',
			'option1':'',
			'geneprotein':'',
			'organism':'',
			'option2':family,
			'organism2':'',
			'function':'',
			'organism3':'',
			'tissue':'',
			'organism4':'',
			'geneSelect':'on',
			'proteinSelect':'on',
			'organismSelect':'on',
			'family':'on',
			'functionSelect':'on',
			'tissueSelect':'on',
			'interpro':'on',
			'pdb':'on',
			'intact':'on',
			'length':'on',
			'sequence':'on'}
		p = b.get_page('/cgi-bin/phosphabase/download.pl', post=params, headers={'Referer':'http://www.bioinf.manchester.ac.uk/cgi-bin/phosphabase/select.pl'})
		file(ABSPATH+'/phosphobase-%s.csv' % family.replace('/','').replace(' ','-'), 'w').write(p)

def parse():
	for family in families:
			lines = file(path(ABSPATH,'phosphobase-%s.csv' % family.replace('/','').replace(' ','-')), 'r').readlines()
			#Sptrembl!Gene!Name!Organism!Family!Function!Tissue!SeqLength!Sequence!InterPro!PDB!Interactions
			headers = [x.strip() for x  in lines[0].split('!')]
			for l in lines[1:]:
				record = dict(zip(headers, [x.strip() for x in l.split('!')]))
				accession = record['Sptrembl']
				try:
					ue = UniprotEntry(accession=accession)
				except Exception, e:
					print e
					continue
				ue.save(protein_type='P', source=source)
				print 'Success for protein,', ue.accession(), 'name:', ue.name()
				#print record['Name']
				#print record['InterPro']
				#print record['Organism']
				#print record['Gene']
				#print record['Sptrembl']
				#print record['Function']

if __name__ == '__main__':
	if '--download' in sys.argv:
		download()
	parse()

