import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import settings
from KiPhoDB.models import *
from Bio import ExPASy
from Bio import SwissProt
import re

class SwissprotEntry:
	def __repr__(self):
		if self.entry:
			return '<SwissprotEntry %s>' % self.accession()
		else:
			return 'None'
	def __init__(self, acc):
		self.entry = self.get(acc)
	def get(self, acc):
		# Fetch the record from uniprot.
		try:
			handle = ExPASy.get_sprot_raw(acc)
			return SwissProt.read(handle)
		except:
			raise Exception("The record with accession number %s was not found in SwissProt." % acc)
	def reviewed(self):
		if self.entry.data_class == "Reviewed":
			return True
		else:
			return False
	def accession(self):
		return self.entry.accessions[0]
	def name(self):
		desc = self.entry.description
		return re.search('(Full=)(.*)(;)', desc).group(2)
	def gene_accession_number(self):
		return self.gene_name()
	def gene_name(self):
		return self.entry.gene_name[5:self.entry.gene_name.find(";")]
	def organism_name(self):
		return self.entry.organism[0:self.entry.organism.find(" (")]
	def organism_taxonomic_id(self):
		return self.entry.taxonomy_id[0]
	def organism_lineage(self, format=False):
		lineage = self.entry.organism_classification
		if format:
			return ';'.join(lineage)
		else:
			return lineage
	def sequence(self):
		return self.entry.sequence
	def ec_number(self):
		desc = self.entry.description
		ec_number = ""
		while desc.find('EC=') != -1:
			ec_number += re.search('(EC=)(.*)(;)', desc).group(2) + ' '
			desc = desc.replace('EC='+re.search('(EC=)(.*)(;)', desc).group(2)+';', '')
		return ec_number
	def comment(self):
		#function comment
		return self.entry.comments[0]
	def references(self):
		class SwissprotRef:
			def __repr__(self):
				return
		# Add the references to this protein.
		for ref in self.entry.references:
			swissref = SwissprotRef()
			# Extract the PubMed ID. If no pubmed id is found, ignore the reference.
			pubmed_id = None
			for r in ref.references:
				if r[0] == "PubMed":
					pubmed_id = r[1]
					break
			if pubmed_id == "":
				continue
			swissref.reference_id = pubmed_id
			swissref.title = ref.title
			swissref.authors = ref.authors
			swissref.location = ref.location
			swissref.comments = ""
			yield swissref
	def cross_references(self):
		return
	def save(self, protein_type='O', substrate=False, source=None):
		#from django.db import connection
		if not self.entry:
			raise Exception('Nothing to save')
		# Create a new protein object and define its properties.
		newProtein = Protein()
		newProtein.accession_number = self.accession()
		for ac in self.entry.accessions[1:]:
			# Store the remaining accession numbers in the ID table, if they do not already exist.
			if not ID.objects.filter(object_id=self.accession(), external_id=ac):
				newID = ID()
				newID.object_id = self.accession()
				newID.external_id = ac
				newID.comments = ""
				try:
					newID.save()
				except Exception, e:
					print 'ID', e

		newProtein.reviewed = self.reviewed()
		newProtein.protein_name = self.name()
		newProtein.ec_number = self.ec_number()
		newProtein.protein_type = protein_type
		newProtein.substrate = substrate
		newProtein.gene_accession_number = self.gene_accession_number()
		newProtein.gene_name = self.gene_name()
		newProtein.protein_sequence = self.sequence()
		newProtein.cog = ""
		newProtein.comments = self.comment()
		# Extract and store the name of the organism.
		o = Organism()
		o.organism_name = self.organism_name()
		o.taxonomic_id = self.organism_taxonomic_id()
		o.taxonomic_lineage = self.organism_lineage(True)
		try:
			o.save()
		except Exception, e:
			#print connection.queries
			print 'Organism', e
		newProtein.organism_name = o
		try:
			newProtein.save()
		except Exception, e:
			#print connection.queries
			print 'Organism', e

		# Add source if specified
		if source:
			ObjectId_Source(object_id=newProtein.accession_number, source=source).save()

		# Add the references to this protein.
		for ref in self.entry.references:
			# Extract the PubMed ID. If no pubmed id is found, ignore the reference.
			pubmed_id = ""
			for r in ref.references:
				if r[0] == "PubMed":
					pubmed_id = r[1]
			if pubmed_id == "":
				continue

			newReference = Reference()
			newReference.reference_id = pubmed_id
			newReference.title = ref.title
			newReference.authors = ref.authors
			newReference.location = ref.location
			newReference.comments = ""
			try:
				newReference.save()
			except Exception, e:
				#print connection.queries
				print 'Reference', e

			newOIDR = ObjectId_Reference()
			newOIDR.object_id = newProtein
			newOIDR.reference = newReference
			try:
				newOIDR.save()
			except Exception, e:
				#print connection.queries
				print 'ObjectId_Reference', e

		# Find the GO terms related to this protein and add then to the database.
		for cross in self.entry.cross_references:
			if cross[0] != "GO":
				continue
			newGOterm = GO_term()
			newGOterm.go_term = cross[1]
			newGOterm.name = cross[2][2:]
			if cross[2][0] == "F":
				newGOterm.ontology = "M"
			elif cross[2][0] == "P":
				newGOterm.ontology = "B"
			elif cross[2][0] == "C":
				newGOterm.ontology = "C"
			else:
				newGOterm.ontology = "U"
			try:
				newGOterm.save()
			except Exception, e:
				#print connection.queries
				print 'GO_term', e
			newGOtermProtein = GO_term_Protein()
			newGOtermProtein.accession_number = Protein.objects.get(accession_number=self.entry.accessions[0])
			newGOtermProtein.go_term = GO_term.objects.get(go_term=cross[1])
			try:
				newGOtermProtein.save()
			except Exception, e:
				#print connection.queries
				print 'GO_term_Protein', e

		#Find the Domains related to this protein and add them to the database.
		for cross in self.entry.cross_references:
			if cross[0] != "Pfam":
				continue
			# If the domain does not exist in the Domains table, add it.
			newDomain = Domain()
			newDomain.pfam_id = cross[1]
			newDomain.name = cross[2]
			try:
				newDomain.save()
			except Exception, e:
				#print connection.queries
				print 'Domain', e
				continue
			# Create a new entry in table Domain_Protein, if it does not already exist.
			newDomainProtein = Domain_Protein()
			newDomainProtein.accession_number = newProtein
			newDomainProtein.pfam = Domain.objects.get(pfam_id=cross[1])
			try:
				newDomainProtein.save()
			except Exception, e:
				#print connection.queries
				print 'Domain_Protein', e


if '--test' in sys.argv:
	e = SwissprotEntry('P01233')
	print e
	e.save()

