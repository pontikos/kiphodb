import sys
import os
def PATH(*args):
	return os.sep.join([str(x) for x in args])

print __name__

if __name__ == 'reaction.reactome.reactome2':
	ABSPATH = os.path.abspath(PATH('reaction','reactome'))
elif __name__ == 'reactome.reactome2':
	ABSPATH = os.path.abspath(PATH('reactome'))
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))

print ABSPATH

sys.path.append(PATH(ABSPATH, '..'))
sys.path.append(PATH(ABSPATH, '..', '..'))
sys.path.append(PATH(ABSPATH, '..', '..','..'))

import urllib
import re
from Bio import ExPASy
from Bio import SwissProt
from uniprotxml import *
from browser import Browser

SOURCE_ID = 'Reactome'
SOURCE = Source()
SOURCE.source_id = SOURCE_ID
SOURCE.url = 'http://banon.cshl.edu/cgi-bin/frontpage?DB=gk_current'
SOURCE.description = 'The Reactome project is a collaboration among Cold Spring Harbor Laboratory, The European Bioinformatics Institute, and The Gene Ontology Consortium to develop a curated resource of core pathways and reactions in human biology.'
SOURCE.save()

def parse():
	FileList = ["reactome_catalyst_kinase_advanced_search_result.txt", "reactome_catalyst_phosphatase_advanced_search_result.txt"]

	for p in xrange(1,2):
		try:
			lines = file(PATH(ABSPATH, FileList[p]), 'r').readlines()
		except Exception, e:
			print e
			exit()

		reac_list = re.findall('\/cgi-bin\/eventbrowser\?DB=gk_current&ID=\d+&',str(lines))

		for i in xrange(0, len(reac_list)):

			br = Browser('www.reactome.org')
			dom = br.get_page_dom(reac_list[i])        
			reac_html = urllib.urlopen("http://www.reactome.org"+reac_list[i]).read()
			reac_name = [re.sub('<.*?>','',str(x).strip()) for x in dom.findAll('title')][0]
			reac_stab_id = [re.sub('<.*?>','',str(x).strip()) for x in dom.findAll('td', {'class':'stableIdentifier'})]
			if not reac_stab_id:
				reac_stab_id = reac_name
			else:
				reac_stab_id = reac_stab_id[0]
			try:
				reac_descp = [re.sub('<.*?>','',str(x).strip()) for x in dom.findAll('td', {'class':'summation'})][0]
				print reac_descp
			except:
				reac_descp = ''
				
			print reac_name
			print reac_stab_id
			
			# reaction html    
			if reac_html.find('<TD CLASS="input"><A HREF="') != -1:
				input = reac_html.split('<TD CLASS="input"><A HREF="')[1][0:reac_html.split('<TD CLASS="input"><A HREF="')[1].index('"')].strip()
			else:
				print "No input information for reaction "+reac_name
				continue
			if reac_html.find('Catalyst</A></TH><TD CLASS="catalystActivity"><A HREF="') != -1:
				cata = reac_html.split('Catalyst</A></TH><TD CLASS="catalystActivity"><A HREF="')[1][0:reac_html.split('Catalyst</A></TH><TD CLASS="catalystActivity"><A HREF="')[1].index('"')].strip()
			else:
				print "No catalyst information for reaction "+reac_name
				continue

			sub_acc = []
			cata_acc = []   
			#If reaction html contains uniprot accession
			# Get uniprot accession for catalyst if this html contains
			r1 = 0
			r2 = 0
			cut = reac_html.split('Catalyst</A></TH><TD CLASS="catalystActivity"><A HREF="'+cata+'">')[1][0:reac_html.split('Catalyst</A></TH><TD CLASS="catalystActivity"><A HREF="'+cata+'">')[1].index(">")+1].strip()
			if reac_html.split('Catalyst</A></TH><TD CLASS="catalystActivity"><A HREF="'+cata+'">')[1].find('<A HREF="http://www.uniprot.org/entry/') != -1 and reac_html.split('Catalyst</A></TH><TD CLASS="catalystActivity"><A HREF="'+cata+'">')[1].replace(cut,"").strip().index('<A HREF="http://www.uniprot.org/entry/') == 0:
				r1 = 1
				cata_acc.append(reac_html.split('Catalyst</A></TH><TD CLASS="catalystActivity"><A HREF="'+cata+'">')[1].replace(cut,"").strip().replace('<A HREF="http://www.uniprot.org/entry/',"").strip()[0:6])
			# Get uniprot accession for substrate if this html contains
			cut = reac_html.split('<TD CLASS="input"><A HREF="'+input+'">')[1][0:reac_html.split('<TD CLASS="input"><A HREF="'+input+'">')[1].index(">")+1].strip()
			if reac_html.split('<TD CLASS="input"><A HREF="'+input+'">')[1].find('<A HREF="http://www.uniprot.org/entry/') != -1 and reac_html.split('<TD CLASS="input"><A HREF="'+input+'">')[1].replace(cut,"").strip().index('<A HREF="http://www.uniprot.org/entry/') == 0:
				r2 = 1
				sub_acc.append(reac_html.split('<TD CLASS="input"><A HREF="'+input+'">')[1].replace(cut,"").strip().replace('<A HREF="http://www.uniprot.org/entry/',"").strip()[0:6])
			
			if r2 == 0: # No direct uniprot information
				input = input.replace(" ","20%")  # input url

				# input html    
				input_html = urllib.urlopen("http://www.reactome.org"+input).read()

				if input_html.find("Entities deduced on the basis of this entity") != -1:
					input_html = input_html.split("Entities deduced on the basis of this entity")[0]
					
				# Find uniprot accessions
				input_uniprot_url = re.findall('http:\/\/www\.uniprot\.org\/entry\/\w+',input_html)
				if len(input_uniprot_url) == 0:
					print "No UniProt information for input"
					continue
			   
				#Get substrate's uniprot accession  
				for j in xrange(0, len(input_uniprot_url)):  
					try:
						sub_record = UniprotEntry(accession=input_uniprot_url[j].replace("http://www.uniprot.org/entry/",""))
					except Exception, e:
						print 'Uniprot entry', e
						continue
									
					if sub_record.substrate():
						sub_acc.append(input_uniprot_url[j].replace("http://www.uniprot.org/entry/",""))

				if len(sub_acc) == 0:
					continue
				

			if r1 == 0: # No direct uniprot information
				cata = cata.replace(" ","20%")   #catalyst url        

				# catalyst html
				cata_html = urllib.urlopen("http://www.reactome.org"+cata).read()
				
				if cata_html.find("Entities deduced on the basis of this entity") != -1:
					cata_html = cata_html.split("Entities deduced on the basis of this entity")[0]
	   
				# Find uniprot accessions
				cata_uniprot_url = re.findall('http:\/\/www\.uniprot\.org\/entry\/\w+',cata_html)
				if len(cata_uniprot_url) == 0:
					print "No UniProt information for catalyst"
					continue
			  
				#Get catalyst's uniprot accession     
				for j in xrange(0, len(cata_uniprot_url)):  
					try:
						cata_record = UniprotEntry(accession=cata_uniprot_url[j].replace("http://www.uniprot.org/entry/",""))
					except Exception, e:
						print 'Uniprot entry', e
						continue
					
					if cata_record.name():
						uniprot_name = cata_record.name()
					else:
						print "No uniprot information for catalyst"
						continue
					if p == 0:
						if len(re.findall(r'[kK]inase',uniprot_name)) != 0 and len(re.findall(r'[iI]nhibitor',uniprot_name)) == 0:
							cata_acc.append(cata_uniprot_url[j].replace("http://www.uniprot.org/entry/",""))
					else:
						if len(re.findall(r'[Pp]hosphatase',uniprot_name)) != 0:
							cata_acc.append(cata_uniprot_url[j].replace("http://www.uniprot.org/entry/",""))
					
				if len(cata_acc) == 0:
				   continue

			try:
				reac_descp = [re.sub('<.*?>','',str(x).strip()) for x in dom.findAll('td', {'class':'summation'})][0]
				print reac_descp
			except:
				reac_descp = ''

			print cata_acc
			print sub_acc
		   
			for m in xrange(0, len(sub_acc)):

				if ID.objects.filter(external_id = sub_acc[m], source=Source("UniProt")):
					sub_acc[m] = ID.objects.get(external_id = sub_acc[m], source=Source("UniProt")).object_id
					print sub_acc[m]            
				# If the substrate does not exist, add it along with the organism, its GO terms,
				# its Domains and its References.
				if not Protein.objects.filter(accession_number=sub_acc[m]):
					# Fetch the record from Swissprot.
					try:
						#be aware that acc might be one of many accession numbers
						#for the swissprot entry, so it's not safe to use acc
						#for retrieving the record from the db
						prot = UniprotEntry(accession=sub_acc[m])
						acc = prot.accession()
					except Exception, e:
						print 'Uniprot entry', e
						continue
					prot.save(substrate=True, source=SOURCE)
					print 'Saved', acc
				else:
					print 'Protein', sub_acc[m], 'already in database.'

				for n in xrange(0, len(cata_acc)):

					if ID.objects.filter(external_id = cata_acc[n], source = Source("UniProt")):
						cata_acc[n] = ID.objects.get(external_id = cata_acc[n], source = Source("UniProt")).object_id
						print cata_acc[n]
						
					# If the catalyst does not exist, add it along with the organism, its GO terms,
					# its Domains and its References.
					if not Protein.objects.filter(accession_number=cata_acc[n]):
						# Fetch the record from Swissprot.
						try:
							#be aware that acc might be one of many accession numbers
							#for the swissprot entry, so it's not safe to use acc
							#for retrieving the record from the db
							prot = UniprotEntry(accession=cata_acc[n])
							acc = prot.accession()
						except Exception, e:
							print 'UniprotEntry entry', e
							continue
						prot.save(substrate=False, source=SOURCE)
						print 'Saved', prot.accession()
					else:
						print 'Protein', cata_acc[n], 'already in database.'

					#Added to reaction table
					if not Reaction.objects.filter(ki_pho_accession_number=cata_acc[n], substrate_accession_number=sub_acc[m]):
						reaction = Reaction()
						reaction.ki_pho_accession_number = Protein.objects.get(accession_number=cata_acc[n])
						reaction.substrate_accession_number = Protein.objects.get(accession_number=sub_acc[m])
						if p == 0:
							reaction.reaction_type = 'P'
						else:
							reaction.reaction_type = 'D'
						reaction.reaction_evidence = 'U'
						reaction.reaction_score = 1
						reaction.reaction_description = reac_descp
						reaction.reviewed = True
						reaction.updated = datetime.date.today()
						try:
							reaction.save()
							print 'Added reaction ' , reac_stab_id
						except Exception, e:
							print 'Reaction', e

						newID = ID()
						newID.object_id = 'RC%0.6d' %reaction.reaction_id
						newID.external_id = reac_stab_id
						newID.source = SOURCE
						newID.comments = ""
						try:
							newID.save()
							print 'Added ID ' , reac_stab_id,cata_acc[n],"->",sub_acc[m]
						except Exception, e:
							print 'ID', e
					else:
						exsit_id = 'RC%0.6d' %Reaction.objects.get(ki_pho_accession_number = cata_acc[n], substrate_accession_number = sub_acc[m]).reaction_id
						if not ID.objects.filter(object_id = exsit_id, external_id = reac_stab_id):
							newID = ID()
							newID.object_id = exsit_id
							newID.external_id = reac_stab_id
							newID.source = SOURCE
							newID.comments = ""
							try:
								newID.save()
								print 'Added ID ' , reac_stab_id,cata_acc[n],"->",sub_acc[m]
							except Exception, e:
								print 'ID', e
						else:
							print 'Reaction and ID', reac_stab_id, reac_stab_id,cata_acc[n],"->",sub_acc[m],'already in database.'
						
		print "File", FileList[p], "is finished."
	print "Done!"

if __name__ == '__main__':
	parse()

