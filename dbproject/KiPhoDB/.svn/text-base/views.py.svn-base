from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.sites import models as mod
from django.http import *
from django.shortcuts import render_to_response
from models import *
from django.db.models import Q
import datetime
import time
import MySQLdb
import os
import urllib

def urlencode(params):
	for (k, v) in params.items():
		if type(v) == str:
			params[k] = "'%s'" % v
	return urllib.urlencode(params)


# Create the index.html page.
def index(request):
	params = dict()
	print request.META['HTTP_ACCEPT']
	for model in (Protein, Domain, Organism, Reaction, PhosphorylationSite, Pathway, Reference, Tree, File, ID, GOTerm, Genefamily):
		params['%s_num' % model.__name__.lower()] = model.objects.count()
	#this is an ajax request
	if request.META['HTTP_ACCEPT'] == 'application/json' or 'ajax' in request.POST:
		#generate some javascript
		js_code = []
		for (k, count) in params.items():
			js_code.append("$('%s').update(%s)" % (k, count))
		response = """ <script> %s; </script> """ % ';\r'.join(js_code)
		import json
		response = json.dumps(params)
		print response
		return HttpResponse(response, mimetype='application/json')
	else:
		return render_to_response('index.html', params)

def about(request):
	return render_to_response('about.html')

def news(request):
	return render_to_response('news.html')

def search(request):
	return render_to_response('search.html')

def comment(request):
	website = mod.Site.objects.get(id=1)
	return render_to_response('comment.html',{'website':website})

def contact(request):
	return render_to_response('contact.html')

def canpathwaypage(request):
	return render_to_response('canpathwaypage.html')

def impathwaypage(request):
	return render_to_response('impathwaypage.html')

def advancedSearch(request):
	#Create empty containers to hold the information from POST.
	SELECTstatements = []; FROMstatements = []; WHEREstatements = []
	error = None
	if not request.POST:
		return render_to_response('advancedsearch.html',{'error':'You have made a mistake in your selections, which produced an invalid database query. Please try again or contact the developers for help.'})
	#Iterate the contents of POST and fill in the containers with the appropriate data.
	for key in request.POST.keys():

		#If it is a filter and it is not empty, use it to update the containers.
		if re.match('filter.*',key) and request.POST.get(key)!='':
			WHEREstatements.append(re.match('filter\.(.*)',key).group(1) + ' LIKE "%' + request.POST.get(key) + '%"' )
			if FROMstatements.count(re.match('.*\.(.*)\..*',key).group(1)) == 0:
				FROMstatements.append(re.match('.*\.(.*)\..*',key).group(1))
		
		#If it is a display key, update again the containers.
		elif re.match('display.*',key):
			SELECTstatements.append(re.match('display\.(.*)',key).group(1))
			if FROMstatements.count(re.match('.*\.(.*)\..*',key).group(1)) == 0:
				FROMstatements.append(re.match('.*\.(.*)\..*',key).group(1))

		#If it is a not key, update the corresponding where clause.
		elif re.match('not',key):
			for statement in WHEREstatements:
				start = re.match('not\.(.*)',key).group(1) 
				if statement[0:len(start)] == start:
					statement.replace('LIKE','NOT LIKE')
		else:
			pass

	#Add also the connecting tables and their interconnection.
	if 'go_term' in FROMstatements and 'protein' in FROMstatements:
		FROMstatements.append('go_term_protein')
		WHEREstatements.append('go_term.go_term=go_term_protein.go_term_id')
		WHEREstatements.append('protein.accession_number=go_term_protein.accession_number_id')
		SELECTstatements.append('go_term_protein.comments')
	if 'reaction' in FROMstatements and 'pathway' in FROMstatements:
		FROMstatements.append('reaction_pathway')
		WHEREstatements.append('reaction.reaction_id=reaction_pathway.reaction_id')
		WHEREstatements.append('pathway.pathway_id=reaction_pathway.pathway_id')
		SELECTstatements.append('reaction_pathway.reviewed')
		SELECTstatements.append('reaction_pathway.updated')
		SELECTstatements.append('reaction_pathway.comments')
	#if 'domain' in FROMstatements:
	#	FROMstatements.append('domain_domain')
	#	WHEREstatements.append('domain.pfam_id=domain_domain.pfam_id_1_id')
	#	WHEREstatements.append('domain.pfam_id=domain_domain.pfam_id_2_id')
	#	SELECTstatements.append('domain_domain.description')
	#	SELECTstatements.append('domain_domain.comments')
	if 'protein' in FROMstatements and 'phosphorylation_site' in FROMstatements:
		WHEREstatements.append('phosphorylation_site.accession_number_id=protein.accession_number')
	if 'protein' in FROMstatements and 'organism' in FROMstatements:
		WHEREstatements.append('protein.organism_name=organism.organism_name')
	if 'pathway' in FROMstatements and 'organism' in FROMstatements:
		WHEREstatements.append('pathway.organism_name=organism.organism_name')
	if 'reaction' in FROMstatements and 'protein' in FROMstatements:
		WHEREstatements.append('reaction.ki_pho_accession_number_id=protein.accession_number')
		WHEREstatements.append('reaction.substrate_accession_number_id=protein.accession_number')
	if 'protein' in FROMstatements and 'domain' in FROMstatements:
		FROMstatements.append('domain_protein')
		WHEREstatements.append('domain_protein.pfam_id=domain.pfam_id')
		WHEREstatements.append('domain_protein.accession_number_id=protein.accession_number')
		SELECTstatements.append('domain_protein.domain_type')
		SELECTstatements.append('domain_protein.comments')

	#Add the connections of the tables reference and source.
	if 'source' in FROMstatements and 'protein' in FROMstatements:
		FROMstatements.append('objectid_source')
		WHEREstatements.append('protein.accession_number=objectid_source.object_id')
		WHEREstatements.append('source.source_id=objectid_source.source_id')
	if 'source' in FROMstatements and 'phosphorylation_site' in FROMstatements:
		FROMstatements.append('objectid_source')
		WHEREstatements.append('phosphorylation_site.phosphosite_id=objectid_source.object_id')
		WHEREstatements.append('source.source_id=objectid_source.source_id')
	if 'source' in FROMstatements and 'reaction' in FROMstatements:
		FROMstatements.append('objectid_source')
		WHEREstatements.append('reaction.reaction_id=objectid_source.object_id')
		WHEREstatements.append('source.source_id=objectid_source.source_id')
	if 'source' in FROMstatements and 'pathway' in FROMstatements:
		FROMstatements.append('objectid_source')
		WHEREstatements.append('pathway.pathway_id=objectid_source.object_id')
		WHEREstatements.append('source.source_id=objectid_source.source_id')
	if 'reference' in FROMstatements and 'protein' in FROMstatements:
		FROMstatements.append('objectid_reference')
		WHEREstatements.append('protein.accession_number=objectid_reference.object_id')
		WHEREstatements.append('reference.reference_id=objectid_reference.reference_id')
	if 'reference' in FROMstatements and 'phosphorylation_site' in FROMstatements:
		FROMstatements.append('objectid_reference')
		WHEREstatements.append('phosphorylation_site.phosphosite_id=objectid_reference.object_id')
		WHEREstatements.append('reference.reference_id=objectid_reference.reference_id')
	if 'reference' in FROMstatements and 'reaction' in FROMstatements:
		FROMstatements.append('objectid_reference')
		WHEREstatements.append('reaction.reaction_id=objectid_reference.object_id')
		WHEREstatements.append('reference.reference_id=objectid_reference.reference_id')
	if 'reference' in FROMstatements and 'domain' in FROMstatements:
		FROMstatements.append('objectid_reference')
		WHEREstatements.append('domain.pfam_id=objectid_reference.object_id')
		WHEREstatements.append('reference.reference_id=objectid_reference.reference_id')

	#Form the sql query.
	SQL = 'SELECT '
	if SELECTstatements:
		for statement in SELECTstatements:
			SQL += statement + ', '
		SQL = SQL[0:len(SQL)-2]
	else:
		SQL += '*'
	SQL += ' FROM '
	for statement in FROMstatements:
		SQL += statement + ', '
	SQL = SQL[0:len(SQL)-2]
	if WHEREstatements:
		SQL += ' WHERE '
		for statement in WHEREstatements:
			if statement == 'reaction.substrate_accession_number_id=protein.accession_number':
				SQL = SQL[0:len(SQL)-4] + ' OR ' + statement + ' AND '
			else:
				SQL += statement + ' AND '
		SQL = SQL[0:len(SQL)-4]
	SQL += ';'

	# Try to execute the query.
	try:
		db=MySQLdb.connect(user="anonymous",passwd="anonymous",db="kiphodb")
		c=db.cursor()
		c.execute(SQL)
		print SQL
		results = c.fetchall()
		print results
		c.close()
	# If the query failed, get the reason.
	except Exception, e:
		print e
		error = str(e) + SQL
		results = ""
	return render_to_response('advancedsearch.html',{'results':results,'columns':SELECTstatements,'error':error,'query':SQL})



