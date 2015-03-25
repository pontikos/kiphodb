import sys
import os
if __name__ == 'phosphoELM.phosphoELM':
	ABSPATH = os.path.abspath('phosphoELM')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append("..")
#Need to add this for models objects to work
sys.path.append("../..")
# Import all necessary modules.
from uniprotxml import *
import sys
import os

if __name__ == 'kinasecom.disease_kinase':
	ABSPATH = os.path.abspath('disease_kinase')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(os.sep.join([ABSPATH, ".."]))
sys.path.append(os.sep.join([ABSPATH, "..", ".."]))

import xlrd
# Add to the sys path the path to the dbproject
import sys
#Need to add this for models objects to work
from uniprotxml import *
import re
#First create a new entry in the source table.

source = Source()
source.source_id = 'Kinase.com'
source.url = 'http://kinase.com/'
source.description = 'This site explores and stores all evolutionary,functional and diversity of Protein kinases'
source.save()

try:
    book = xlrd.open_workbook(os.sep.join([ABSPATH, "Table S2.xls"]))
    sheet = book.sheet_by_index(0)
    headers = sheet.row_values(0)
except Exception,e:
    print e
    exit()

def parse():
	for n in xrange(1,sheet.nrows):
	    #Read the contents of the line.
	    lineContents = dict(zip(headers,sheet.row_values(n)))
	    
	    #Get the Ensembl ids and the the Associated Disease
	    ensembl_id=lineContents['Ensembl']
	    disease=lineContents['Disease Association']
	    p=re.compile(',')
	    disease=p.split(disease,2)

	    if lineContents['Disease Association']:
	    #Search for the Ensembl id in uniprot 
	        if ensembl_id:
	            b=Browser('www.uniprot.org')
	            query = '%s AND reviewed:yes AND fragment:no' % (ensembl_id)
	            dom=b.get_page_dom('/uniprot/', params={'query':query, 'force':'yes', 'format':'xml',})

	            # Issue error if nothing is found.
	            if not dom.entry:
	                print 'Nothing found', ensembl_id
	                continue

	            kinase_uniprot = UniprotEntry(dom.entry)

	            print kinase_uniprot.accession(),disease
	            if not Protein.objects.filter(accession_number=kinase_uniprot.accession()):
	                try:
	                    final_comments='Disease Associated:  %s' % disease
	                    kinase_uniprot.save(reviewed=True, substrate=False, protein_type='K', source=source, comment=final_comments)
		        except Exception, e:
	                    continue
	            else:
	                print 'Protein', kinase_uniprot.accession(), 'already in database.'

if __name__ == '__main__':
	parse()        

    






