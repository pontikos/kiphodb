import sys
import os

def PATH(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'phosida.bacil_parser':
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
		book = xlrd.open_workbook(PATH(ABSPATH, 'bacillus_subtilis.xls'))
		sheet = book.sheet_by_index(0)
		headers = sheet.row_values(0)
	except Exception, e:
		print e
		exit()


	for n in xrange(1, sheet.nrows):
		lineContents = dict(zip(headers,sheet.row_values(n)))

		#Search http://www.expasy.org/cgi-bin/sprot-search-de website to get AC NO.
		handle = ExPASy.sprot_search_de(lineContents['Accession']+"0")
		html_results = handle.read()
		acc = re.findall(r'a href="./(\w+)"', html_results) #Fetch accession number from swissprot
		if len(acc) == 0:
			print "Can't find reviewed protein "+lineContents['Accession']+" data in Bacillussubtilis from swissprot\n"
			continue
		else:
			acc = acc[0].strip()

		aa_pos_list = lineContents['Phosphosite(s)'].strip().split(" ")
		motifs_list = []
		for i in xrange(0, len(aa_pos_list)):
			q = lineContents['Kinase Motif(s)'].find(aa_pos_list[i])
			if i != len(aa_pos_list)-1:
				p = lineContents['Kinase Motif(s)'].find(aa_pos_list[i+1])
				motifs_list.append(lineContents['Kinase Motif(s)'][q:p].replace(aa_pos_list[i].strip(),"")[1:].strip())
			else:
				motifs_list.append(lineContents['Kinase Motif(s)'][q:].replace(aa_pos_list[i].strip(),"")[1:].strip())
		print aa_pos_list,motifs_list

		for j in xrange(0, len(aa_pos_list)):
			#Get phosphorylation sites and motifs
			aa = aa_pos_list[j][0].strip()
			pos = int(aa_pos_list[j][1:].strip())
			motifs = motifs_list[j]

			if not acc:
				continue

			if not Protein.objects.filter(accession_number=acc):
				try:
					ue = UniprotEntry(accession=acc)
					acc = ue.accession()
				except Exception, e:
					print 'Fetching uniprot record', acc, e
					continue
				ue.save(source=source)
			else:
				print 'Protein', acc, 'already in database'           

			# Add the phosphorylation site and its references.
			if not PhosphorylationSite.objects.filter(accession_number=acc, position=pos):
				newSite = PhosphorylationSite()
				newSite.accession_number = Protein.objects.get(accession_number=acc)
				newSite.amino_acid = aa
				newSite.position = pos
				newSite.motif = motifs
				newSite.reviewed = True
				newSite.comments = ""
				newSite.source = source
				newSite.site_id = '%s-%s-%s' % (acc, aa, pos)
				newSite.save()
			else:
				print 'Site', acc, pos, 'already in database'
		print "Success in line "+str(n)+" ,protein( "+acc+" ).\n"
	print "Done"

if __name__ == '__main__':
	parse()


