import xlrd

import sys
import os
def path(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'phosida.musphoini_parser':
	ABSPATH = os.path.abspath('phosida')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(path(ABSPATH, '..'))
#Need to add this for models objects to work
sys.path.append(path(ABSPATH, '..', '..'))

# Import all necessary modules.
from uniprotxml import *
from Bio import ExPASy
from Bio import SwissProt
import re


def parse():
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

	try:
		book = xlrd.open_workbook(path(ABSPATH,'Musmusculus_phosphataseinhibition.xls'))
		sheet5 = book.sheet_by_index(5)
		headers = sheet5.row_values(0)
	except:
		print "I/O File error. The input or the output files are not valid."
		exit()

	for n in xrange(1, sheet5.nrows):
		lineContents = dict(zip(headers,sheet5.row_values(n)))

		#Search http://www.expasy.org/cgi-bin/sprot-search-de website to get AC NO.
		handle = ExPASy.sprot_search_de("gene_exact:"+lineContents['Gene symbol'].strip()+"%20AND%20organism:Mus%20musculus%20reviewed:yes")
		html_results = handle.read()
		acc = re.findall(r'a href="./(\w+)"', html_results) #Fetch accession number from swissprot
		if len(acc) == 0:
			print "Can't find reviewed gene "+lineContents['Gene symbol']+" data in Mus musculus from swissprot"
			continue
		else:
			acc = acc[0].strip()

					#Get phosphosite and corresponding kinase motif
		phos_sites = lineContents['Integrated Phosphosites'].split(", ")
		motifs_index = []
		mark = []
		motifs = [x for x in xrange(0,len(phos_sites))]
		for r in xrange(0,len(phos_sites)):
			if lineContents['Kinase Motif(s)'].find(phos_sites[r]) != -1:
				motifs_index.append(lineContents['Kinase Motif(s)'].find(phos_sites[r]))
				mark.append(r)
			else:
				motifs[r] = ""

		for r in xrange(0,len(motifs_index)):
			if r != len(motifs_index)-1:
				motifs[mark[r]] = lineContents['Kinase Motif(s)'][motifs_index[r]:motifs_index[r+1]-1].replace(phos_sites[mark[r]],"")[1:].strip()
			else:
				motifs[mark[r]] = lineContents['Kinase Motif(s)'][motifs_index[r]:].replace(phos_sites[mark[r]],"")[1:].strip()

		if not acc:
			continue

		if not Protein.objects.filter(accession_number=acc):
			try:
				ue = UniprotEntry(acc)
				acc = ue.accession()
			except Exception, e:
				print 'Fetching uniprot record', acc, e
				continue
			ue.save()
		else:
			print 'Protein', acc, 'already in database'     

		# Add the phosphorylation site and its references.
		for i in range(0, len(phos_sites)):
			if not PhosphorylationSite.objects.filter(accession_number=acc, position=phos_sites[i][1:]):
				newSite = PhosphorylationSite()
				newSite.site_id = "PS" + '%0.6d' % len(PhosphorylationSite.objects.all())
				newSite.accession_number = Protein.objects.get(accession_number=acc)
				newSite.amino_acid = phos_sites[i][0].strip()
				newSite.position = phos_sites[i][1:].strip()
				newSite.motif = motifs[i]
				newSite.reviewed = True
				newSite.comments = ""
				newSite.source = source
				newSite.save()
		print "Success in line "+str(n)+" ,protein( "+acc+" ).\n"
	print "Done"

if __name__ == '__main__':
	parse()