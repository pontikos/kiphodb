import time
import sys
import os
def PATH(*args):
        return os.sep.join([str(x) for x in args])
#if imported from update
if __name__ == 'update.uniorthologs':
        ABSPATH = os.path.abspath(PATH('.', 'uniorthologs'))
else:
        ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(PATH(ABSPATH, '..'))

from uniprotxml import *

for p in Protein.objects.all():
	time.sleep(5)
	ue = UniprotEntry(accession=p.accession_number, force_update=True)
	#--------------------------------------------------
	# if ue.uniref_id:
	# 	continue
	#-------------------------------------------------- 
	uniref_id, orthologs, = ue.uniref_orthologs()
	for o in orthologs:
		o.uniref_id = uniref_id
		o.save(source=Source('Uniprot'))


