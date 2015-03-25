import sys
import os
def PATH(*args):
	return os.sep.join([str(x) for x in args])
#if imported from update
if __name__ == 'update.reference':
	ABSPATH = os.path.abspath(PATH('.', 'orthologs'))
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(PATH(ABSPATH, '..'))
#Need to add this for models objects to work
sys.path.append(PATH(ABSPATH, '..', '..'))

from uniprotxml import *
from Bio import Entrez
from Bio import Medline

def update():
	# Iterate the Reference table and update the entries.
	for ref in Reference.objects.all():
		# If the entry is complete, continue with the next one.
		if ref.title and ref.authors and ref.location:
			continue

		# Try to fetch the PubMed entry for the specific reference.
		try:
			handle = Entrez.efetch(db="pubmed", id=ref.reference_id, rettype="medline", retmode="text")
			record = Medline.parse(handle)
			record = list(record)
		except Exception, e:
			print e
			print "The PubMed entry for the following record could not be fetched:", ref.reference_id
			continue

		# Get the data from the PubMed entry and check the integrity of the database entry.
		try:
			ref.title = record[0]['TI']
			ref.authors = '., '.join(record[0]['AU'])
			ref.location = record[0]['SO']
			ref.save()
			print 'Reference', ref
			print ref.title
		except Exception, e:
			print e
			print "The entry for the following record could not be updated:", ref.reference_id

if __name__ == '__main__':
	update()

