
import sys
import os
if __name__ == 'phosphatases_kinases_uniprot':
	ABSPATH = os.path.abspath('phosphatase_parser')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))

sys.path.append(os.sep.join([ABSPATH, ".."]))
#Need to add this for models objects to work
sys.path.append(os.sep.join([ABSPATH, "..", ".."]))
# Import all necessary modules.
from uniprotxml import *

import xlrd
# Add to the sys path the path to the dbproject
import sys

#Need to add this for models objects to work

import re
from Bio.SwissProt import SProt
from Bio import File
from Bio import ExPASy
from dbproject.KiPhoDB import models


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
	except:
	    print "I/O File error. The input files is not valid."
	    exit()


	for n in xrange(1,sheet.nrows):
	    #Read the contents of the line.
	    lineContents = dict(zip(headers,sheet.row_values(n)))
	    accession=lineContents['Accession']

	    if  models.Protein.objects.filter(accession_number=accession):
	       
	            try:
	                all_results = ''           
	                results = ExPASy.get_sprot_raw(accession)
	            except Exception,e:
	                print "Swissprot entry",accession,"could not be retrieved"

	            all_results = all_results + results.read()
	            s_parser = SProt.RecordParser()
	            s_iterator = SProt.Iterator(File.StringHandle(all_results), s_parser)       

	            while 1:
	                cur_record = s_iterator.next()

	                if cur_record is None:
	                    break

	                print "description:",cur_record.annotation_update
			newProtein = models.Protein()
			newProtein.accession_number = accession
			newProtein.gene_name =cur_record.gene_name
			newProtein.protein_sequence =cur_record.sequence
			newProtein.cog = ""
			newProtein.updated = datetime.date.today() 
			if not models.Organism.objects.filter(organism_name =cur_record.organism):
	   		    newOrganism = models.Organism()		    
			    newOrganism.rganism_name =cur_record.organism
			    newOrganism.save()
			newProtein.organism_name = models.Organism.objects.get(organism_name=cur_record.organism)
			
			if cur_record.data_class == "Reviewed":
			    newProtein.reviewed = True
			else:
			    newProtein.reviewed = False

			newProtein.save()


if __name__ == '__main__':
	parse()







