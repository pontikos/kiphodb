import sys
import os


if __name__ == 'pathway.panther.panther_parser':
	ABSPATH = os.path.abspath('pathway')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
def path(*args):
	return os.sep.join([str(x) for x in args])
sys.path.append(path(ABSPATH, '..'))
#Need to add this for models objects to work
sys.path.append(path(ABSPATH, '..', '..'))
sys.path.append(path(ABSPATH, '..', '..','..'))

import urllib2
from browser import Browser
from uniprotxml import *
import re
from Bio import ExPASy
from Bio import SwissProt
import time

SOURCE_ID = 'PANTHER'
source = Source()
source.source_id = SOURCE_ID
source.url = 'http://www.pantherdb.org/'
source.description = 'The PANTHER (Protein ANalysis THrough Evolutionary Relationships) Classification System is a unique resource that classifies genes by their functions, using published scientific experimental evidence and evolutionary relationships to predict function even in the absence of direct experimental evidence.'
source.save()


def parse():
	try:
		inputFile = open(path(ABSPATH,'SequenceAssociationPathway2.5.txt'))
	except:
		print "I/O File error. The input or the output files are not valid."
		exit()

	lines = inputFile.readlines()
	headers = ['Pathway accession','Pathway name','Pathway component accession',
			  'Pathway component name','UniProt ID','Protein definition',
			  'Confidence code','Evidence','Evidence type','PANTHER subfamily ID'
			  'PANTHER subfamily name']
	reac_all = Reaction.objects.all()


  	#Relating pathway to reaction (if both kinase/phosphatase and substrate appear in the same pathway, record passway and the relationsip)

	for k in xrange(0,Reaction.objects.count()):
		reac = reac_all[k]
		print reac
		ki_pho_path = []
		ki_pho_path_name = []
		sub_path = []
		sub_path_name = []
		for line in lines:
			path_comp = dict(zip(headers, [x.strip() for x in line.strip().split('\t')]))
			if path_comp['UniProt ID'].strip() == str(reac.ki_pho_accession_number)or path_comp['UniProt ID'].strip() == str(reac.substrate_accession_number):
				if len(ki_pho_path) == 0 and path_comp['UniProt ID'].strip() == str(reac.ki_pho_accession_number):
					ki_pho_path.append(path_comp['Pathway accession'].strip())
					ki_pho_path_name.append(path_comp['Pathway name'].strip())
					continue
				if len(sub_path) == 0 and path_comp['UniProt ID'].strip() == str(reac.substrate_accession_number):
					sub_path.append(path_comp['Pathway accession'].strip())
					sub_path_name.append(path_comp['Pathway name'].strip())
					continue
				if path_comp['UniProt ID'].strip() == str(reac.ki_pho_accession_number):
					for m in xrange(0, len(ki_pho_path)):
						if ki_pho_path[m] == path_comp['Pathway accession'].strip():
							break
						elif m == len(ki_pho_path)-1:
							ki_pho_path.append(path_comp['Pathway accession'].strip())
							ki_pho_path_name.append(path_comp['Pathway name'].strip())
				else:
					for m in xrange(0, len(sub_path)):
						if sub_path[m] == path_comp['Pathway accession'].strip():
							break
						elif m == len(ki_pho_path)-1:
							sub_path.append(path_comp['Pathway accession'].strip())
							sub_path_name.append(path_comp['Pathway name'].strip())

		if len(sub_path) == 0:
			print "Can't find pathways relating to substrate "+str(reac.substrate_accession_number)
			continue
		if len(ki_pho_path) == 0:
			print "Can't find pathways relating to catalyst "+str(reac.ki_pho_accession_number)
			continue

		r = 0
		for n in xrange(0,len((ki_pho_path))):
			for p in xrange(0,len(sub_path)):
				if sub_path[p] == ki_pho_path[n]:
					r = 1
					# Fetch pathway description from PANTHER
					pathway_url = "/pathway/pathDetail.do?clsAccession="+ki_pho_path[n]
					br = Browser('www.pantherdb.org')
					dom = br.get_page_dom(pathway_url.replace(' ','%20'))
					if len(dom.findAll('td',bgcolor="#E9EDF2")) != 0:
						path_descp = str(dom.findAll('td',bgcolor="#E9EDF2")[0])[22:].replace("</td>","").strip()
					else:
						path_descp = ""
						
					#Get organism information                
					try:
						time.sleep(2)
						handle = ExPASy.get_sprot_raw(reac.ki_pho_accession_number)
						record = SwissProt.read(handle)
					except:
						outputFile.write("The record with accesion number: " + reac.ki_pho_accession_number + " was not found in Uniprot.\n")
						continue
				  
				# Extract and store the name of the organism.
					newOrganism = Organism()
					newOrganism.rganism_name = record.organism[0:record.organism.find(" (")]
					newOrganism.save()

				# If the Pathway does not exist, add its Accession number to ID and set an internal ID					
					#Add the new pathway to Pathway table
					newPathway = Pathway()
					newPathway.pathway_name = ki_pho_path_name[n]
					newPathway.organism_name = Organism.objects.get(organism_name = record.organism[0:record.organism.find(" (")])
					newPathway.description = path_descp
					newPathway.reviewed = True
					newPathway.source = source
					newPathway.comments = ""
					newPathway.save()

					newID = ID()
					newID.object_id = 'PW%0.6d' % int(newPathway.pathway_id)
					newID.external_id = ki_pho_path[n]
					newID.source = source
					newID.comments = ""
					newID.save()
					print "added pathway "+ki_pho_path[n]+" to Pathway table"

				# If the relationship does not exist, add to the Relation_Pathway table          
					newReaction_Pathway = Reaction_Pathway()
					newReaction_Pathway.reaction = reac
					newReaction_Pathway.pathway = newPathway
					newReaction_Pathway.reviewed = True
					newReaction_Pathway.comments = ""
					newReaction_Pathway.source = source
					newReaction_Pathway.save()
					print "Relate reaction "+str(reac.ki_pho_accession_number)+" -> "+str(reac.substrate_accession_number)+" to pathway "+ki_pho_path[n]

				if n == len(ki_pho_path)-1 and p == len(sub_path)-1 and r == 0:
					print "No pathway in common"
					
	print "Done!"
	

if __name__ == '__main__':
	parse()
