import sys
import os

def PATH(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'phosida.ecoli_parser':
	ABSPATH = os.path.abspath('phosida')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(PATH(ABSPATH, '..'))
#Need to add this for models objects to work
sys.path.append(PATH(ABSPATH, '..', '..'))
from uniprotxml import *

print ABSPATH

SOURCE_ID = 'PHOSIDA'
source = Source()
source.source_id = SOURCE_ID
source.url = 'http://www.phosida.com/'
source.description = """
The PHOsphorylation SIte DAtabase allows retrieval of phosphorylation data of any protein of interest.
It lists phosphorylation sites associated with particular projects and proteomes or, alternatively, displays phosphorylation sites found for any protein or protein group of interest.
In addition, structural and evolutionary information on each phosphoprotein and phosphosite is integrated.
"""
source.save()


import xlrd
from Bio import ExPASy
from Bio import SwissProt
import re

def parse():
	try:
		book = xlrd.open_workbook(PATH(ABSPATH,'escherichia_coli.xls'))
		sheet = book.sheet_by_index(0)
		headers = sheet.row_values(0)
	except Exception, e:
		print e
		exit()

	Before = [x for x in xrange(0, sheet.nrows-1)]
	for n in xrange(1, sheet.nrows):
		lineContents = dict(zip(headers,sheet.row_values(n)))
		if lineContents['Gene name'] == "":
			Before[n-1] = Before[n-2]
			lineContents['Gene name'] = str(Before[n-1])
		else:
			Before[n-1] = lineContents['Gene name']

		#Search http://www.expasy.org/cgi-bin/sprot-search-de website to get AC NO.
		handle = ExPASy.sprot_search_de("gene_exact%3A"+lineContents['Gene name']+"+AND+reviewed%3Ayes+AND+organism%3Aescherichia+coli")
		html_results = handle.read()
		acc = re.findall(r'a href="./(\w+)"', html_results) #Fetch accession number from swissprot
		if len(acc) == 0:
			print "Can't find reviewed gene "+lineContents['Gene name']+" data in Escherichia coli from swissprot\n"
			continue
		else:
			acc = acc[0]
			
		aa = lineContents['Mod. AA'].strip()
		print n
		pos = int(lineContents['Position'])
		motifs = lineContents['Motif (eukaryotic kinase)'].strip()

		if not acc:
			continue

		try:
			ue = UniprotEntry(accession=acc)
			acc = ue.accession()
		except Exception, e:
			print 'Fetching uniprot record', acc, e
			continue
		ue.save(source=source)
	
		 # Add the phosphorylation site and its references.
		newSite = PhosphorylationSite()
		newSite.accession_number = Protein.objects.get(accession_number=acc)
		newSite.amino_acid = aa
		newSite.position = pos
		newSite.motif = motifs
		newSite.reviewed = True
		newSite.comments = ""
		newSite.phosphosite_id = '%s-%s-%s' % (acc, aa, pos)
		newSite.source = source
		newSite.save()

		print "Success in line "+str(n)+" ,protein( "+acc+" ).\n"
	print "Done"

if __name__ == '__main__':
	parse()

			