def sqlresults(request):
	# Get the SQL query from the user.
	SQLquery = request.POST['SQLquery']
	error = ""

	# Try to execute the query.
	try:
		db=MySQLdb.connect(user="anonymous",passwd="anonymous",db="kiphodb")
		c=db.cursor()
		c.execute(SQLquery)
		results = c.fetchall()
		c.close()
	# If the query failed, get the reason.
	except Exception, e:
		error = str(e)
		results = ""
	return render_to_response('sqlresults.html',{'results':results,'error':error})



def generateTree(request):
	errors = tree = fastaFile = treeFile = ''
	proteinString = request.POST['Proteins']
	proteins = proteinString.replace(' ','').split(',')
	
	#Try to open the file for output. If there is an error, return immediately.
	try:
		fastaFile = open('/tmp/fastaFile', 'w')
	except:
		errors += "The fasta file could not be generated."
		return render_to_response('generateTree.html',{'errors':errors})

	#For every protein, get its sequence and store it in fasta format in the output file.
	for protein in proteins:
		# If the protein is empty, continue with the next one.
		if not protein:
			continue

		#Try to fetch the protein from the database.
		try:
			retrievedProtein = Protein.objects.get(accession_number=protein)
		except:
			errors += "The protein: " + protein + " was not found in the database."
			continue

		#Store the sequence in fasta format.
		org = retrievedProtein.organism_name.organism_name.replace(' ','_')
		if org>4:
			org = org[0:4]
		name = retrievedProtein.protein_name.replace(' ','_')
		if name>50:
			name = name[0:50]
		fastaFile.write('> ' + protein + '-' + org + '-' + name + '\n')
		fastaFile.write(retrievedProtein.protein_sequence + '\n\n')
	#Close the file.
	fastaFile.close()
	
	#Run ClastalW2
	os.system('/home/kipho/clustalw2 -INFILE=/tmp/fastaFile -TREE -OUTPUTTREE=phylip')
	os.system('rm /tmp/fastaFile')
	try:
		treeFile = open('/tmp/fastaFile.ph', 'r')
		fileContents = treeFile.read()
		tree = fileContents.replace('\n','').replace(' ','%20')
		treeFile.close()
		os.system('rm /tmp/fastaFile.ph')
	except:
		errors += "The phylogenetic tree file could not be created."
		return render_to_response('generateTree.html',{'errors':errors})

	# Return the results.	
	return render_to_response('generateTree.html',{'errors':errors,'tree':tree})

