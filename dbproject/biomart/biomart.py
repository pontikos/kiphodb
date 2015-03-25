import os
import sys
def PATH(*args):
        return os.sep.join([str(x) for x in args])
if __name__ == 'biomart.biomart':
        ABSPATH = os.path.abspath('biomart')
else:
        ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(PATH(ABSPATH, '..'))

from browser import *
import re


organisms = list(set([x for x in re.findall("homologs__attribute\.([^\.]*?)_ensembl_gene", file('biomart.html', 'r').read())]))

print len(organisms)

orgs=organisms[:4]
print orgs

#query = """<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE Query> <Query  virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.7" > <Dataset name = "hsapiens_gene_ensembl" interface = "default" > <Attribute name = "ensembl_gene_id" /> <Attribute name = "ensembl_transcript_id" /> <Attribute name = "dolphin_ensembl_gene" /> <Attribute name = "tarsier_ensembl_gene" /> </Dataset> </Query>"""
query = """<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE Query> <Query  virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.7" > <Dataset name = "hsapiens_gene_ensembl" interface = "default" > <Attribute name = "ensembl_gene_id" /> %s </Dataset> </Query>""" % ( ''.join(["""<Attribute name = "%s_ensembl_gene" />""" % x for x in orgs]) )

br = Browser('www.ensembl.org',debug=True)

fname = 'biomart-orthologs.tsv'
if os.path.exists(PATH(ABSPATH, fname)) and '--download' not in sys.argv:
	print fname, 'exists'
	p = file(PATH(ABSPATH, fname), 'r').read()
else:
	print fname, 'not found in', ABSPATH
	print 'Downloading from biomart...'
	p = br.get_page('/biomart/martservice', params={'query':query})
	file(PATH(ABSPATH, fname), 'w').write(p)

headers = ['hsapiens'] + orgs
print headers
for line in p.splitlines():
	rec = dict(zip(headers, [x.strip() for x in line.split('\t')]))
	if reduce(lambda x, y: bool(x) or bool(y), [rec[o] for o in orgs]):
		print [(k, rec[k]) for k in headers]



