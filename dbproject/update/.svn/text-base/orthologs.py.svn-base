import sys
import os
def path(*args):
	return os.sep.join([str(x) for x in args])
#if imported from update
if __name__ == 'update.orthologs':
	ABSPATH = os.path.abspath(path('.', 'orthologs'))
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
# Add to the sys path the path to the dbproject
sys.path.append(path(ABSPATH,".."))
#Need to add this for models objects to work
sys.path.append(path(ABSPATH,"..",".."))

from uniprotxml import *

def update():
	for p in Protein.objects.iterator():
		ue = UniprotEntry(accession=p.accession_number)
		for ortho in ue.orthologs():
			ortho.save()
			print 'Saved', ortho, 'ortholog of', ue

if __name__ == '__main__':
	update()

