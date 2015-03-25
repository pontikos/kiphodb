import sys
import os

def PATH(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'phosida.musphoini1_parser':
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

def parse():
	try:  
		book = xlrd.open_workbook(PATH(ABSPATH,'musmusculus_phosphataseinhibition.xls'))
		sheet1 = book.sheet_by_index(0)
		headers = [x.strip() for x in sheet1.row_values(0)]
		print headers
	except Exception, e:
		print e
		exit()

	for n in xrange(1, sheet1.nrows):
		lineContents = dict(zip(headers,sheet1.row_values(n)))
		acc = lineContents['Uniprot']
		acc = str(acc.split('-')[0])
		aa = lineContents['phosphoAA'][0].strip()
		pos = int(lineContents['phosphoAA'][1:].strip())
		#motif = str(lineContents['Sequence'].split(';')[0]).strip()
		#n = motif.find(aa)
		#motif = motif[:n]+motif[n].lower()+motif[n+1:]
		motif = ""
		if not acc:
			continue
		try:
			ue = UniprotEntry(accession=acc)
			acc = ue.accession()
		except Exception, e:
			print 'Fetching uniprot record', acc, e
			continue
		ue.save(source)

		# Add the phosphorylation site and its references.
		newSite = PhosphorylationSite()
		newSite.accession_number = Protein.objects.get(accession_number=acc)
		newSite.amino_acid = aa
		newSite.position = pos
		newSite.motif = motif
		newSite.reviewed = True
		newSite.comments = ""
		newSite.site_id = '%s-%s-%s' % (acc, aa, pos)
		newSite.source = source
		newSite.save()

		print "Success in line",str(n),"protein",acc

if __name__ == '__main__':
	parse()
