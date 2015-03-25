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

import re

try:
    lines=file("familyA.txt.table").readlines()
except Exception,e:
    print e
    exit()

headers = ['treefam_id','protein_name','description']

for line in lines:
    names = dict(zip(headers, [x.strip() for x in line.strip().split('\t')]))

    if re.search('phosphatase',names['description']):
        newFamily=Genefamily()
        newFamily.protein_type='P'
        newFamily.treefam_id=names['treefam_id']
        newFamily.gene_id=names['protein_name']
        newFamily.gene_name=names['description']
        newFamily.save()

    if re.search('kinase',names['description']):
        newFamily=Genefamily()
        newFamily.protein_type='K'
        newFamily.treefam_id=names['treefam_id']
        newFamily.gene_id=names['protein_name']
        newFamily.gene_name=names['description']
        newFamily.save()

