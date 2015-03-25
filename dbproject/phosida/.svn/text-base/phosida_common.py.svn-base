import sys
import os

def PATH(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'phosida.bacil_parser':
	ABSPATH = os.path.abspath('phosida')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(PATH(ABSPATH, '..'))
#Need to add this for models objects to work
sys.path.append(PATH(ABSPATH, '..', '..'))
from uniprotxml import *

print ABSPATH

SOURCE_ID = 'PHOSIDA'
source = Source()
source.source_id = SOURCE_ID
source.url = 'http://www.phosida.com/'
source.description = """
The PHOsphorylation SIte DAtabase allows retrieval of phosphorylation data of any protein of interest.
It lists phosphorylation sites associated with particular projects and proteomes or, alternatively, displays phosphorylation sites found for any protein or protein group of interest.
In addition, structural and evolutionary information on each phosphoprotein and phosphosite is integrated.
"""
source.save()

