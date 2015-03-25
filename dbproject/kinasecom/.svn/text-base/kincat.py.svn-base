import sys
import os
if __name__ == 'kinasecom.kincat':
	ABSPATH = os.path.abspath('kinasecom')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))

sys.path.append(os.sep.join([ABSPATH, ".."]))
sys.path.append(os.sep.join([ABSPATH, "..", ".."]))

from uniprotxml import *
import xlrd
import re

#First create a new entry in the source table.
source = Source()
source.source_id = 'Kinase.com'
source.url = 'http://kinase.com/'
source.description = 'This site explores and stores all evolutionary,functional and diversity of Protein kinases'
source.save()

def parse():
	try:
	    book = xlrd.open_workbook(os.sep.join([ABSPATH, "Kincat_Hsap.08.02.xls"]))
	    sheet = book.sheet_by_index(0)
	    headers = sheet.row_values(0)
	except Exception,e :
	    print e
	    exit()

	for n in xrange(1,sheet.nrows):
	    #Read the contents of the line.
	    lineContents = dict(zip(headers,sheet.row_values(n)))
	    refseq_id=lineContents['Refseq protein']

	    #Remove the . which stands for version number
	    p=re.compile('\.\d*')
	    refseq_id=p.sub('',refseq_id)    
	    group=lineContents['Group']
	    family=lineContents['Family']
	    subfamily=lineContents['Subfamily']    

	    #Search for the refseq is in uniprot 
	    b=Browser('www.uniprot.org')
	    query = '%s AND reviewed:yes AND fragment:no' % (refseq_id)    
	    dom=b.get_page_dom('/uniprot/', params={'query':query, 'force':'yes', 'format':'xml',})

	    # Issue error if nothing is found.
	    if not dom.entry:
	    	print 'Nothing found', refseq_id, 'Human.'
		continue

	    kinase_uniprot = UniprotEntry(dom=dom.entry)
	    if not Protein.objects.filter(accession_number=kinase_uniprot.accession()):
	    	try:
	            final_comments = ''
	            if group:
	                final_comments += 'Group: ' + group + '. '
	            if family:
	                final_comments += 'Family: ' + family + '. '
	            if subfamily:
	                final_comments += 'Subfamily: ' + subfamily + '. '
	            kinase_uniprot.save(reviewed=True, substrate=False, protein_type='K', source=source, comment=final_comments)
		except Exception, e:
		    print e
	            continue
	    else:
	        print 'Already there'

if __name__ == '__main__':
	parse()







