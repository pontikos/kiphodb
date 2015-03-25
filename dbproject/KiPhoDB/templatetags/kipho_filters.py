from django.template.defaultfilters import stringfilter
from django import template
from django.template.loader import render_to_string
from django.template import Template

register = template.Library()

@register.filter(name='reviewed')
@stringfilter
def reviewed(r):
	return dict({'1':'yes', '0':'no'}).get(r, '')

@register.filter
@stringfilter
def yes_no(b):
	return dict({'1':'yes', '0':'no'}).get(b, '')

@register.filter(name='amino_acid')
@stringfilter
def amino_acid(a):
	return dict({'S':'Ser','T':'Thr','Y':'Tyr','X':'Unk'}).get(a, '')

@register.filter(name='protein_type')
@stringfilter
def protein_type(pt):
	return dict({'K':'Kinase','P':'Phosphatase','D':'Kinase/Phosphatase','O':'Other'}).get(pt, '')

@register.filter(name='substrate')
@stringfilter
def substrate(s):
	return dict({'0':'No','1':'Yes'}).get(s, '')

@register.filter(name='ontology')
@stringfilter
def ontology(o):
	return dict({'B':'Biochemical Process','C':'Cellular Component','M':'Molecular Function','U':'Unknown'}).get(o, '')

@register.filter(name='domain_type')
@stringfilter
def domain_type(d):
	return dict({'A':'Active Site','B':'Binding Site','P':'Phosphorylation Site','O':'Other'}).get(d, '')

@register.filter(name='organism_type')
@stringfilter
def organism_type(ot):
	return dict({'P':'Plant','A':'Animal','U':'Unknown'}).get(ot, '')

@register.filter(name='cellularity')
@stringfilter
def cellularity(c):
	return dict({'U':'Unicellular','M':'Multicellular','X':'Unknown'}).get(c, '')

@register.filter(name='organism_domain')
@stringfilter
def organism_domain(od):
	return dict({'A':'Archaea','B':'Bacteria','E':'Eukarya'}).get(od, '')

@register.filter(name='reaction_type')
@stringfilter
def reaction_type(t):
	return dict({'P':'phosphorylates', 'D':'dephosphorylates', 'U':'unknown reaction',}).get(t, '')

@register.filter(name='reaction_effect')
@stringfilter
def reaction_effect(e):
	return dict({'A':'Activation','D':'Deactivation','U':'Unknown'}).get(e, '')

@register.filter(name='reaction_evidence')
@stringfilter
def reaction_evidence(e):
	return dict({'H':'High Throughput Experimental','V':'In Vivo','R':'In Vitro','S':'In Silico','U':'Unknown'}).get(e, '')

@register.filter
def hash(h, key):
    return h[key]

@register.filter
def accession_list(proteins):
	return ','.join([str(p.accession_number) for p in proteins])

@register.filter
def hasID(id):
	if str(id.external_id).find("[") != -1:
		return bool(0)
	else:
		return bool(1)

@register.filter
def hasID_reac(id):
	if str(id.external_id).find("Reactome:") != -1:
		return bool(0)
	else:
		return bool(1)	

@register.filter
def source(s, ids):
	if str(s) == "PANTHER":
		return "http://www.pantherdb.org/pathway/pathDetail.do?clsAccession="+str(ids.external_id)
	if str(s) == "NCI-Nature curated":
		return "http://pid.nci.nih.gov/search/pathway_landing.shtml?pathway_id="+str(ids.external_id)+"&source=NCI-Nature%20curated&what=graphic&gif=on&ppage=1"
	if str(s) == "KEGG Pathway":
		return "http://www.genome.ad.jp/dbget-bin/www_bget?pathway+"+str(ids.external_id)
	if str(s) == "Reactome":
		return "http://www.reactome.org/cgi-bin/eventbrowser_st_id?ST_ID="+str(ids.external_id)
