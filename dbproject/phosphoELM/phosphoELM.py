import sys
import os
def PATH(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'phosphoELM.phosphoELM':
	ABSPATH = os.path.abspath('phosphoELM')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(PATH(ABSPATH, '..'))
#Need to add this for models objects to work
sys.path.append(PATH(ABSPATH, '..', '..'))
# Import all necessary modules.
from uniprotxml import *

SOURCE_ID = 'phosphoELM'
source = Source()
source.source_id = SOURCE_ID
source.url = 'http://phospho.elm.eu.org/'
source.description = 'Phospho.ELM is a database of experimentally verified phosphorylation sites in eukaryotic proteins.'
source.save()

def parse():
	# Open the input and output files and read all lines of the input file. If an exception occurs, issue an error message and exit.
	try:
		lines = file(PATH(ABSPATH,'phosphoELM_1208'), 'r').readlines()
		headers = lines[0].strip().split('\t')
	except Exception, e:
		print "I/O File error. The input is not valid."
		print e
		exit()	

	# The following loop is executed for every line of the input file.
	for l in lines[1:]:
		# Analyse the contents of this line.
		lineContents = dict(zip(headers, [x.strip() for x in l.strip().split('\t')]))
		acc = lineContents['acc']
		seq = lineContents['sequence']
		pos = lineContents['position']
		aa = lineContents['code']
		pubmed = lineContents['pmids']

		try:
			prot = UniprotEntry(accession=acc)
		except Exception, e:
			print e
			continue
		prot.save(substrate=True, source=source)
		print 'Saved', acc, prot.accession()
		acc = prot.accession()

		newSite = PhosphorylationSite()
		newSite.accession_number = Protein.objects.get(accession_number=acc)
		newSite.amino_acid = aa
		newSite.position = pos
		newSite.motif = seq[int(pos)-6:int(pos)-1] + seq[int(pos)-1].lower() + seq[int(pos):int(pos)+5]
		newSite.site_id = '%s-%s-%s' % (newSite.accession_number, newSite.amino_acid, newSite.position)
		newSite.reviewed = True
		newSite.source = source
		newSite.save()

		for pubmedid in pubmed.split(';'):
			if not pubmedid.isdigit() or not pubmedid:
				continue
			Reference(reference_id=pubmedid).save(object_id=newSite.site_id)

if __name__ == '__main__':
	parse()



