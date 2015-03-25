import sys
import os
import xlrd

def path(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'phosida.musphoini2_parser':
	ABSPATH = os.path.abspath('phosida')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(path(ABSPATH, '..'))
#Need to add this for models objects to work
sys.path.append(path(ABSPATH, '..', '..'))

from uniprotxml import *
from Bio import ExPASy
from Bio import SwissProt

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
		sheet2 = book.sheet_by_index(1)
		headers = sheet2.row_values(0)
		print headers
	except:
		print "I/O File error. The input is not valid."
		exit()

	for n in xrange(1, sheet2.nrows):
		lineContents = dict(zip(headers,sheet2.row_values(n)))
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
		if not Protein.objects.filter(accession_number=acc):
			try:
				ue = UniprotEntry(acc)
				acc = ue.accession()
			except Exception, e:
				print 'Fetching uniprot record', acc, e
				continue
			try:
				ue.save()
			except Exception, e:
				print 'Saving uniprotentry', acc, e
				continue
		else:
			print 'Protein', acc, 'already in database'
		# Add the phosphorylation site and its references.
		if not PhosphorylationSite.objects.filter(accession_number=acc, position=pos):
			newSite = PhosphorylationSite()
			newSite.site_id = 'PS%0.6d' % len(PhosphorylationSite.objects.all())
			newSite.accession_number = Protein.objects.get(accession_number=acc)
			newSite.amino_acid = aa
			newSite.position = pos
			newSite.motif = motif
			newSite.reviewed = True
			newSite.comments = ""
			newSite.source = source
			try:
				newSite.save()
			except Exception, e:
				print 'Saving site', e

		print "Success in line",str(n),"protein",acc


if __name__ == '__main__':
	parse()

