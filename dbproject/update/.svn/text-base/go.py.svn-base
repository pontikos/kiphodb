import sys
import os
def path(*args):
	return os.sep.join([str(x) for x in args])
#if imported from update
if __name__ == 'update.go':
	ABSPATH = os.path.abspath(path('.', 'go'))
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
# Add to the sys path the path to the dbproject
sys.path.append(path(ABSPATH,".."))
#Need to add this for models objects to work
sys.path.append(path(ABSPATH,"..",".."))

from uniprotxml import *
from urllib import urlopen
from xml.dom.minidom import parseString


def update():
	# Iterate the GO_term table and update the entries.
	for go in GOTerm.objects.all():
		# Try to fetch the GO entry for the specific term.
		try:
			xml_string = urlopen('http://amigo.geneontology.org/cgi-bin/amigo/term-details.cgi?term=' + go.go_term + '&format=rdfxml').read()
			dom = parseString(xml_string)
		except Exception, e:
			print go
			print "The GO entry for the following GO term could not be fetched:" , go.go_term
			continue

		# Analyze the xml file and retrieve the required information.
		try:
			goterms = dom.getElementsByTagName("go:term")
			for term in goterms:
				# If the GO term is not the one we want, continue with the next one.
				if term.getElementsByTagName("go:accession")[0].firstChild.data != go.go_term:
					continue

				# Get the name, the definition and the comments for the specific GO term, if they exist.
				go.name = term.getElementsByTagName("go:name")[0].firstChild.data
				if term.getElementsByTagName("go:definition"):
					go.definition = term.getElementsByTagName("go:definition")[0].firstChild.data
				if term.getElementsByTagName("go:comment"):
					go.comment = term.getElementsByTagName("go:comment")[0].firstChild.data

			# Find the ontology that this term belongs to.
			if xml_string.find("molecular_function") != -1:
				go.ontology = 'M'
			elif xml_string.find("biological_process") != -1:
				go.ontology = 'B'
			elif xml_string.find("cellular_component") != -1:
				go.ontology = 'C'
			else:
				go.ontology = 'U'
			go.save()
			print 'GOTerm', go
			print go.name
		except Exception, e:
			print "The entry for the following GO term could not be updated:" , go.go_term
			continue
	print 'Done'

if __name__ == '__main__':
	update()