# This method evaluates the results of a search using the search tool and then it diplays them using the template results.html.
def results(request):
	# Initialize all variables.
	errors = proteins = domains = phosphorylation_sites = reactions = references = pathways  = organisms = trees = go_terms = accessions = kinfamily=phosfamily= families= ''
	protein_number = domain_number = pho_site_number = reaction_number = pathway_number = organism_number = tree_number = go_number = kinfam_number = phosfam_number = fam_number = ref_number = ''
	reac_ids = dict()
	path_ids =dict()

	p_ids = []
	r_ids = []
	p_external_ids= []
	r_external_ids = []
	r_s_ids = []
	p_s_ids = []
	path_source_ids = dict()
	reac_source_ids = dict()

	# Try to retrieve the search options and the search string. If there is an error, return the error message.
	params = dict([(str(k), v) for (k, v) in request.GET.items()])
	if not params:
		searchOptions = request.POST.getlist('search')
		searchString = request.POST['searchString']
		page = 1
		if not searchOptions or not searchString:
		    errors = 'No results were found because you did not check any one of the checkboxes in the previous page. Please use the "Back" button of your browser to return to the previous page and make the appropriate corrections.'
		    return render_to_response('results.html',{'errors':errors,'proteins':proteins,'domains':domains,'phosphorylation_sites':phosphorylation_sites,'reactions':reactions,'references':references,'pathways':pathways,'organisms':organisms,'trees':trees,'go_terms':go_terms})
	else:
		try:			
			searchOptions = params['search']
			searchString = params['searchString']
			page = int(params['page'])
		except:
			errors = 'No results were found because you did not check any one of the checkboxes in the previous page. Please use the "Back" button of your browser to return to the previous page and make the appropriate corrections.'
			return render_to_response('results.html',{'errors':errors,'proteins':proteins,'domains':domains,'phosphorylation_sites':phosphorylation_sites,'reactions':reactions,'references':references,'pathways':pathways,'organisms':organisms,'trees':trees,'go_terms':go_terms,'kinfamily':kinfamily})


	# If the protein has been selected, search in all protein fields for the keyword.
	if 'protein' in searchOptions:
		if searchString == '*':
			proteins = Protein.objects.order_by('organism_name')[:100]
		else:
			proteins =  Protein.objects.filter(Q(accession_number__icontains=searchString) | Q(protein_name__icontains=searchString) | Q(gene_name__icontains=searchString) | Q(gene_accession_number__icontains=searchString) | Q(ec_number__icontains=searchString) | Q(protein_sequence__icontains=searchString) | Q(comments__icontains=searchString))
			if len(proteins) > 3:
				for protein in proteins:
					accessions += protein.accession_number + ','
		protein_number = int(proteins.count())

		paginator = Paginator(proteins, 10)
		if page < paginator.num_pages:
			proteins = paginator.page(page)
		else:
			proteins = paginator.page(paginator.num_pages)

	# If the domain has been selected, search in all domain fields for the keyword.
	if 'domain' in searchOptions:
		if searchString == '*':
			domains = Domain.objects.all()
		else:
			domains = Domain.objects.filter(Q(pfam_id__icontains=searchString) | Q(name__icontains=searchString) | Q(description__icontains=searchString) | Q(comments__icontains=searchString))
		domain_number = domains.count()
		paginator = Paginator(domains, 10)	
		if page < paginator.num_pages:
			domains = paginator.page(page)
		else:
			domains = paginator.page(paginator.num_pages)


	# If the phosphorylation_site has been selected, search in all phosphorylation_site fields for the keyword.
	if 'phosphorylation_site' in searchOptions:
		if searchString == '*':
			phosphorylation_sites = PhosphorylationSite.objects.all()
		else:
			phosphorylation_sites = PhosphorylationSite.objects.filter(Q(phosphosite_id__icontains=searchString) | Q(position__icontains=searchString) | Q(motif__icontains=searchString) | Q(comments__icontains=searchString))
		pho_site_number =  phosphorylation_sites.count()
		paginator = Paginator(phosphorylation_sites, 10)	
		if page < paginator.num_pages:
			phosphorylation_sites = paginator.page(page)
		else:
			phosphorylation_sites = paginator.page(paginator.num_pages)
			
	# If the reaction has been selected, search in all reaction fields for the keyword.
	if 'reaction' in searchOptions:
		if searchString == '*':
			reactions = Reaction.objects.order_by('reaction_type')
		else:
			reactions = Reaction.objects.filter(Q(reaction_id__icontains=searchString) | Q(reaction_description__icontains=searchString) | Q(comments__icontains=searchString))
			
		for reac in reactions:
			r_ids.append(reac.reaction_id)
			r_external_ids.append('RC%0.6d' %reac.reaction_id)
			r_s_ids.append(ID.objects.filter(object_id ='RC%0.6d'%reac.reaction_id, source = reac.source))
		reac_source_ids = dict(zip(r_ids, r_s_ids))
		reac_ids = dict(zip(r_ids, r_external_ids))
		reaction_number = reactions.count()
		paginator = Paginator(reactions, 10)		
		if page < paginator.num_pages:
			reactions = paginator.page(page)
		else:
			reactions = paginator.page(paginator.num_pages)

	# If the pathway has been selected, search in all pathway fields for the keyword.
	if 'pathway' in searchOptions:
		if searchString == '*':
			pathways = Pathway.objects.order_by('organism_name')
		else:
			pathways = Pathway.objects.filter(Q(pathway_id__icontains=searchString) | Q(pathway_name__icontains=searchString) | Q(description__icontains=searchString) | Q(comments__icontains=searchString))

		for path in pathways:
			p_ids.append(path.pathway_id)
			p_external_ids.append('PW%0.6d' %path.pathway_id)
			p_s_ids.append(ID.objects.filter(object_id = 'PW%0.6d' %path.pathway_id, source = path.source))			  
		path_source_ids = dict(zip(p_ids, p_s_ids))
		pathway_number = pathways.count()
		path_ids = dict(zip(p_ids, p_external_ids))			
		paginator = Paginator(pathways, 10)	
		if page < paginator.num_pages:
			pathways = paginator.page(page)
		else:
			pathways = paginator.page(paginator.num_pages)
		
	# If the organism has been selected, search in all organism fields for the keyword.
	if 'organism' in searchOptions:
		if searchString == '*':
			organisms = Organism.objects.all()
		else:
			organisms = Organism.objects.filter(Q(organism_name__icontains=searchString) | Q(taxonomic_id__icontains=searchString) | Q(taxonomic_lineage__icontains=searchString) | Q(common_name__icontains=searchString) | Q(comments__icontains=searchString))
		organism_number = organisms.count()
		paginator = Paginator(organisms, 10)	
		if page < paginator.num_pages:
			organisms = paginator.page(page)
		else:
			organisms = paginator.page(paginator.num_pages)
		
	# If the tree has been selected, search in all tree fields for the keyword.
	if 'tree' in searchOptions:
		trees = Tree.objects.filter(Q(tree_id__icontains=searchString) | Q(name__icontains=searchString) | Q(structure__icontains=searchString) | Q(sql_query__icontains=searchString) | Q(comments__icontains=searchString))
		tree_number =  trees.count()
		paginator = Paginator(trees, 10)	
		if page < paginator.num_pages:
			trees = paginator.page(page)
		else:
			trees = paginator.page(paginator.num_pages)
		
	# If the GO term checkbox has been selected, search in all GO term fields for the keyword.
	if 'go_term' in searchOptions:
		go_terms = GOTerm.objects.filter(Q(go_term__icontains=searchString) | Q(name__icontains=searchString) | Q(definition__icontains=searchString) | Q(comments__icontains=searchString))
		paginator = Paginator(go_terms, 10)
		go_number = go_terms.count()
		if page < paginator.num_pages:
			go_terms = paginator.page(page)
		else:
			go_terms = paginator.page(paginator.num_pages)

		# For the Kinfamily
	if 'kinfamily' in searchOptions:
		kinfamily = Genefamily.objects.filter(protein_type__icontains=searchString)
		kinfam_number = kinfamily.count()
		#For Phosfamily
	if 'phosfamily' in searchOptions:
		phosfamily = Genefamily.objects.filter(protein_type__icontains=searchString)
		phosfam_number = phosfamily.count()


	if 'genename' in searchOptions:
		if searchString == '*':
			families = Genefamily.objects.all()
		else:
			families = Genefamily.objects.filter(gene_name__icontains=searchString)
			page = 1
		fam_number = families.count()
		paginator = Paginator(families, 50)
		families = paginator.page(page)

	if 'gene' in searchOptions:
		if searchString == '*':
			families = Genefamily.objects.all()
		else:
			families = Genefamily.objects.filter(gene_id__icontains=searchString)
		fam_number = families.count()
		page=1
		paginator = Paginator(families, 50)	
		families = paginator.page(1)

	if 'treefam_id' in searchOptions:
		if searchString == '*':
			families = Genefamily.objects.all()
		else:
			families = Genefamily.objects.filter(treefam_id__icontains=searchString)
		fam_number = families.count()
		page=1
		paginator = Paginator(families, 50)	
		families = paginator.page(1)

	# If the Reference checkbox has been selected, search in all Reference fields for the keyword.
	if 'reference' in searchOptions:
		references = Reference.objects.filter(Q(reference_id__icontains=searchString) | Q(title__icontains=searchString) | Q(authors__icontains=searchString) | Q(location__icontains=searchString) | Q(comments__icontains=searchString))
		ref_number = references.count()
		paginator = Paginator(references, 10)	
		references = paginator.page(page)
		if page < paginator.num_pages:
			references = paginator.page(page)
		else:
			references = paginator.page(paginator.num_pages)
			
	get_params = dict(zip(['search','searchString'],[searchOptions,searchString]))


	# Return the results so that they can be diplayed on the website.
	return render_to_response('results.html',{'errors':errors,'proteins':proteins,'domains':domains,'phosphorylation_sites':phosphorylation_sites,'reactions':reactions,'reac_ids':reac_ids,'reac_source_ids':reac_source_ids,'references':references,'pathways':pathways,'path_source_ids':path_source_ids,'path_ids':path_ids,'organisms':organisms,'trees':trees,'go_terms':go_terms,'accessions':accessions,'kinfamily':kinfamily,'phosfamily':phosfamily,'families':families,'protein_number':protein_number,' domain_number':domain_number,'pho_site_number':pho_site_number, 'reaction_number':reaction_number, 'pathway_number':pathway_number, 'organism_number':organism_number, 'tree_number':tree_number, 'go_number':go_number, 'kinfam_number':kinfam_number, 'phosfam_number':phosfam_number, 'fam_number':fam_number,'ref_number': ref_number,'getparams':urlencode(get_params)})



