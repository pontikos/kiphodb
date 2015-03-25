import sys
import os
#if imported from update
def path(*args):
	return os.sep.join([str(x) for x in args])
if __name__ == 'update.organism_up':
        ABSPATH = os.path.abspath(path('.','organism_up'))
else:
        ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))

sys.path.append(os.sep.join([ABSPATH, ".."]))
#Need to add this for models objects to work
sys.path.append(os.sep.join([ABSPATH, "..", ".."]))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
# Import all necessary modules.
import settings
from KiPhoDB.models import *
import re
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
import urllib

lineage=[]

def update():
    for organism in Organism.objects.all():

        soup = BeautifulSoup(urllib.urlopen("http://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Undef&name=%s&lvl=0&srchmode=1&keep=1&unlock" %str(organism.organism_name).replace(' ','+')).read())    

       # finding the common name of the organism
        if soup.find('strong') != None:
            organism.common_name=soup.find('strong').contents[0]
    
            #finding the taxonomic id
            if len(soup.findAll('br')) != 0:
                table=soup.findAll('br')[0]   
                organism.taxonomic_id=table.previousSibling
                #finding the taxonomic lineage
                if soup.find('dd') != None:
                    l=soup.find('dd')
                    if len(l.findAll('a')) != 0:
                        a_tag=l.findAll('a')
                        for n in range(0,len(a_tag)):
                            lineage+=a_tag[n].contents
                        organism.taxonomic_lineage=  ';'.join(lineage[1:])[:300]
                        print organism.common_name
                        print organism.taxonomic_id
                        print organism.taxonomic_lineage
                        print
                        organism.save()
    print 'Done'

if __name__ == '__main__':
	update()



