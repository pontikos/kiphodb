import sys
import os
import xlrd

def path(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'phosida.humoegf_parser':
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
		book = xlrd.open_workbook(path(ABSPATH,'Homosapiens_egf.xls'))
		sheet = book.sheet_by_index(0)
		headers = sheet.row_values(0)
	except:
		print "I/O File error. The input or the output files are not valid."
		exit()

	Before_AC = [x for x in xrange(0, sheet.nrows-1)]
	Before_Pos = [x for x in xrange(0, sheet.nrows-1)]
	Before_AC[0] = ""
	Before_Pos[0] = ""
	for n in xrange(1,188870):#sheet.nrows):
		lineContents = dict(zip(headers,sheet.row_values(n)))
		Before_AC[n] = lineContents['Accession']
		Before_Pos[n] = lineContents['Phosphosite(s)']
		
		if Before_AC[n-1] == lineContents['Accession'] and Before_Pos[n-1] == lineContents['Phosphosite(s)']:
			continue
		else:
			#Search http://www.expasy.org/cgi-bin/sprot-search-de website to get AC NO.
			handle = ExPASy.sprot_search_de("%22ipi+"+lineContents['Accession'].lower()+"%22+AND+organism%3Ahuman+reviewed%3Ayes")
			html_results = handle.read()
			acc = re.findall(r'a href="./(\w+)"', html_results) #Fetch accession number from swissprot
			if len(acc) == 0:
				print "Can't find reviewed protein "+lineContents['Accession']+" data in Human from swissprot\n"
				continue
			else:
				acc = acc[0].strip()

			#Get phosphosite and corresponding kinase motif
			phos_sites = lineContents['Phosphosite(s)'].strip().split(" ")
			motifs_index = []
			mark = []
			motifs = [x for x in xrange(0,len(phos_sites))]
			for r in xrange(0,len(phos_sites)):
				if lineContents['Kinase motif(s)'].find(phos_sites[r]) != -1:
					motifs_index.append(lineContents['Kinase motif(s)'].find(phos_sites[r]))
					mark.append(r)
				else:
					motifs[r] = ""
					
			for r in xrange(0,len(motifs_index)):
				if r != len(motifs_index)-1:
					motifs[mark[r]] = lineContents['Kinase motif(s)'][motifs_index[r]:motifs_index[r+1]-1].replace(phos_sites[mark[r]],"")[1:].strip()
				else:
					motifs[mark[r]] = lineContents['Kinase motif(s)'][motifs_index[r]:].replace(phos_sites[mark[r]],"")[1:].strip()

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