def protein(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('protein.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	numperpage = 20
	if 'numperpage' in get_params:
		numperpage = int(get_params['numperpage'])
		del get_params['numperpage']

	print get_params

	proteins = Protein.objects.filter(**get_params)
	protein_number = proteins.count()
	#If no protein matched the query, return an error message.
	ids = []
	external_ids = []
	s_ids = []
	if not proteins:
		return render_to_response('protein.html',{'error':'No proteins matched your query. Please try again...'})

	if len(proteins) > 1:
		paginator = Paginator(proteins, numperpage)
		try:
			proteins = paginator.page(page)
		except (EmptyPage, InvalidPage):
			proteins = paginator.page(paginator.num_pages)
		
		return render_to_response('results.html',{'proteins':proteins,'protein_number':protein_number,'getparams':urlencode(get_params),})

	protein_accession_number = proteins[0].accession_number
	protein = Protein.objects.get(accession_number=protein_accession_number)
	orthologs = Protein.objects.exclude(accession_number=protein_accession_number).filter(cog=protein.cog)
	go_terms = GOTerm_Protein.objects.filter(accession_number=protein_accession_number)
	domains = Domain_Protein.objects.filter(accession_number=protein_accession_number)
	reactions = Reaction.objects.filter(Q(ki_pho_accession_number=protein_accession_number)|Q(substrate_accession_number=protein_accession_number))
	for reac in reactions:
		ids.append(reac.reaction_id)
		external_ids.append('RC%0.6d' %reac.reaction_id)
		s_ids.append(ID.objects.filter(object_id ='RC%0.6d'%reac.reaction_id, source = reac.source))
	reac_ids = dict(zip(ids, external_ids))
	reac_source_ids = dict(zip(ids, s_ids))
	phosphorylation_sites = PhosphorylationSite.objects.filter(accession_number = protein_accession_number)
	files = File.objects.filter(object_id=protein_accession_number)
	references = ObjectId_Reference.objects.filter(object_id=protein_accession_number)
	external_ids = ID.objects.filter(object_id=protein_accession_number)

	return render_to_response('protein.html',
			{'protein':protein,'go_terms':go_terms,'domains':domains,'reactions':reactions,'phosphorylation_sites':phosphorylation_sites,'files':files,'references':references,'external_ids':external_ids, 'orthologs':orthologs ,'reac_ids':reac_ids,'reac_source_ids':reac_source_ids,})

def genefamily(request):
	return render_to_response('genefamily.html')

def kinfamily(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])


	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('kinfamily.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	kinfamily = Genefamily.objects.filter(**get_params)
	kinfam_number = kinfamily.count()
	print kinfamily

	#If no protein matched the query, return an error message.
	if not kinfamily:
		return render_to_response('kinfamily.html',{'error':'No proteins matched your query. Please try again...'})

	if len(kinfamily) > 1:
		paginator = Paginator(kinfamily, 30)
		try:
			kinfamily = paginator.page(page)
		except (EmptyPage, InvalidPage):
			kinfamily = paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'kinfamily':kinfamily,'kinfam_number':kinfam_number,'getparams':urlencode(get_params),})


	return render_to_response('kinfamily.html',
			{'gene':gene,'gene_name':gene_name,'treefam_id':treefam_id})

