import sys
import os
def PATH(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'reaction.dbPTM2.dbPTM2':
	ABSPATH = os.path.abspath(PATH('reaction', 'dbPTM2'))
elif __name__ == 'dbPTM2.dbPTM2':
	ABSPATH = os.path.abspath('dbPTM2')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))

sys.path.append(PATH(ABSPATH, '..'))
#Need to add this for models objects to work
sys.path.append(PATH(ABSPATH, '..', '..'))
sys.path.append(PATH(ABSPATH, '..', '..', '..'))

from Bio import ExPASy
from Bio import Entrez
from Bio import Medline
from uniprotxml import *     
import re

#Source table
SOURCE_ID = 'dbPTM'
source = Source()
source.source_id = SOURCE_ID
source.url = 'http://dbptm.mbc.nctu.edu.tw/'
source.description = 'dbPTM was proposed to integrate experimentally verified PTMs from several databases, and to annotate the predicted PTMs on Swiss-Prot proteins.'
source.save()


def parse():
	#Open file  
	try:
		lines = file(PATH(ABSPATH,'dbPTM2.txt'), 'r').readlines()
	except Exception, e:
		print e
		exit()

	headers = ['ProteinEntry','Position','Type','References','Resource']
	ptm_types = ['Phosphothreonine','Phosphoserine','Phosphohistidine','Phosphocysteine','4-aspartylphosphate','Phosphotyrosine']

	file_data = dict()

	for line in lines:
		ptm_pro = dict(zip(headers, [x.strip() for x in line.strip().split('\t')]))
		ptm_pro['Type'] = ptm_pro['Type'].split("(")[0].strip()
		if ptm_pro['Type'] in ptm_types:
			print ptm_pro['ProteinEntry']
			print ptm_pro['Type']
			pro_entry = ptm_pro['ProteinEntry']
			position = ptm_pro['Position']

			#Use entry name to get accession number
			handle = ExPASy.sprot_search_de(pro_entry)
			html_results = handle.read()
			if re.findall("accession\s+number:\s+<strong>\w+",html_results):
				ac = re.findall("accession\s+number:\s+<strong>\w+",html_results)[0]
				ac = ac[ac.find(">")+1:].strip()
				print ac
			else:
				print "No uniprot information for", pro_entry
				continue
			
			try:
				#be aware that acc might be one of many accession numbers
				#for the Uniprot entry, so it's not safe to use acc
				#for retrieving the record from the db
				prot = UniprotEntry(accession=ac)
			except Exception, e:
				print 'Uniprot entry', e
				continue
			ptm_pro['Position'] = position+";"+prot.sequence()[int(position)-1]
			if ac in file_data:
				ptm_pro.update({'Position':file_data[ac]['Position']+"@"+ptm_pro['Position'],})
				ptm_pro.update({'Type':file_data[ac]['Type']+"@"+ptm_pro['Type'],})
				ptm_pro.update({'References':file_data[ac]['References']+"@"+ptm_pro['References'],})
				ptm_pro.update({'Resource':file_data[ac]['Resource']+"@"+ptm_pro['Resource'],})
			file_data[ac] = ptm_pro


	for pro in Protein.objects.all():
		print pro
		acc = pro.accession_number
		if acc in file_data:
			pro_data = file_data[acc]

			sites = pro_data['Position'].split("@")
			ref = pro_data['References'].split("@")
			for i in xrange(0,len(sites)):
				pos = sites[i].split(";")[0]
				aa = sites[i].split(";")[1]
				newSite = Phosphorylation_site()
				newSite.accession_number = Protein.objects.get(accession_number=acc)
				newSite.amino_acid = aa
				newSite.position = pos
				newSite.site_id = '%s-%s-%s' % (acc, pos, aa)
				newSite.motif = ""
				newSite.reviewed = True
				newSite.comments = ""
				newSite.source = source
				newSite.save()	

				for ref_id in ref[i].split(';'):
					if not ref[i].isdigit() or not ref[i]:
						continue
					try:
						rec_parser = Medline.RecordParser()
						medline_dict = PubMed.Dictionary(parser = rec_parser)
						handle = Entrez.efetch(db="pubmed", id=ref_id, rettype="medline",retmode="text")
						record = Medline.parse(handle)
					except Exception,e:
						print 'PubMed',e
						continue

					newReference = Reference()
					newReference.reference_id = ref_id
					newReference.title = record["TI"]
					newReference.authors =  record["AU"]
					newReference.location = record["SO"]
					newReference.comments = ""
					newReference.save()

					# Check if the reference has been inserted into the database.
					#if not Reference.objects.filter(reference_id=ref_id):
					#	print "I am not able to insert this reference into the database:", pubmed_id
					#	continue

					# Relate the reference to the protein if it does not already exist.	
					newOIDR = ObjectId_Reference()
					newOIDR.object_id = newSite.site_id
					newOIDR.reference = Reference.objects.get(reference_id=ref_id)
					newOIDR.save()
						
			
if __name__ == '__main__':
	parse()

