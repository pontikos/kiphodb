import sys
import os
def PATH(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'pathway.reactome.reactome':
	ABSPATH = os.path.abspath(PATH('pathway','reactome'))
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(PATH(ABSPATH, '..'))
#Need to add this for models objects to work
sys.path.append(PATH(ABSPATH, '..', '..'))
sys.path.append(PATH(ABSPATH, '..', '..','..'))


from uniprotxml import *
import urllib2
from browser import Browser
import re

SOURCE_ID = 'Reactome'
SOURCE = Source()
SOURCE.source_id = SOURCE_ID
SOURCE.url = 'http://banon.cshl.edu/cgi-bin/frontpage?DB=gk_current'
SOURCE.description = 'The Reactome project is a collaboration among Cold Spring Harbor Laboratory, The European Bioinformatics Institute, and The Gene Ontology Consortium to develop a curated resource of core pathways and reactions in human biology.'
SOURCE.save()

def parse():
	try:
		lines = file(PATH(ABSPATH,'curated_and_inferred_uniprot_2_pathways.txt'), 'r').readlines()
	except Exception, e:
		print e
		exit()

	headers = ['ProteinAccession','UniProtID','PathwayNames','ProteinUrl','Organism']
	file_data = dict()

	for line in lines:
		path_comp = dict(zip(headers, [x.strip() for x in line.strip().split('\t')]))
		acc = path_comp['UniProtID'].split(':')[-1]
		path_comp.update({'UniProtID':acc,})
		processes = [x.replace('IEA','').strip() for x in path_comp['PathwayNames'].split(':')[-1].split(';')]
		path_comp.update({'PathwayNames':processes,})
		file_data[acc] = path_comp

	#Relating pathway to reaction (if both kinase/phosphatase and substrate appear in the same pathway, record passway and the relationsip)
	for reac in Reaction.objects.all():
		rki_pho = str(reac.ki_pho_accession_number_id)
		rsub = str(reac.substrate_accession_number_id)
		pathwayNames_kipho = set([])
		pathwayNames_sub = set([])
		if rki_pho in file_data: 
			rki_pho_data = file_data[rki_pho]
			pathwayNames_kipho = set(rki_pho_data['PathwayNames'])
		else:
			print "No related pathway inforamtion for",rki_pho
		if rsub in file_data:
			rsub_data = file_data[rsub]
			pathwayNames_sub = set(rsub_data['PathwayNames'])
		else:
			print "No related pathway inforamtion for",rsub

		pathwayNames_comm = pathwayNames_kipho.intersection(pathwayNames_sub)

		if pathwayNames_comm:
			print 'Pathway found', reac, pathwayNames_comm
			for path in pathwayNames_comm:
				print path
				urlregex = re.compile('<A HREF="(.*?)">\s*%s\s*</A>' % path)
				page = urllib2.urlopen(rki_pho_data['ProteinUrl']).read()
				m = urlregex.search(page)
				if m:
					pathway_url = m.group(1)
				else:
					print page
					print 'urlregex not found'
					continue
				br = Browser('www.reactome.org')
				dom = br.get_page_dom(pathway_url.replace(' ','%20'))
				#<table class="Pathway" width="100%" cellspacing="0">
				if [re.sub('<.*?>','',str(x).strip()) for x in dom.findAll('td', {'class':'summation'})]:
					path_descp = [re.sub('<.*?>','',str(x).strip()) for x in dom.findAll('td', {'class':'summation'})][0]
				else:
					path_descp = ""
				#<TD CLASS="stableIdentifier" WIDTH="75%"><A HREF="control_panel_st_id?ST_ID=REACT_6900.5">REACT_6900.5</A></TD>
				if [re.sub('<.*?>','',str(x).strip()) for x in dom.findAll('td', {'class':'stableIdentifier'})]:
					path_stable_id = [re.sub('<.*?>','',str(x).strip()) for x in dom.findAll('td', {'class':'stableIdentifier'})][0]
				else:
					path_stable_id = path+"["+rki_pho_data['Organism']+"]"
				
				
				# Extract and store the name of the organism.
				newOrganism = Organism()
				newOrganism.rganism_name = rki_pho_data['Organism']
				newOrganism.save()
				print 'Added Organism' , rki_pho_data['Organism']

				#Add the new pathway to Pathway table
				newPathway = Pathway()
				newPathway.pathway_name = path
				newPathway.organism_name = Organism.objects.get(organism_name = rki_pho_data['Organism'])
				newPathway.description = path_descp
				newPathway.reviewed = True
				newPathway.source = SOURCE
				newPathway.comments = ""
				newPathway.save()
				print 'Added pathway ' , newPathway.pathway_id, path

				newID = ID()
				newID.object_id = "PW%0.6d" % newPathway.pathway_id
				newID.external_id = path_stable_id
				newID.source = SOURCE
				newID.comments = ""
				newID.save()
				print 'Added ID ' , path_stable_id
					
				# If the relationship does not exist, add to the Relation_Pathway table
				newReaction_Pathway = Reaction_Pathway()
				newReaction_Pathway.reaction = reac
				newReaction_Pathway.pathway = newPathway
				newReaction_Pathway.reviewed = True
				newReaction_Pathway.comments = ""
				newReaction_Pathway.source = SOURCE
				newReaction_Pathway.save()
				print "Relate reaction "+str(reac.ki_pho_accession_number)+" -> "+str(reac.substrate_accession_number)+" to pathway "+path
		else:
			print 'No pathway in common found for', reac
			print pathwayNames_kipho
			print pathwayNames_sub
			continue

if __name__ == '__main__':
	parse()