#      request for Phosfamily

def phosfamily(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('phosfamily.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	phosfamily = Genefamily.objects.filter(**get_params)
	phosfam_number = phosfamily.count()
	print phosfamily

	#If no protein matched the query, return an error message.
	if not phosfamily:
		return render_to_response('phosfamily.html',{'error':'No proteins matched your query. Please try again...'})

	if len(phosfamily) > 1:
		paginator = Paginator(phosfamily, 30)
		try:
			phosfamily = paginator.page(page)
		except (EmptyPage, InvalidPage):
			phosfamily = paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'phosfamily':phosfamily, 'phosfam_number':phosfam_number,'getparams':urlencode(get_params),})


	return render_to_response('phosfamily.html',
			{'gene':gene,'gene_name':gene_name,'treefam_id':treefam_id})


def canpathway(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('cancerpathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	canpathway = Cancer_pathway.objects.filter(**get_params)
	print canpathway

	#If no protein matched the query, return an error message.
	if not canpathway:
		return render_to_response('canpathway.html',{'error':'No proteins matched your query. Please try again...'})

	if len(canpathway) > 1:
		paginator = Paginator(canpathway, 30)
		try:
			canpathway = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 canpathway= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'canpathway':canpathway,'getparams':urlencode(get_params),})


	return render_to_response('canpathway.html',
			{})

