import sys
import os
if __name__ == 'phosphatases_kinases_uniprot':
	ABSPATH = os.path.abspath('phosphatase_uniprot')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))

sys.path.append(os.sep.join([ABSPATH, ".."]))
#Need to add this for models objects to work
sys.path.append(os.sep.join([ABSPATH, "..", ".."]))

# Import all necessary modules.
from uniprotxml import *
import xlrd
# Add to the sys path the path to the dbproject
#Need to add this for models objects to work
from uniprotxml import *
import re

source = Source()
source.source_id = 'Uniprot'
source.url = 'http://www.Uniprot.org/'
source.description = 'Uniprot is the best source for manually curated Proteins of all types in all organisms'
source.save()

def parse():
	try:
		book = xlrd.open_workbook(os.sep.join([ABSPATH, "phosphatase.xls"]))
		sheet = book.sheet_by_index(0)
		headers = sheet.row_values(0)
	except Exception,e:
		print e
		exit()

	for n in xrange(1,sheet.nrows):
		#Read the contents of the line.
		lineContents = dict(zip(headers,sheet.row_values(n)))
		accession=lineContents['Accession']
		protein = UniprotEntry(accession=accession)
		protein.save(substrate=False,protein_type='P',source=source)
		print 'Saved', protein.accession()

if __name__ == '__main__':
	parse()




