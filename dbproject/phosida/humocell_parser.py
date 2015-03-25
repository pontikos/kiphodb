import sys
import os

def PATH(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'phosida.humocell_parser':
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
		book = xlrd.open_workbook(PATH(ABSPATH,'homosapiens_cellcycle.xls'))
		sheet = book.sheet_by_index(0)
		headers = sheet.row_values(0)
	except Exception, e:
		print e
		exit()

	Before_AC = [x for x in xrange(0, sheet.nrows-1)]
	Before_Pos = [x for x in xrange(0, sheet.nrows-1)]
	Before_AC[0] = ""
	Before_Pos[0] = ""

	for n in xrange(1,8938):
		lineContents = dict(zip(headers,sheet.row_values(n)))
		Before_AC[n] = lineContents['Accession']
		Before_Pos[n] = lineContents['Phosphosite(s)']
		obj = re.search(r'^\w\d+',lineContents['Phosphosite(s)'].strip())
	  
		if Before_AC[n-1] == lineContents['Accession'] and Before_Pos[n-1] == lineContents['Phosphosite(s)']:
			continue
		elif obj == None:
			continue
		else:
			#Search http://www.expasy.org/cgi-bin/sprot-search-de website to get AC NO.
			handle = ExPASy.sprot_search_de("%22ipi+"+lineContents['Accession'].lower()+"%22+AND+organism%3Ahuman+reviewed%3Ayes")
			html_results = handle.read()
			acc = re.findall(r'a href="./(\w+)"', html_results) #Fetch accession number from swissprot
			if len(acc) == 0:
				print "Can't find reviewed protein",lineContents['Accession'],"data in Human from swissprot"
				continue
			else:
				acc = acc[0].strip()

			#Get phosphosite and corresponding kinase motif
			phos_sites = lineContents['Phosphosite(s)'].strip().split(" ")
			motifs_index = []
			mark = []
			motifs = [x for x in xrange(0,len(phos_sites))]
			for r in xrange(0,len(phos_sites)):
				if lineContents['Matching kinase motif(s)'].find(phos_sites[r]) != -1:
					motifs_index.append(lineContents['Matching kinase motif(s)'].find(phos_sites[r]))
					mark.append(r)
				else:
					motifs[r] = ""
					
			for r in xrange(0,len(motifs_index)):
				if r != len(motifs_index)-1:
					motifs[mark[r]] = lineContents['Matching kinase motif(s)'][motifs_index[r]:motifs_index[r+1]-1].replace(phos_sites[mark[r]],"")[1:].strip()
				else:
					motifs[mark[r]] = lineContents['Matching kinase motif(s)'][motifs_index[r]:].replace(phos_sites[mark[r]],"")[1:].strip()

			if not acc:
				continue

			try:
				ue = UniprotEntry(accession=acc)
				acc = ue.accession()
			except Exception, e:
				print 'Fetching uniprot record', acc, e
				continue
			ue.save(source=source)
							
				# Add the phosphorylation site 
			for i in range(0, len(phos_sites)):
				if not PhosphorylationSite.objects.filter(accession_number=acc, position=phos_sites[i][1:]):
					aa = phos_sites[i][0].strip()
					pos = int(phos_sites[i][1:].strip())
					newSite = PhosphorylationSite()
					newSite.accession_number = Protein.objects.get(accession_number=acc)
					newSite.amino_acid = aa
					newSite.position = pos
					newSite.motif = motifs[i]
					newSite.reviewed = True
					newSite.comments = ""
					newSite.source = source
					newSite.save()

			print "Success in line "+str(n)+" ,protein( "+acc+" ).\n"

	print "Done"           

if __name__ == '__main__':
	parse()

