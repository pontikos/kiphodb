#http://www.uniprot.org/docs/uniprot.xsd
import sys
#needed for importing models
sys.path.append('..')
sys.path.append('../..')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import settings
from KiPhoDB.models import *
from browser import *
import BeautifulSoup
import re
from htmlentitydefs import name2codepoint

SOURCE_ID = 'Uniprot'
s = Source()
s.source_id = SOURCE_ID
s.url = 'www.uniprot.org'
s.description = """
The Universal Protein Resource (UniProt) is a comprehensive resource for protein sequence and annotation data. The UniProt databases are the UniProt Knowledgebase (UniProtKB), the UniProt Reference Clusters (UniRef), and the UniProt Archive (UniParc). The UniProt Metagenomic and Environmental Sequences (UniMES) database is a repository specifically developed for metagenomic and environmental data.
"""
s.save()

SOURCE_ID2 = 'Phosphosite'
s2 = Source()
s2.source_id = SOURCE_ID2
s2.url = 'www.phosphosite.org'
s2.description = """
Information obtained in vivo about phosphorylation sites and orthologues in human, mouse and rat.
"""
s2.save()


class UniprotEntry:
	uniref_id = ''
	def __repr__(self):
		return '<UniprotEntry %s>' % self.accession()
	""" """
	def __init__(self, dom=None, accession=None, organism=None, gene=None, reviewed=True, fragment=False, force_update=False):
		ubrowser = Browser('www.uniprot.org')
		if dom: 
			if isinstance(dom, BeautifulSoup.Tag):
				self.entry = dom
			else:
				raise Exception('%s is not a valid BeautifulSoup Tag' % type(dom))
		elif accession:
			#before fetching from uniprot check if entry exists already in db
			if Protein.objects.filter(accession_number=accession) and not force_update:
				p = Protein.objects.get(accession_number=accession)
				self.load(p)
			else:
				dom = ubrowser.get_page_dom('/uniprot/%s.xml' % accession)
				if dom.entry:
					self.entry = dom.entry
				else:
					raise Exception('%s not found on Uniprot' % accession)
		else:
			#--------------------------------------------------
			# br = Browser('www.ncbi.nlm.nih.gov')
			# br.get_page('/sites/entrez?db=Taxonomy&cmd=search&term=%s' % organism)
			#-------------------------------------------------- 
			#before fetching from uniprot check if entry exists already in db
			if Protein.objects.filter(gene_accession_number=gene, organism_name=Organism(organism), reviewed=reviewed) and not force_update:
				p = Protein.objects.get(gene_accession_number=gene, organism_name=Organism(organism), reviewed=reviewed)
				self.load(p)
			else:
				yes_no = {True:'yes', False:'no'}
				reviewed = yes_no[reviewed]
				fragment = yes_no[fragment]
				query = 'gene_exact:%s AND organism:"%s" AND reviewed:%s AND fragment:%s' % (gene, organism, reviewed, fragment)
				dom = ubrowser.get_page_dom('/uniprot/', params={'query':query, 'force':'yes', 'format':'xml',})
				if dom.entry:
					self.entry = dom.entry
				else:
					raise Exception('"%s" not found on Uniprot' % query)
	def load(self, p):
		def accession():
			return p.accession_number
		self.accession = accession
		organism = p.organism_name
		def organism_name():
			return organism.organism_name
		self.organism_name = organism_name
		def taxonomic_id():
			return organism.taxonomic_id
		self.taxonomic_id = taxonomic_id
		def taxonomic_lineage(*args, **k):
			return organism.taxonomic_lineage
		self.organism_lineage = taxonomic_lineage
		def protein_type():
			return p.protein_type
		self.protein_type = protein_type
		def reviewed():
			return bool(p.reviewed)
		self.reviewed = reviewed
		#def save(*args, **k):
			#pass
		#self.save = save
		def name():
			return p.protein_name
		self.name = name
		def gene_accession_number():
			return p.gene_accession_number
		self.gene_accession_number = gene_accession_number
		self.uniref_id = p.cog
		def substrate():
			return p.substrate
		self.substrate = substrate
		def sequence():
			return p.protein_sequence
		self.sequence = sequence
		#load references
		def references():
			return []
			#return Reference.objects.filter(objectid_reference__object_id=p.accession_number)
		self.references = references
		def go_terms():
			return []
		self.go_terms = go_terms
		def pfam_terms():
			return []
		self.pfam_terms = pfam_terms
		def phosphosite_terms():
			return []
		self.phosphosite_terms = phosphosite_terms
	def parse(self):
		self.Accession = self.accession()
		self.AllAccessions = self.all_accessions()
		self.Reviewed = self.reviewed()
		self.Name = self.name()
		self.ProteinType = self.protein_type()
	def accession(self):
		try:
			return self.entry.accession.string.strip()
		except:
			return None
	def all_accessions(self):
		try:
			return [x.string.strip().upper() for x in self.entry.findAll('accession')[1:]]
		except:
			return []
	def reviewed(self):
		return {'Swiss-Prot':True, 'TrEMBL':False}[self.entry['dataset']]
	def name(self):
		try:
			return self.entry.protein.recommendedname.fullname.string.strip()
		except:
			try: 
				return self.entry.protein.submittedname.fullname.string.strip()
			except:
				return None
	def protein_type(self):
		#<keyword id="KW-0418">Kinase</keyword>
		#<keyword id="KW-0904">Protein phosphatase</keyword>
		if self.entry.find('keyword', {'id':'KW-0418'}) and self.entry.find('keyword', {'id':'KW-0904'}):
			#can act as both a kinase and phosphatase
			return 'D'
		elif self.entry.find('keyword', {'id':'KW-0904'}):
			return 'P'
		elif self.entry.find('keyword', {'id':'KW-0418'}):
			return 'K'
		#<property type="term" value="F:phosphatidate phosphatase activity"/>
		elif self.entry.find('dbreference', {'type':'GO', 'id':'GO:0008195'}):
			return 'P'
		else:
			return 'O'
	def substrate(self):
		#<keyword id="KW-0597">Phosphoprotein</keyword>
		if self.entry.find('keyword', {'id':'KW-0597'}):
			return True
		else:
			return False
	def protein_existence(self):
		#<proteinExistence type="Evidence at transcript level"/>
		try:
			return self.entry.find('proteinexistence')['type']
		except:
			return ''
	def gene_accession_number(self):
		try:
			return self.entry.gene.find('name', {'type':'primary'}).string.strip().upper()
		except:
			try:
				return self.entry.find('name', {'type':'ORF'}).string.strip().upper()
			except:
				try:
					return self.entry.gene.find('name', {'type':'ordered locus'}).string.strip().upper()
				except:
					return
	def cog(self):
		return self.gene_accession_number()
	def all_gene_accession_numbers(self):
		try:
			return [x.string.strip().upper() for x in self.entry.gene.findAll('name')[1:]]
		except:
			return []
	def gene_name(self):
		try:
			return self.entry.gene.find('name', {'type':'primary'}).string.strip().upper()
		except:
			try:
				return self.entry.gene.find('name', {'type':'ordered locus'}).string.strip().upper()
			except:
				try:
					return self.gene_accession_number().upper()
				except:
					return
	def organism_name(self):
		try:
			return self.entry.organism.find('name', {'type':'scientific'}).string.strip()
		except:
			return None
	def organism_taxonomic_id(self):
		try:
			return self.entry.organism.dbreference['id']
		except:
			return None
	def organism_lineage(self, format=False):
		try:
			lineage = [x.string.strip() for x in self.entry.organism.lineage.findAll('taxon')]
			if format:
				return ';'.join(lineage)
			else:
				return lineage
		except:
			return None
	def sequence(self):
		try:
			return self.entry.find('sequence', {'length':True}).string.strip().replace('\n','')
		except:
			return None
	def ec_number(self):
		try:
			return self.entry.find('dbreference', {'type':'EC'})['id'].strip()
		except:
			return ''
	def comment(self, t):
		#PTM
		try:
			return self.entry.find('comment', {'type':t}).text.string.strip()
		except:
			return ''
	def references(self):
			class UniprotRef:
				source = ''
				def __repr__(self):
					return "<UniprotRef '%s'>" % self.title
			for ref in self.entry.findAll('reference'):
				uniref = UniprotRef()
				cit = ref.citation
				#--------------------------------------------------
				# "book"
				# "journal article"
				# "online journal article"
				# "patent"
				# "submission"
				# "thesis"
				# "unpublished observations"
				# "unpublished results"
				#-------------------------------------------------- 
				uniref.type = cit['type']
				#we don't like anything else than journal article for now
				if 'journal article' in uniref.type:
					try:
						uniref.title = cit.title.string.strip()
					except:
						print ref
						continue
					uniref.authors = [str(p['name']).strip() for p in cit.authorlist.findAll('person')]
					try:
						uniref.source = cit['name']
					except:
						print cit
					try:
						uniref.pubmed = cit.find('dbreference', {'type':'PubMed'})['id']
					except:
						uniref.pubmed = None
					try:
						uniref.doi = cit.find('dbreference', {'type':'DOI'})['id']
					except:
						uniref.doi = None
				elif uniref.type == 'submission':
					#uniref.source = cit['db']
					continue
				else:
					#uniref.source = None
					continue
				try:
					uniref.date = cit['date']
				except Exception, e:
					print e
					uniref.date = None
				yield uniref
	def go_terms(self):
		class GoTerm:
			id = ''
			name = ''
			ontology = 'U'
			evidence = ''
			def __repr__(self):
				return "<GoTerm '%s'>" % self.id
		for gt in self.entry.findAll('dbreference', {'type':'GO'}):
			goterm = GoTerm()
			goterm.id = gt['id'] 
			properties = gt.findAll('property')
			for p in properties:
				if 'evidence' in p:
					goterm.evidence = gt['evidence']
				elif 'term' in p:
					goterm.ontology, goterm.name, = gt['term'].split(':')
			yield goterm
	def pfam_terms(self):
		pfam_terms = []
		class PfamTerm:
			id = ''
			entry_name = ''
			match_status = ''
			startpos = 0
			endpos = 0
			def __repr__(self):
				return '<PfamTerm %s>' % self.id
		for pf in self.entry.findAll('dbreference', {'type':'Pfam'}):
			pfamterm = PfamTerm()
			pfamterm.id = pf['id']
			properties = pf.findAll('property')
			for p in properties:
				ptype = p['type']
				if ptype == 'entry_name':
					pfamterm.entry_name = p['value']
				elif ptype == 'match status':
					pfamterm.match_status = p['value']
			pfam_terms.append(pfamterm)
		#http://pfam.sanger.ac.uk/protein?acc=P01233&output=xml
		br = Browser('pfam.sanger.ac.uk')
		dom = br.get_page_dom('/protein?acc=%s&output=xml' % self.accession())
		for pfterm in pfam_terms:
			loc = dom.find('match', {'accession':pfterm.id, 'class':('Domain', 'Family', 'Motif', 'Repeat')})
			if not loc:
				print dom
				print pfterm.id in str(dom)
				print pfterm.id, 'info not found'
				continue
			loc = loc.location
			pfterm.startpos = int(loc['start'])
			pfterm.endpos = int(loc['end'])
			yield pfterm
	def phosphosite_terms(self):
		class PhosphositeTerm:
			id = ''
			aa = ''
			pos = ''
			motif = ''
			pubmedids = []
			def __repr__(self):
				return '<PhosphositeTerm %s>' % self.id
		#no point in checking
		#self.entry.findAll('dbreference', {'type':'Phosphosite'}):
		#just go straight to phosphosite
		br = Browser('www.phosphosite.org')
		dom = br.get_page_dom('/uniprotAccAction.do?id=%s' % self.accession())
		#<table id="siteTable"></table>
		siteTable = dom.find('table', id='siteTable')
		if not siteTable:
			print 'no phosphosites found for %s' % self.accession()
			return
		#next table after siteTable is phosTable
		phosTable = None
		for sibling in siteTable.nextGenerator():
			if isinstance(sibling, BeautifulSoup.Tag) and sibling.name == 'table':
				phosTable = sibling
				break
		if not phosTable:
			print 'no phosTable found for %s' % self.accession_number()
			return
		#third cell of every row in phos table is phos site
		#other cells are for orthologs and isoforms
		phosre = re.compile('(?P<aa>[A-Z])(?P<pos>\d+)-p')
		for row in phosTable.findAll('tr'):
			tds = row.findAll('td')
			if len(tds) < 3:
				continue
			#<a href="/siteAction.do?id=50231" class="linkSite">S37-p</a>
			a = tds[2].find('a', {'class':'linkSite'})
			if not a:
				continue
			m = phosre.match(a.string.strip())
			if not m:
				print 'phosphosite no match'
				print a.string.strip()
				continue
			phosphositeTerm = PhosphositeTerm()
			phosphositeTerm.aa = m.group('aa')
			phosphositeTerm.pos = m.group('pos')
			href = a['href']
			phosphositeTerm.id = href.split('=')[1]
			br.clear_cookies()
			d = br.get_page_dom(a['href'])
			motif = str(d.find('span', {'class':'peptideSeq'})).strip()
			phosphositeTerm.motif = re.sub("(<.*?>|\&nbsp|;| |\n|\t)", '', motif).strip()
			phosphositeTerm.pubmedids = [x.string.strip() for x in d.findAll('a', {'class':'link12HoverRed', 'href':re.compile('http://www\.ncbi\.nlm\.nih\.gov.*Abstract')})]
			yield phosphositeTerm
	def createOrganism(self):
		o = Organism()
		o.organism_name = self.organism_name()
		o.taxonomic_id = self.organism_taxonomic_id()
		o.taxonomic_lineage = self.organism_lineage(format=True)
		return o
	def createProtein(self, organism, protein_type, substrate, comment, source):
		p = Protein()
		p.accession_number = self.accession()
		p.protein_name = self.name()
		if protein_type:
			p.protein_type = protein_type
		else:
			p.protein_type = self.protein_type()
		if substrate is None:
			p.substrate = self.substrate()
		else:
			p.substrate = substrate
		p.gene_accession_number = self.gene_accession_number()
		p.gene_name = self.gene_name()
		p.ec_number = self.ec_number()
		p.cog = self.uniref_id
		print 'cog', p.cog
		p.organism_name = organism
		p.protein_sequence = self.sequence()
		p.reviewed = self.reviewed()
		p.comments = comment
		if source:
			p.source = source
		return p
	def createReference(self, r):
		reference = Reference()
		if r.pubmed:
			reference.reference_id = r.pubmed
		elif r.doi:
			reference.reference_id = r.doi
		else:
			reference.reference_id = r.title
		reference.title = r.title
		reference.authors = ','.join(r.authors)
		reference.location = r.source
		#reference.comments = '%s' % doi
		return reference
	def createGOTerm(self, gt):
		goterm = GOTerm()
		goterm.go_term = gt.id
		goterm.name = gt.name
		goterm.ontology = {'F':'M', 'P':'B', 'C':'C',}.get(gt.ontology, 'U')
		#goterm.definition = gt.evidence
		return goterm
	def createDomain(self, pfam):
		domain = Domain()
		domain.pfam_id = pfam.id
		domain.name = pfam.entry_name
		return domain
	def createPhosphosite(self, protein, phos, source=Source(SOURCE_ID2)):
		phosphorylation_site = PhosphorylationSite()
		phosphorylation_site.phosphosite_id = 'PS%d' % int(phos.id)
		phosphorylation_site.accession_number = protein
		phosphorylation_site.amino_acid = phos.aa
		phosphorylation_site.position = phos.pos
		phosphorylation_site.motif = phos.motif
		phosphorylation_site.pubmedids = phos.pubmedids
		phosphorylation_site.source = source
		return phosphorylation_site
	def delete(self,):
		Protein.objects.get(accession_number=self.accession()).delete()
	""" """
	def save(self, reviewed=None, protein_type=None, substrate=None, comment='', source=''):
		def try_save(m, exception, **k):
			from django.db import connection
			try:
				m.save(**k)
				return m
			except Exception, e:
				print e
				print list(connection.queries)[-1]
				raise exception
		o = try_save(self.createOrganism(), Exception('Organism'))
		p = try_save(self.createProtein(o, protein_type, substrate, comment, source), Exception('Protein'))
		#Populate ids table with synonymous accession numbers
		for acc in self.all_accessions():
			try_save(ID(object_id=self.accession(), external_id=acc, source=Source(SOURCE_ID),
				comments='synonymous accession from Uniprot'), Exception('ID'))
		#Populate ids table with synonymous gene accession numbers
		for acc in self.all_gene_accession_numbers():
			try_save(ID(object_id=self.gene_accession_number(), external_id=acc, source=Source(SOURCE_ID),
				comments='synonymous gene accession from Uniprot'), Exception('ID'))
		#Populate reference table
		for r in self.references():
			reference = try_save(self.createReference(r), Exception('Reference'), object_id=self.accession())
		#Populate GOTerm table
		for gt in self.go_terms():
			goterm = try_save(self.createGOTerm(gt), Exception('GOTerm'))
			try_save(GOTerm_Protein(accession_number=p, go_term=goterm), Exception('GOTerm_Protein'))
		#Populate Domain table
		for pfam in self.pfam_terms():
			domain = try_save(self.createDomain(pfam), Exception('Domain'))
			#Populate Domain_Protein table
			try_save(Domain_Protein(accession_number=p, pfam=domain, startpos=pfam.startpos, endpos=pfam.endpos), Exception('Domain_Protein'))
		#Populate phosphosite table
		for phosterm in self.phosphosite_terms():
			phos = try_save(self.createPhosphosite(p, phosterm), Exception('PhosphorylationSite'))
			#save references
			for pubmedid in phos.pubmedids:
				try_save(Reference(reference_id=pubmedid), Exception('Reference'), object_id=phos.phosphosite_id)
	def genename_orthologs(self):
		ubrowser = Browser('www.uniprot.org')
		query = 'gene_exact:%s AND reviewed:yes AND fragment:no' % self.gene_accession_number()
		dom = ubrowser.get_page_dom('/uniprot/', params={'query':query, 'force':'yes', 'format':'xml',})
		for entry in dom.findAll('entry'):
			yield UniprotEntry(dom=entry)
	def blast_orthologs(self, threshold=0.0001, numal=100):
		ubrowser = Browser('www.uniprot.org')
		page = ubrowser.get_page('/uniprot/%s?tab=blast' % self.accession())
		params = {
				'query': '>%s\n%s' % (self.accession(), self.sequence()),
				'redirect': 'yes',
				'url' : '',
				'annotated':'false',
				'dataset':'swissprot',
				'threshold':str(threshold),
				'matrix':'',
				'filter':'false',
				'gapped':'true',
				'numal':str(numal),
				}
		try:
			page = ubrowser.get_page('/blast/', post=params)
			print page
			raise Exception('blast failed')
		except ExternalRedirect, er:
			print er.info()
			host = er.host()
			location = er.location
		ubrowser = Browser(host)
		#get the last bit of the url
		g, = re.compile('.*-(.*-.*)$').search(location).groups()
		print g
		#stick on the end of this one to fetch the results in xml format
		page = ubrowser.get_page('/resultxml/blast-%s' % g)
		#for some reason we get escaped html so we unescape it
		page = re.sub('&(%s);' % '|'.join(name2codepoint), lambda m: unichr(name2codepoint[m.group(1)]), page)
		dom = BeautifulSoup.BeautifulSoup(page)
		#return [(hit['ac'], hit['id'], hit['OS']) for hit in dom.findAll('hit')]
		return [UniprotEntry(accession=hit['ac'].strip()) for hit in dom.findAll('hit')]
	def uniref_orthologs(self, seq_identity=1.0):
		#sequence clusters
		ubrowser = Browser('www.uniprot.org')
		dom = ubrowser.get_page_dom('/uniref/?query=member:%s+identity:%s&format=xml' % (self.accession(), seq_identity))
		seq_cluster_id = dom.find('entry')['id']
		return (seq_cluster_id,
				[UniprotEntry(accession=hit['value'].strip()) for hit in dom.findAll('property', {'type':'UniProtKB accession'})])

if '--test' in sys.argv:
	try:
		Protein.objects.get(accession_number='P46527').delete()
	except Exception, e:
		print e
	unientry2 = UniprotEntry('P46527')
	#unientry2.save()
	b=Browser('www.uniprot.org')
	dom=b.get_page_dom('/uniprot/P68250.xml')
	unientry = UniprotEntry(dom.entry)
	unientry.parse()
	print unientry.Accession
	unientry.save()
	#--------------------------------------------------
	# unientry3 = UniprotEntry('P01233')
	# print unientry3.go_terms()
	#-------------------------------------------------- 