def impathway(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('cancerpathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	impathway = Cancer_pathway.objects.filter(**get_params)
	print impathway

	#If no protein matched the query, return an error message.
	if not impathway:
		return render_to_response('cancerpathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(impathway) > 1:
		paginator = Paginator(impathway, 30)
		try:
			impathway = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 impathway= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'impathway':impathway,'getparams':urlencode(get_params),})


	return render_to_response('about.html',
			{})

# Pathway 1

def pathway1(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('cancerpathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway1 = Cancer_pathway.objects.filter(**get_params)
	print pathway1

	#If no protein matched the query, return an error message.
	if not pathway1:
		return render_to_response('cancerpathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway1) >=1:
		paginator = Paginator(pathway1, 30)
		try:
			pathway1 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway1= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway1':pathway1,'getparams':urlencode(get_params),})


	return render_to_response('cancerpathwaypage.html.html',
			{})
def pathway2(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('cancerpathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway2 = Cancer_pathway.objects.filter(**get_params)
	print pathway2

	#If no protein matched the query, return an error message.
	if not pathway2:
		return render_to_response('cancerpathwaypage.html',{'error':'No pathways matched your query. Please try again...'})

	if len(pathway2) >=1:
		paginator = Paginator(pathway2, 30)
		try:
			pathway2 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway2= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway2':pathway2,'getparams':urlencode(get_params),})


	return render_to_response('cancerpathwaypage.html',
			{})

def pathway3(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('cancerpathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway3 = Cancer_pathway.objects.filter(**get_params)
	print pathway3

	#If no protein matched the query, return an error message.
	if not pathway3:
		return render_to_response('cancerpathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway3) >=1:
		paginator = Paginator(pathway3, 30)
		try:
			pathway3 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway3= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway3':pathway3,'getparams':urlencode(get_params),})


	return render_to_response('cancerpathwaypage.html',
			{})
def pathway4(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('cancerpathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway4 = Cancer_pathway.objects.filter(**get_params)
	print pathway4

	#If no protein matched the query, return an error message.
	if not pathway4:
		return render_to_response('cancerpathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway4) >=1:
		paginator = Paginator(pathway4, 30)
		try:
			pathway4 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway4= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway4':pathway4,'getparams':urlencode(get_params),})


	return render_to_response('cancerpathwaypage.html',
			{})
def pathway5(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('cancerpathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway5 = Cancer_pathway.objects.filter(**get_params)
	print pathway5

	#If no protein matched the query, return an error message.
	if not pathway5:
		return render_to_response('cancerpathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway5) >=1:
		paginator = Paginator(pathway5, 30)
		try:
			pathway5 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway5= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway5':pathway5,'getparams':urlencode(get_params),})


	return render_to_response('cancerpathwaypage.html',
			{})
def pathway6(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('cancerpathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway6 = Cancer_pathway.objects.filter(**get_params)
	print pathway6

	#If no protein matched the query, return an error message.
	if not pathway6:
		return render_to_response('cancerpathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway6) >=1:
		paginator = Paginator(pathway6, 30)
		try:
			pathway6 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway6= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway6':pathway6,'getparams':urlencode(get_params),})


	return render_to_response('cancerpathwaypage.html',
			{})
def pathway7(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('cancerpathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway7 = Cancer_pathway.objects.filter(**get_params)
	print pathway7

	#If no protein matched the query, return an error message.
	if not pathway7:
		return render_to_response('cancerpathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway7) >=1:
		paginator = Paginator(pathway7, 30)
		try:
			pathway4 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway4= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway7':pathway7,'getparams':urlencode(get_params),})


	return render_to_response('cancerpathwaypage.html',
			{})
def pathway8(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('phosfamily.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway8 = Cancer_pathway.objects.filter(**get_params)
	print pathway8

	#If no protein matched the query, return an error message.
	if not pathway8:
		return render_to_response('cancerpathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway8) >=1:
		paginator = Paginator(pathway8, 30)
		try:
			pathway8 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway8= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway8':pathway8,'getparams':urlencode(get_params),})


	return render_to_response('cancerpathwaypage.html',
			{})
def pathway9(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('cancerpathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway9 = Cancer_pathway.objects.filter(**get_params)
	print pathway9

	#If no protein matched the query, return an error message.
	if not pathway9:
		return render_to_response('cancerpathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway9) >=1:
		paginator = Paginator(pathway9, 30)
		try:
			pathway9 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway9= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway9':pathway9,'getparams':urlencode(get_params),})


	return render_to_response('cancerpathwaypage.html',
			{})
def pathway10(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('phosfamily.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway10 = Cancer_pathway.objects.filter(**get_params)
	print pathway10

	#If no protein matched the query, return an error message.
	if not pathway10:
		return render_to_response('cancerpathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway10) >=1:
		paginator = Paginator(pathway10, 30)
		try:
			pathway10 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway10= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway10':pathway10,'getparams':urlencode(get_params),})


	return render_to_response('cancerpathwaypage.html',
			{})
def pathway11(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('immunepathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway11 = Cancer_pathway.objects.filter(**get_params)
	print pathway11

	#If no protein matched the query, return an error message.
	if not pathway11:
		return render_to_response('immunepathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway11) >= 1:
		paginator = Paginator(pathway11, 30)
		try:
			pathway11 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway11= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway11':pathway11,'getparams':urlencode(get_params),})


	return render_to_response('immunepathwaypage.html',
			{})
def pathway12(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('immunepathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway12 = Cancer_pathway.objects.filter(**get_params)
	print pathway4

	#If no protein matched the query, return an error message.
	if not pathway12:
		return render_to_response('about.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway12) >= 1:
		paginator = Paginator(pathway12, 30)
		try:
			pathway12 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway12= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway12':pathway12,'getparams':urlencode(get_params),})


	return render_to_response('immunepathwaypage.html',
			{})
def pathway13(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('immunepathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway13 = Cancer_pathway.objects.filter(**get_params)
	print pathway13

	#If no protein matched the query, return an error message.
	if not pathway13:
		return render_to_response('immunepathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway13) >= 1:
		paginator = Paginator(pathway13, 30)
		try:
			pathway13 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway13= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway13':pathway13,'getparams':urlencode(get_params),})


	return render_to_response('immunepathwaypage.html',
			{})
def pathway14(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('phosfamily.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway14 = Cancer_pathway.objects.filter(**get_params)
	print pathway14

	#If no protein matched the query, return an error message.
	if not pathway14:
		return render_to_response('immunepathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway14) >=1:
		paginator = Paginator(pathway14, 30)
		try:
			pathway14 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway14= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway14':pathway14,'getparams':urlencode(get_params),})


	return render_to_response('immunepathwaypage.html',
			{})
def pathway15(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('phosfamily.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway15 = Cancer_pathway.objects.filter(**get_params)
	print pathway4

	#If no protein matched the query, return an error message.
	if not pathway15:
		return render_to_response('immunepathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway15) >= 1:
		paginator = Paginator(pathway15, 30)
		try:
			pathway15 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway15= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway15':pathway15,'getparams':urlencode(get_params),})


	return render_to_response('immunepathwaypage.html',
			{})
def pathway16(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('immunepathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway16 = Cancer_pathway.objects.filter(**get_params)
	print pathway16

	#If no protein matched the query, return an error message.
	if not pathway16:
		return render_to_response('about.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway16) >= 1:
		paginator = Paginator(pathway16, 30)
		try:
			pathway16 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway16= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway16':pathway16,'getparams':urlencode(get_params),})


	return render_to_response('immunepathwaypage.html',
			{})
def pathway17(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('phosfamily.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway17 = Cancer_pathway.objects.filter(**get_params)
	print pathway17

	#If no protein matched the query, return an error message.
	if not pathway17:
		return render_to_response('immunepathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway17) >= 1:
		paginator = Paginator(pathway17, 30)
		try:
			pathway17 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway17= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway17':pathway17,'getparams':urlencode(get_params),})


	return render_to_response('immunepathwaypage.html',
			{})
def pathway18(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('immunepathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway18 = Cancer_pathway.objects.filter(**get_params)
	print pathway18

	#If no protein matched the query, return an error message.
	if not pathway18:
		return render_to_response('immunepathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway18) >= 1:
		paginator = Paginator(pathway18, 30)
		try:
			pathway18 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway18= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway18':pathway18,'getparams':urlencode(get_params),})


	return render_to_response('immunepathwaypage.html',
			{})
def pathway19(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('immunepathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway19 = Cancer_pathway.objects.filter(**get_params)
	print pathway4

	#If no protein matched the query, return an error message.
	if not pathway19:
		return render_to_response('immunepathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway19) >= 1:
		paginator = Paginator(pathway19, 30)
		try:
			pathway19 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway19= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway19':pathway19,'getparams':urlencode(get_params),})


	return render_to_response('immunepathwaypage.html',
			{})
def pathway20(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('immunepathwaypage.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	pathway20 = Cancer_pathway.objects.filter(**get_params)
	print pathway4

	#If no protein matched the query, return an error message.
	if not pathway20:
		return render_to_response('immunepathwaypage.html',{'error':'No proteins matched your query. Please try again...'})

	if len(pathway20) >= 1:
		paginator = Paginator(pathway20, 30)
		try:
			pathway20 = paginator.page(page)
		except (EmptyPage, InvalidPage):
			 pathway20= paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathway20':pathway20,'getparams':urlencode(get_params),})


	return render_to_response('immunepathwaypage.html',
			{})


def domain(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('domain.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	domains = Domain.objects.filter(**get_params)
	domian_number = domains.count()
	print domains

	if not domains:
		return render_to_response('domain.html',{'error':'No domains matched your query. Please try again...'})

	if len(domains) > 1:
		paginator = Paginator(domains, 20)
		try:
			domains = paginator.page(page)
		except (EmptyPage, InvalidPage):
			domains = paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'domains':domains,'domian_number':domian_number,'getparams':urlencode(get_params),})

	if not domains:
		error = 'The requested domain does not exist in the database.'
		return render_to_response('domain.html',{'error':error})

	#if len(domains) > 1:
	#	return render_to_response('results.html',{'domains':domain,'domain_number':domain_number})
	
	domain_id = domains[0].pfam_id
	domain = Domain.objects.get(pfam_id=domain_id)
	domains = Domain_Domain.objects.filter(Q(pfam_id_1=domain_id) | Q(pfam_id_2=domain_id))
	files = File.objects.filter(object_id=domain_id)
	references = ObjectId_Reference.objects.filter(object_id=domain_id)
	external_ids = ID.objects.filter(object_id=domain_id)

	return render_to_response('domain.html',
			{'domain':domain,'domains':domains,'files':files,'references':references,'external_ids':external_ids})


def go_term(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('goterm.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	goterms = GOTerm.objects.filter(**get_params)
	go_number = goterms.count()
	print goterms

	if not goterms:
		return render_to_response('goterm.html',{'error':'No go terms matched your query. Please try again...'})

	if len(goterms) > 1:
		paginator = Paginator(goterms, 20)
		try:
			goterms = paginator.page(page)
		except (EmptyPage, InvalidPage):
			goterms = paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'goterms':goterms,'go_number':go_number,'getparams':urlencode(get_params),})

	return render_to_response('goterm.html',{'goterm':goterms[0]})


def phosphorylation_site(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('phosphorylation_site.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	phosphorylation_sites = PhosphorylationSite.objects.filter(**get_params)
	pho_site_number = phosphorylation_sites.count()
	print phosphorylation_sites

	if not phosphorylation_sites:
		return render_to_response('phosphorylation_site.html',{'error':'No phosphorylation site matched your query. Please try again...'})

	if len(phosphorylation_sites) > 1:
		paginator = Paginator(phosphorylation_sites, 20)
		try:
			phosphorylation_sites = paginator.page(page)
		except (EmptyPage, InvalidPage):
			phosphorylation_sites = paginator.page(paginator.num_pages)
		print phosphorylation_sites
		return render_to_response('results.html',{'phosphorylation_sites':phosphorylation_sites,'pho_site_number':pho_site_number,'getparams':urlencode(get_params),})

	pro = Protein.objects.get(accession_number = str(phosphorylation_sites[0].accession_number))
	references = ObjectId_Reference.objects.filter(object_id=str(phosphorylation_sites[0].phosphosite_id))

	return render_to_response('phosphorylation_site.html',{'phosphorylation_site':phosphorylation_sites[0],'protein':pro,'references':references})


def reference(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('reference.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	references = Reference.objects.filter(**get_params)
	print references
	ref_number = references.count()

	if not references:
		return render_to_response('phosphorylation_site.html',{'error':'No phosphorylation site matched your query. Please try again...'})

	if len(references) > 1:
		paginator = Paginator(references, 20)
		try:
			references = paginator.page(page)
		except (EmptyPage, InvalidPage):
			references = paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'references':references,'ref_number':ref_number,'getparams':urlencode(get_params),})

	return render_to_response('reference.html',{'reference':references[0]})


def reaction(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('reaction.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	reactions = Reaction.objects.filter(**get_params)
	reaction_number = reactions.count()
	print reactions
	reac_source_ids = dict()

	if len(reactions) > 1:
		ids = []
		external_ids = []
		s_ids = []
		for reac in reactions:
			ids.append(reac.reaction_id)
			external_ids.append('RC%0.6d' %reac.reaction_id)
			s_ids.append(ID.objects.filter(object_id ='RC%0.6d'%reac.reaction_id, source = reac.source))
		reac_ids = dict(zip(ids, external_ids))
		reac_source_ids = dict(zip(ids, s_ids))
		paginator = Paginator(reactions, 20)
		try:
			reactions = paginator.page(page)
		except (EmptyPage, InvalidPage):
			reactions = paginator.page(paginator.num_pages)

		return render_to_response('results.html',{'reactions':reactions,'reac_source_ids':reac_source_ids, 'reac_ids':reac_ids,'reaction_number':reaction_number, 'getparams':urlencode(get_params),})

	ki_pho = Protein.objects.get(accession_number = str(reactions[0].ki_pho_accession_number))
	substrate = Protein.objects.get(accession_number = str(reactions[0].substrate_accession_number))
	reac_id = 'RC%0.6d'%reactions[0].reaction_id
	external_ids = ID.objects.filter(object_id = reac_id)
	references = ObjectId_Reference.objects.filter(object_id=reac_id)
	files = File.objects.filter(object_id=reac_id)
	reac_source_ids = dict(zip([reactions[0].reaction_id], [ID.objects.filter(object_id ='RC%0.6d'%reactions[0].reaction_id, source = reactions[0].source)]))

	paths = Reaction_Pathway.objects.filter(reaction = reactions[0].reaction_id)
	path_id = []
	for i in xrange(0, len(paths)):
		path_id.append('PW%0.6d'%paths[i].pathway_id)
	pathways = zip(path_id, paths)
	return render_to_response('reaction.html',{'reaction':reactions[0],'reac_source_ids ':reac_source_ids ,'ki_pho':ki_pho,'substrate':substrate,'reaction_id': reac_id,'pathways':pathways, 'external_ids':external_ids,'external_ids':external_ids,'references':references,'files':files})


def organism(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('organism.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	print get_params

	organisms = Organism.objects.filter(**get_params)
	organism_number = organisms.count()
	print organisms

	if not organisms:
		return render_to_response('organism.html',{'error':'No organisms matched your query. Please try again...'})

	if len(organisms) > 1:
		paginator = Paginator(organisms, 20)
		try:
			organisms = paginator.page(page)
		except (EmptyPage, InvalidPage):
			organisms = paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'organisms':organisms, 'organism_number':organism_number,'getparams':urlencode(get_params),})

	return render_to_response('organism.html',{'organism':organisms[0]})


def pathway(request):
	get_params = dict([(str(k), eval(v, {}, {})) for (k, v) in request.GET.items()])

	#If there is an error with the url and the GET dictionary is empty, issue an error message.
	if not get_params:
		return render_to_response('pathway.html',{'error':'Invalid Query! Please try again...'})

	page = 1
	if 'page' in get_params:
		page = int(get_params['page'])
		del get_params['page']

	pathways = Pathway.objects.filter(**get_params)
	pathway_number = pathways.count()
	path_source_ids = dict()
	
	if not pathways:
		return render_to_response('pathway.html',{'error':'No pathways matched your query. Please try again...'})
	if len(pathways) > 1:
		ids = []
		ex_ids = []
		s_ids = []
		for path in pathways:
			ids.append(path.pathway_id)
			ex_ids.append('PW%0.6d' %path.pathway_id)
			s_ids.append(ID.objects.filter(object_id = 'PW%0.6d' %path.pathway_id, source = path.source))			  
		path_ids = dict(zip(ids, ex_ids))
		path_source_ids = dict(zip(ids, s_ids))

		paginator = Paginator(pathways, 20)
		try:
			pathways = paginator.page(page)
		except (EmptyPage, InvalidPage):
			pathways = paginator.page(paginator.num_pages)
		return render_to_response('results.html',{'pathways':pathways,'path_ids':path_ids,'path_source_ids':path_source_ids,'pathway_number':pathway_number, 'getparams':urlencode(get_params),})

	pathway_id = pathways[0].pathway_id
	object_pathway_id = 'PW%0.6d' % pathway_id
	pathway = Pathway.objects.get(pathway_id=pathway_id)
	reactions = Reaction.objects.filter(reaction_id__in=[x.reaction_id for x in Reaction_Pathway.objects.filter(pathway=pathway)])
	references = ObjectId_Reference.objects.filter(object_id=object_pathway_id)
	external_ids = ID.objects.filter(object_id=object_pathway_id)
	files = File.objects.filter(object_id=object_pathway_id)
	path_source_ids = dict(zip([pathway_id],[ID.objects.filter(object_id = 'PW%0.6d' %pathways[0].pathway_id, source = pathways[0].source)]))

	return render_to_response('pathway.html',{'pathway':pathway,'path_source_ids':path_source_ids,'pathway_id':object_pathway_id,'reactions':reactions,'references':references,'external_ids':external_ids})



def tree(request, treeID):
	tree = error =  ''
	references = []; external_ids = []; sources = []; files = []

	#Try to fetch the tree. If there is an error, issue a message.
	try:
		tree = Tree.objects.get(tree_id=treeID)
		tree_number = tree.count()
		references = ObjectId_Reference.objects.filter(object_id=path_id)
		external_ids = ID.objects.filter(object_id=path_id)
		files = File.objects.filter(object_id=path_id)
	except:
		error = 'The requested tree does not exist in the database.'
		return render_to_response('tree.html',{'error':error})

	return render_to_response('tree.html',{'tree':tree,'tree_number':tree_number,'error':error,'references':references,'external_ids':external_ids,'sources':sources})


def reactions(request):
	try:
		q = str(request.POST['searchString'])
		print q
	except:
		return render_to_response('reactions.html',{'error':'No accession number specified'})
	reactions = [x for x in Reaction.objects.filter(Q(ki_pho_accession_number=q) | Q(substrate_accession_number=q))]
	#phosphorylation reactions
	p_reactions = [x for x in reactions if x.reaction_type == 'P']
	#dephosphorylation reactions
	dp_reactions = [x for x in reactions if x.reaction_type == 'D']
	#find phosphorylation/dephosphorylation reactions with common substrate
	p_dp_reactions = [(p, dp) for p in p_reactions for dp in dp_reactions if p.substrate_accession_number == dp.substrate_accession_number]
	return render_to_response('reactions.html',{'accession_number':q,
		'p_reactions':p_reactions,
		'dp_reactions':dp_reactions,
		'p_dp_reactions':p_dp_reactions})


def pairs(request):
	# Initialize all variables.
	errors = proteins = pairs_substrates = ''

	# Try to retrieve the search options and the search string. If there is an error, return the error message.
	try:
		searchString = str(request.POST['searchString'])
		print searchString
	except:
		errors = 'No results were found, please enter a accession number!'
		print errors
		return render_to_response('pairs.html',{'errors':errors,'proteins':proteins,'pairs_substrates':pairs_substrates})

	if Protein.objects.filter(accession_number = searchString):
		proteins = Protein.objects.get(accession_number = searchString)
		print proteins
		if proteins.protein_type == 'O':
			errors = 'No results were found, please search for a kinase or phosphatase!'
			print errors
			return render_to_response('pairs.html',{'errors':errors,'proteins':proteins,'pairs_substrates':pairs_substrates})
		else:
			if proteins.protein_type == 'K':
				pairs_type = 'D'
			elif proteins.protein_type == 'P':
				pairs_type = 'P'
			else:
				pairs_type = 'DP'
			print pairs_type
			reacs = Reaction.objects.filter(ki_pho_accession_number = searchString)
			if not reacs:
				errors = 'No reaction was found for this protein as a catalyst!'
				print errors
				return render_to_response('pairs.html',{'errors':errors,'proteins':proteins,'pairs_substrates':pairs_substrates})
			else:
				self_reactions = []
				pair_reactions = []
				self_id = []
				pair_id = []
				for reac in reacs:
					print reac
					reacs_sub = Reaction.objects.filter(substrate_accession_number = reac.substrate_accession_number)
					for reac_sub in reacs_sub:
						print reac_sub, reac.substrate_accession_number
						if reac_sub.reaction_type == pairs_type or pairs_type == 'DP':
							self_reactions.append(reac)
							self_id.append(str('RC%0.6d'%reac.reaction_id))
							pair_reactions.append(reac_sub)
							pair_id.append(str('RC%0.6d'%reac_sub.reaction_id))
						
				if len(self_reactions) == 0 or len(pair_reactions) == 0:
					errors = 'No pair was found for this protein!'
					print errors
					return render_to_response('pairs.html',{'errors':errors,'proteins':proteins,'pairs_substrates':pairs_substrates})
				else:
					pairs_substrates = zip (self_reactions, pair_reactions, self_id, pair_id)
					print pairs_substrates
					return render_to_response('pairs.html',{'errors':errors,'proteins':proteins,'pairs_substrates':pairs_substrates})
	else:
		errors = 'No information for this protein!'
		print errors
		return render_to_response('pairs.html',{'errors':errors,'proteins':proteins,'pairs_substrates':pairs_substrates})

def suggest_reaction_protein(request):
	q = request.GET.get('q','')
	limit = int(request.GET.get('max',10))
	#only for accession numbers now
	#suggestions = '\n'.join(["%s %s" % (x.accession_number,x.protein_name[:20]) for x in Protein.objects.filter(accession_number__istartswith=q)])
	suggestions = '\n'.join([x.ki_pho_accession_number.accession_number for x in Reaction.objects.filter(Q(ki_pho_accession_number__accession_number__istartswith=q) | Q(substrate_accession_number__accession_number__istartswith=q))])
	#print suggestions
	return HttpResponse(suggestions, mimetype='text/plain')

def suggest(request):
	q = request.GET.get('q','')
	limit = int(request.GET.get('max',10))
	#only for accession numbers now
	#suggestions = '\n'.join(["%s %s" % (x.accession_number,x.protein_name[:20]) for x in Protein.objects.filter(accession_number__istartswith=q)])
	suggestions = '\n'.join([x.accession_number for x in Protein.objects.filter(accession_number__istartswith=q)])
	#print suggestions
	return HttpResponse(suggestions, mimetype='text/plain')

def test(request):
	return render_to_response('test2.html')

def ajax_test(request):
	return HttpResponse('jog on you si\ndude\nyeah', mimetype='text/plain')


