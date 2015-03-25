import sys
import os
def PATH(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'pathway.nci_nature_pid.nci':
	ABSPATH = os.path.abspath(PATH('pathway','nci_nature_pid'))
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(PATH(ABSPATH, '..'))
#Need to add this for models objects to work
sys.path.append(PATH(ABSPATH, '..', '..'))
sys.path.append(PATH(ABSPATH, '..', '..','..'))

# Import all necessary modules.
import re
from uniprotxml import *
from Bio import ExPASy
from Bio import SwissProt
import time


SOURCE_ID = 'NCI-Nature curated'
source = Source()
source.source_id = SOURCE_ID
source.url = 'http://pid.nci.nih.gov/'
source.description = 'The Pathway Interaction Database is a highly-structured, curated collection of information about known biomolecular interactions and key cellular processes assembled into signaling pathways. It is a collaborative project between the US National Cancer Institute (NCI) and Nature Publishing Group (NPG), and is an open access online resource.'
source.save()


def parse():
	try:
		lines = file(PATH(ABSPATH,"uniprot.tab")).readlines()

	except Exception, e:
		print e
		exit()

	headers = ['ProteinAccession','PathwayNames','PathwayID']
	file_data = dict()

	for line in lines:
		path_comp = dict(zip(headers, [x.strip() for x in line.strip().split('\t')]))
		acc = path_comp['ProteinAccession']
		if acc in file_data:
			path_comp.update({'PathwayNames':file_data[acc]['PathwayNames']+"@"+path_comp['PathwayNames'],})
			path_comp.update({'PathwayID':file_data[acc]['PathwayID']+"@"+path_comp['PathwayID'],})
		file_data[acc] = path_comp

	#Relating pathway to reaction (if both kinase/phosphatase and substrate appear in the same pathway, record passway and the relationsip)
	for reac in Reaction.objects.all():
		print reac
		rki_pho = str(reac.ki_pho_accession_number_id)
		rsub = str(reac.substrate_accession_number_id)
		id = dict()
		if rki_pho in file_data:
			rki_pho_data = file_data[rki_pho]
			if rki_pho_data['PathwayNames'].find("@") != -1:
				pathwayNames_kipho = set(rki_pho_data['PathwayNames'].split("@"))           
			else:
				pathwayNames_kipho = set([rki_pho_data['PathwayNames']])
			id = dict(zip(rki_pho_data['PathwayNames'].split("@"), rki_pho_data['PathwayID'].split("@")))
		else:
			pathwayNames_kipho = set()


		if rsub in file_data:
			rsub_data = file_data[rsub]
			if rsub_data['PathwayNames'].find("@") != -1:
				pathwayNames_sub = set(rsub_data['PathwayNames'].split("@"))
			else:
				pathwayNames_sub = set([rsub_data['PathwayNames']])
		else:
			pathwayNames_sub = set()



		pathwayNames_comm = pathwayNames_kipho.intersection(pathwayNames_sub)
		#print pathwayNames_comm
		if pathwayNames_comm:
			print 'Pathway found', reac, pathwayNames_comm
			for path in pathwayNames_comm:
				print path
				path_stable_id = id[path]
				print path_stable_id
				path_descp = ""

				#Get organism information                
				try:
					time.sleep(2)
					handle = ExPASy.get_sprot_raw(rki_pho)
					record = SwissProt.read(handle)
				except:
					print "The record with accesion number: " + rki_pho + " was not found in Uniprot.\n"
					continue
				# Extract and store the name of the organism.
				newOrganism = Organism()
				newOrganism.rganism_name = record.organism[0:record.organism.find(" (")]
				newOrganism.save()
				print 'Added Organism' , record.organism[0:record.organism.find(" (")]
					
				# If the Pathway does not exist, add its Accession number to ID and set an internal ID
					#Add the new pathway to Pathway table
				newPathway = Pathway()
				newPathway.pathway_name = path
				newPathway.organism_name = Organism.objects.get(organism_name = record.organism[0:record.organism.find(" (")])
				newPathway.description = path_descp
				newPathway.reviewed = True
				newPathway.source = source
				newPathway.comments = ""
				newPathway.save()
				print 'Added pathway ' , newPathway.pathway_id, path

				newID = ID()
				newID.object_id = "PW%0.6d" % (newPathway.pathway_id)
				newID.external_id = path_stable_id
				newID.source = source
				newID.comments = ""
				newID.save()
				print 'Added ID ' , path_stable_id

			# If the relationship does not exist, add to the Relation_Pathway table
				newReaction_Pathway = Reaction_Pathway()
				newReaction_Pathway.reaction = reac
				newReaction_Pathway.pathway = newPathway
				newReaction_Pathway.reviewed = True
				newReaction_Pathway.source = source
				newReaction_Pathway.comments = ""
				newReaction_Pathway.save()
				print "Relate reaction "+rki_pho+" -> "+rsub+" to pathway "+path
		else:
			print 'No pathway in common found for', reac
			continue


if __name__ == '__main__':
	parse()
