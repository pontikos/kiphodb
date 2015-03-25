import sys
import os
def PATH(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'reaction.inact.inact':
		p = PATH('reaction','inact')
		ABSPATH = os.path.abspath(p)
		print ABSPATH
elif __name__ == 'inact.inact':
		ABSPATH = os.path.abspath('inact')
else:
		ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))

# Add to the sys path the path to the dbproject
sys.path.append(ABSPATH+"/../..")
#Need to add this for models objects to work
sys.path.append(ABSPATH+"/../../..")

from uniprotxml import *
import re

SOURCE_ID = 'InAct'
source = Source()
source.source_id = SOURCE_ID
source.url = 'http://www.ebi.ac.uk/intact/site/index.jsf'
source.description = 'IntAct provides a freely available, open source database system and analysis tools for protein interaction data. All interactions are derived from literature curation or direct user submissions and are freely available.'
source.save()

def parse():
	try:
		lines = file(PATH(ABSPATH, "InAct_Dephosphorylation.txt"), 'r').readlines()
	except Exception, e:
		print 'I/O File error', e
		exit()

	headers = [x.strip() for x in lines[0].split('\t')]

	for line in lines[1:]:
		interact = dict(zip(headers, [x.strip() for x in line.strip().split('\t')]))
		interact['Accession number molecule A'] = interact['Accession number molecule A'].split(",")[0]
		interact['Accession number molecule B'] = interact['Accession number molecule B'].split(",")[0]
		if interact['Accession number molecule A'].find("-") != -1:
			index_a = interact['Accession number molecule A'].find("-")
			interact['Accession number molecule A'] = interact['Accession number molecule A'][0:index_a]
		if interact['Accession number molecule B'].find("-") != -1:
			index_b = interact['Accession number molecule B'].find("-")
			interact['Accession number molecule B'] = interact['Accession number molecule B'][0:index_b]
		if len(interact['Accession number molecule A']) != 6 or len(interact['Accession number molecule B']) != 6:
			print "No uniprot information"
			continue
		print interact['Accession number molecule A'],interact['Accession number molecule B']

		#Get UniProt entry
		try:
			prot_a = UniprotEntry(accession=interact['Accession number molecule A'])
		except Exception, e:
			print 'Uniprot entry', e
			continue
		try:
			prot_b = UniprotEntry(accession=interact['Accession number molecule B'])
		except Exception, e:
			print 'Uniprot entry', e
			continue


		if len(re.findall(r'[Pp]hosphatase',prot_a.name())) != 0:
			if prot_b.substrate():
				sub = prot_b
				cata = prot_a
		elif len(re.findall(r'[Pp]hosphatase',prot_b.name())) != 0:
			if prot_a.substrate():
				sub = prot_a
				cata = prot_b
		else:
			print "Not a dephosphorylation reaction."
			continue
		sub_acc = str(sub.accession())
		cata_acc = str(cata.accession())


		#Check for alternative UniProt AC
		if ID.objects.filter(external_id = sub_acc, source = "UniProt"):
			sub_acc = str(ID.objects.get(external_id =sub_acc, source = "UniProt").object_id)
		if ID.objects.filter(external_id = cata_acc , source = "UniProt"):
			cata_acc = str(ID.objects.get(external_id = cata_acc, source = "UniProt").object_id)


		#If the protein does not exsit, add it into protein table                
		if not Protein.objects.filter(accession_number=cata_acc):
			# Fetch the record from Swissprot
			try:
				prot = UniprotEntry(accession=cata_acc)
			except Exception, e:
				print 'Uniprot entry', e
				continue
			try:
				prot.save(substrate=False, source=source)
				#prot.save(substrate=False)
				print 'Saved', prot.accession()
			except Exception, e:
				print 'Uniprot save', e
		else:
			print 'Protein', cata_acc, 'already in database.'

		if not Protein.objects.filter(accession_number=sub_acc):
		# Fetch the record from Swissprot
			try:
				prot = UniprotEntry(accession=sub_acc)
			except Exception, e:
				print 'Uniprot entry', e
				continue
			try:
				prot.save(substrate=True, source=source)
				#prot.save(substrate=True)
				print 'Saved', prot.accession()
			except Exception, e:
				print 'Uniprot save', e
		else:
			print 'Protein', sub_acc, 'already in database.'

		#Store reaction
		if not Reaction.objects.filter(ki_pho_accession_number = cata.accession(), substrate_accession_number = sub.accession()):
			reaction = Reaction()
			reaction.ki_pho_accession_number = Protein.objects.get(accession_number=cata_acc)
			reaction.substrate_accession_number = Protein.objects.get(accession_number=sub_acc)
			reaction.reaction_type = 'D'
			reaction.reaction_evidence = 'U'
			reaction.reaction_score = 1
			reaction.reaction_description = ""
			reaction.reviewed = True
			try:
				reaction.save()
				print 'Added reaction ' ,  reaction.reaction_id
			except Exception, e:
				print 'Reaction', e
		else:
			print 'Reaction', cata.accession(),'->',sub.accession(), 'already in database.'

	print "Done!"
		

if __name__ == '__main__':
	parse()

