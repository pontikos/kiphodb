import sys
import os
#if imported from update
if __name__ == 'update.domain':
        ABSPATH = os.path.abspath('./domain')
else:
        ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
def path(*args):
	return os.sep.join([str(x) for x in args])
sys.path.append(path(ABSPATH, '..'))
#Need to add this for models objects to work
sys.path.append(path(ABSPATH, '..', '..'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
# Import all necessary modules.
import settings
from KiPhoDB.models import *
import re
from urllib import urlopen
from xml.dom.minidom import parseString

def update():
	# Iterate the Domain table and update the entries.
	for domain in Domain.objects.all():
		# Try to fetch the PFAM entry for the specific domain.
		try:
			xml_string = urlopen('http://pfam.sanger.ac.uk/family?acc=%s&output=xml' % domain.pfam_id).read()
			dom = parseString(xml_string)
		except Exception, e:
			print e
			print "The PFAM entry for the following record could not be fetched:", domain.pfam_id
			continue

		# Get the data from the PubMed entry and check the integrity of the database entry.
		try:
			domain.name = dom.getElementsByTagName("entry")[0].getAttributeNode("id").value
			domain.description = dom.getElementsByTagName("description")[0].childNodes[1].data.replace( "\n", "")
			domain.comments = re.sub(' \[([1-9]\,)*[1-9]\]', '' ,re.sub(' \[\d*\]', '', dom.getElementsByTagName("comment")[0].childNodes[1].data.replace( "\n", "")))
			domain.save()
			print 'Domain:', domain
			print domain.pfam_id
			print domain.name
		except Exception, e:
			print e
			print "The entry for the following domain could not be updated:", domain.pfam_id

if __name__ == '__main__':
	update()

