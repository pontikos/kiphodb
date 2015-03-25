import sys
import os
#if imported from update

if __name__ == 'phosphopoint.phosphopoint':
        ABSPATH = os.path.abspath('phosphopoint')
else:
        ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))

# Add to the sys path the path to the dbproject
sys.path.append(os.sep.join([ABSPATH, ".."]))
#Need to add this for models objects to work
sys.path.append(os.sep.join([ABSPATH, "..", ".."]))
from uniprotxml import *

import xlrd
import re

#First create a new entry in the source table.
source = Source()
source.source_id = 'PhosphoPoint'
source.url = 'http://kinase.bioinformatics.tw/'
source.description = 'Phosphopoint is a curated database of Phosphorylation sites of phosphoproteins and kinases in HUmans'
source.save()

def parse():
	#Try to open the xls book.
	try:
		book = xlrd.open_workbook(os.sep.join([ABSPATH, "Human_4195_PhosphoProteins.xls"]))
		sheet = book.sheet_by_index(0)
		headers = sheet.row_values(0)
	except Exception,e:
		print e
		exit()

	#Read every row and insert it in the database.
	seq=''
	for n in xrange(1,sheet.nrows):
		#Read the contents of the line.
		lineContents = dict(zip(headers,sheet.row_values(n)))

		#If the SwissProt field is empty, we can safely ignore the entry.
		if not lineContents['SwissProt']:
			continue

		#Extract the contents of the line.
		swissprot_id=lineContents['SwissProt']
		site=lineContents['Site']
		kinases=lineContents['Kinase']
		pubmed_ids=lineContents['PubMed']
		source_dbs=lineContents['Source']

		# If the protein does not exist, add it along with the organism, its GO terms, its Domains and its References.
		try:
			protein = UniprotEntry(accession=swissprot_id)
		except Exception, e:
			print e
			continue

		swissprot_id = protein.accession()
		seq=protein.sequence()

		protein.save(substrate=True, source=source)
		print 'Saved', protein.accession()

		# Save the phosphorylation site in the database.
		# If we have no sequence, continue with the next protein.
		if not seq:
			continue
		if not PhosphorylationSite.objects.filter(accession_number=swissprot_id, position=site[1:]):
			aa = site[0]
			pos = site[1:]
			newSite = PhosphorylationSite()
			newSite.accession_number = Protein.objects.get(accession_number=swissprot_id)
			newSite.amino_acid = aa
			newSite.position = pos
			newSite.site_id = '%s-%s-%s' % (swissprot_id, aa, pos)
			newSite.source = source
			#if int(site[1:]) < 6 and len(seq) - int(site[1:]) < 6:
			#	newSite.motif = seq[:int(site[1:])-1] + seq[int(site[1:])-1].lower() + seq[int(site[1:]):]
			#elif int(site[1:]) < 6:
			#	newSite.motif = seq[:int(site[1:])-1] + seq[int(site[1:])-1].lower() + seq[int(site[1:]):int(site[1:])+5]
			#	try:
			#		if len(seq) - int(site[1:]) < 6:
			#			newSite.motif = seq[int(site[1:])-6:int(site[1:])-1] + seq[int(site[1:])-1].lower() + seq[int(site[1:]):]
			#	except Exception, e:
			#		print "String index out of range" ,e
			#		continue
			#else:
			#	newSite.motif = seq[int(site[1:])-6:int(site[1:])-1] + seq[int(site[1:])-1].lower() + seq[int(site[1:]):int(site[1:])+5]
			newSite.motif = ""
			newSite.reviewed = True
			newSite.comments = "This site has been identified by: " + source_dbs

			newSite.save()

			# Store the references, too.
			for pub_id in pubmed_ids.split(';'):
				if not pub_id.isdigit() or not pub_id:
					continue

				# If the reference does not exist, create it.
				if not Reference.objects.filter(reference_id=pub_id):
					newReference = Reference()
					newReference.reference_id = pub_id
					newReference.title = ""
					newReference.authors = ""
					newReference.location = ""
					newReference.comments = ""
					try:
						newReference.save()
					except Exception, e:
						print 'Reference', e

				# Check if the reference has been inserted into the database.
				if not Reference.objects.filter(reference_id=pub_id):
					print "I am not able to insert this reference into the database: ", pub_id
					continue

				# Relate the reference to the phosphorylation site if it does not already exist.
				if not ObjectId_Reference.objects.filter(object_id=newSite.site_id, reference=pub_id):
					newOIDR = ObjectId_Reference()
					newOIDR.object_id = newSite.site_id
					newOIDR.reference = Reference.objects.get(reference_id=pub_id)
					try:
						newOIDR.save()
					except Exception, e:
						print 'ObjectId_Reference', e

		# If there are no kinases, continue with the next entry.
		if not kinases:
			continue

		# Insert entries in the reactions table.
		b=Browser('www.uniprot.org')
		kinases= kinases.split(';')

		# For every kinase in the list, search uniprot.
		for kinase in kinases:
			# If kinase is empty, continue with the next one.
			if not kinase:
				continue

			# Find the name of the kinase gene
			kinase = re.search('(.*)-\d*', kinase).group(1)
			query = 'gene:%s AND organism:"%s" AND reviewed:yes AND fragment:no' % (kinase, 'human')
			dom=b.get_page_dom('/uniprot/', params={'query':query, 'force':'yes', 'format':'xml',})

			# If nothing is found, issue an error message.
			if not dom.entry:
				print 'Nothing found', kinase, 'Human.'
				continue

			# If the protein does not exist, add it along with the organism, its GO terms, its Domains and its References.
			kinase_uniprot = UniprotEntry(dom=dom.entry)
			if not Protein.objects.filter(accession_number=kinase_uniprot.accession()):
				# Save the record.
					try:
						kinase_uniprot.save(reviewed=True, substrate=False, protein_type='K', source=source, comment=kinase_uniprot.comment('function'))
					except Exception, e:
						print 'Uniprot save', e
						continue
			else:
				print 'Protein', kinase_uniprot.accession(), 'already in database.'

			# Create a new reaction in the Reaction table.
			if not Reaction.objects.filter(ki_pho_accession_number=Protein(kinase_uniprot.accession()), substrate_accession_number=Protein(swissprot_id)):
				newReaction = Reaction()
				newReaction.ki_pho_accession_number = Protein(kinase_uniprot.accession())
				newReaction.substrate_accession_number = Protein(swissprot_id)
				newReaction.reaction_type = 'P'
				newReaction.reaction_effect = 'A'
				newReaction.reaction_evidence = 'R'
				newReaction.reaction_score = '1'
				newReaction.reaction_description = ''
				newReaction.source = source
				newReaction.save()

if __name__ == '__main__':
	parse()

