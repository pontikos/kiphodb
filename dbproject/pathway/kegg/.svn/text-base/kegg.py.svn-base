import sys
import os
def path(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'pathway.kegg.kegg':
	ABSPATH = os.path.abspath('pathway')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(path(ABSPATH, '..'))
#Need to add this for models objects to work
sys.path.append(path(ABSPATH, '..', '..'))
sys.path.append(path(ABSPATH, '..', '..','..'))

from uniprotxml import *
from Bio import ExPASy
from Bio import SwissProt
import urllib
import time
import re

SOURCE_ID = 'KEGG Pathway'
SOURCE = Source()
SOURCE.source_id = SOURCE_ID
SOURCE.url = 'http://www.genome.ad.jp/kegg/pathway.html'
SOURCE.description = 'KEGG PATHWAY is a collection of manually drawn pathway maps representing our knowledge on the molecular interaction and reaction networks.'
SOURCE.save()


def parse():
	#Relating pathway to reaction (if both kinase/phosphatase and substrate appear in the same pathway, record passway and the relationsip)
	for reac in Reaction.objects.all():
		print 'RC%0.6d' % int(reac.reaction_id)
		#Get kinase/phosphatase's KEGG ID         
		try:
			time.sleep(2)
			handle_kipho = ExPASy.get_sprot_raw(reac.ki_pho_accession_number)
			record_kipho = SwissProt.read(handle_kipho)
		except:
			print "The record with accession number:",str(reac.ki_pho_accession_number),"was not found in Uniprot."
			continue
		
		r = 0
		for i in xrange(0,len(record_kipho.cross_references)):
			if record_kipho.cross_references[i][0] == "KEGG":
				kipho_kegg_gene = record_kipho.cross_references[i][1]
				r = 1
				break
		if r == 0:  # If no related KEGG ID
			print "No related KEGG information for",str(reac.ki_pho_accession_number)
			continue

		#Get substrate's KEGG ID    
		try:
			time.sleep(2)
			handle_sub = ExPASy.get_sprot_raw(reac.substrate_accession_number)
			record_sub = SwissProt.read(handle_sub)
		except:
			print "The record with accesion number: " + str(reac.substrate_accession_number) + " was not found in Uniprot.\n"
			continue
			
		r = 0
		for i in xrange(0,len(record_sub.cross_references)):
			if record_sub.cross_references[i][0] == "KEGG":
				sub_kegg_gene = record_sub.cross_references[i][1]
				r = 1
				break
		if r == 0:   # If no related KEGG ID
			print "No related KEGG information for "+str(reac.substrate_accession_number)
			continue
		
		
		# Fetch kinase/phosphatase's KEGG pathway ID
		kipho_kegg_gene_url = urllib.urlopen("http://www.genome.jp/dbget-bin/www_bget?"+kipho_kegg_gene).read()
		kipho_path_id = re.findall('PATH:\s<a\shref="\/dbget-bin\/show_pathway\?\w+\d+\+\d+">\w+\d+',kipho_kegg_gene_url)

	   # Fetch substrate's KEGG pathway ID
		sub_kegg_gene_url = urllib.urlopen("http://www.genome.jp/dbget-bin/www_bget?"+sub_kegg_gene).read()
		sub_path_id = re.findall('PATH:\s<a\shref="\/dbget-bin\/show_pathway\?\w+\d+\+\d+">\w+\d+',sub_kegg_gene_url)
		
		if len(kipho_path_id) == 0:
			print "No related KEGG pathway information for "+str(reac.ki_pho_accession_number)
			continue
		if len(sub_path_id) == 0:
			print "No related KEGG pathway information for "+str(reac.substrate_accession_number)
			continue
		
		kipho_path_id = [kipho_path_id[j][kipho_path_id[j].find(">")+1:] for j in xrange(0,len(kipho_path_id))]
		sub_path_id = [sub_path_id[j][sub_path_id[j].find(">")+1:] for j in xrange(0,len(sub_path_id))]

		r = 0
		#Find if the relationship of this reaction and certain pathway exists
		for m in xrange(0, len(kipho_path_id)):
			for n in xrange(0, len(sub_path_id)):
				if kipho_path_id[m] == sub_path_id[n]:
					r = 1
					path_html = urllib.urlopen("http://www.genome.jp/dbget-bin/www_bget?pathway+"+kipho_path_id[m].strip()).read()
					if path_html.find('<tr><th class="th31" align="left" valign="top" style="border-color:#000; border-width: 1px 0px 0px 1px; border-style: solid">Name</th>\n<td class="td31" style="border-color:#000; border-width: 1px 1px 0px 1px; border-style: solid"><table width="600" border="0" cellspacing="0" cellpadding="0"><tr><td align="left">') != -1:
						path_name = path_html.split('<tr><th class="th31" align="left" valign="top" style="border-color:#000; border-width: 1px 0px 0px 1px; border-style: solid">Name</th>\n<td class="td31" style="border-color:#000; border-width: 1px 1px 0px 1px; border-style: solid"><table width="600" border="0" cellspacing="0" cellpadding="0"><tr><td align="left">')[1].strip()
						path_name = path_name[0:path_name.find("<")].strip()
						if path_name.find("-") != -1:
						    path_name = path_name[0:path_name.find("-")].strip()
						print path_name
					else:
						path_name = ""
					if  path_html.find('<tr><th class="th30" align="left" valign="top" style="border-color:#000; border-width: 1px 0px 0px 1px; border-style: solid">Description</th>\n<td class="td30" style="border-color:#000; border-width: 1px 1px 0px 1px; border-style: solid"><table width="600" border="0" cellspacing="0" cellpadding="0"><tr><td align="left">') != -1:
						path_descp = path_html.split('<tr><th class="th30" align="left" valign="top" style="border-color:#000; border-width: 1px 0px 0px 1px; border-style: solid">Description</th>\n<td class="td30" style="border-color:#000; border-width: 1px 1px 0px 1px; border-style: solid"><table width="600" border="0" cellspacing="0" cellpadding="0"><tr><td align="left">')[1].strip()
						path_descp = path_descp[0:path_descp.find("<")].strip()
					else:
						path_descp = ""

					organism = record_kipho.organism[0:record_kipho.organism.find(" (")]

					# Extract and store the name of the organism.
					newOrganism = Organism()
					newOrganism.organism_name = organism
					newOrganism.save()                

					#Add the new pathway to Pathway table
					newPathway = Pathway()
					newPathway.pathway_name = path_name
					newPathway.organism_name = newOrganism
					newPathway.description = path_descp
					newPathway.reviewed = True
					newPathway.comments = ""
					newPathway.source = SOURCE
					newPathway.save()

					newID = ID()
					newID.object_id = 'PW%0.6d' % int(newPathway.pathway_id)
					newID.external_id = sub_path_id[n]
					newID.source = SOURCE
					newID.comments = ""
					newID.save()
					print "Added pathway",sub_path_id[n],"to Pathway table"

					newReaction_Pathway = Reaction_Pathway()
					newReaction_Pathway.reaction = reac
					newReaction_Pathway.pathway = newPathway
					newReaction_Pathway.reviewed = True
					newReaction_Pathway.comments = ""
					newReaction_Pathway.source = SOURCE
					newReaction_Pathway.save()
					print "Relate reaction",str(reac.ki_pho_accession_number),"->",str(reac.substrate_accession_number),"to pathway ",sub_path_id[n]

				if m == len(kipho_path_id)-1 and n == len(sub_path_id)-1 and r == 0:
					print "No pathway in common"

	print "Done!"
						
		
if __name__ == '__main__':
	parse()

