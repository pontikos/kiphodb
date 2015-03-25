from dbproject.KiPhoDB.models import * 
from django.contrib import admin

# Add the Protein table.
class Protein_Admin(admin.ModelAdmin):
	list_display = ('accession_number', 'protein_name', 'protein_type', 'substrate', 'ec_number', 'organism_name', 'reviewed', 'updated')
	list_filter = ['protein_type', 'substrate', 'reviewed', 'updated']
	search_fields = ['accession_number', 'protein_name', 'gene_accession_number', 'gene_name', 'ec_number', 'cog', 'protein_sequence', 'comments' ]
admin.site.register(Protein, Protein_Admin)


# Add the GOTerm table.
class GOTerm_Admin(admin.ModelAdmin):
	list_display = ('go_term', 'name', 'ontology', 'definition')
	list_filter = ['ontology']
	search_fields = ['go_term', 'name', 'definition', 'comments']
admin.site.register(GOTerm, GOTerm_Admin)


# Add the GOTerm_Protein table.
class GOTerm_Protein_Admin(admin.ModelAdmin):
	list_display = ('accession_number', 'go_term', 'comments')
	search_fields = ['accession_number', 'go_term', 'comments']
admin.site.register(GOTerm_Protein, GOTerm_Protein_Admin)


# Add the Domain table.
class Domain_Admin(admin.ModelAdmin):
	list_display = ('pfam_id', 'name', 'description', 'comments')
	search_fields = ['pfam_id', 'name', 'description', 'comments']
admin.site.register(Domain, Domain_Admin)


# Add the Domain_Protein table.
class Domain_Protein_Admin(admin.ModelAdmin):
	list_display = ('accession_number', 'pfam', 'domain_type', 'comments')
	list_filter = ['domain_type']
	search_fields = ['accession_number', 'pfam', 'comments']
admin.site.register(Domain_Protein, Domain_Protein_Admin)


# Add the Domain_Domain table.
class Domain_Domain_Admin(admin.ModelAdmin):
	list_display = ('pfam_id_1', 'pfam_id_2', 'description', 'comments')
	search_fields = ['pfam_id_1', 'pfam_id_2', 'description', 'comments']
admin.site.register(Domain_Domain, Domain_Domain_Admin)


# Add the Reaction table.
class Reaction_Admin(admin.ModelAdmin):
	list_display = ('reaction_id', 'ki_pho_accession_number', 'substrate_accession_number', 'reaction_type', 'reaction_effect', 'reaction_evidence', 'reaction_score', 'reaction_description', 'reviewed', 'updated')
	list_filter = ['reaction_type', 'reviewed',]
	search_fields = ['reaction_id', 'ki_pho_accession_number', 'substrate_accession_number', 'reaction_description', 'comments']
admin.site.register(Reaction, Reaction_Admin)


# Add the PhosphorylationSite table.
class PhosphorylationSite_Admin(admin.ModelAdmin):
	list_display = ('phosphosite_id', 'accession_number', 'amino_acid', 'motif', 'reviewed', 'updated')
	list_filter = ['amino_acid', 'reviewed', 'updated']
	search_fields = ['site_id', 'accession_number', 'motif', 'comments']
admin.site.register(PhosphorylationSite, PhosphorylationSite_Admin)


# Add the Pathway table.
class Pathway_Admin(admin.ModelAdmin):
	list_display = ('pathway_id', 'pathway_name', 'organism_name', 'reviewed', 'updated')
	list_filter = ['organism_name', 'reviewed', 'updated']
	search_fields = ['pathway_id', 'pathway_name', 'description', 'comments']
admin.site.register(Pathway, Pathway_Admin)


# Add the Reaction_Pathway table.
class Reaction_Pathway_Admin(admin.ModelAdmin):
	list_display = ('reaction', 'pathway', 'reviewed', 'updated')
	list_filter = ['reviewed', 'updated']
	search_fields = ['reaction', 'pathway', 'comments']
admin.site.register(Reaction_Pathway, Reaction_Pathway_Admin)


# Add the Organism table.
class Organism_Admin(admin.ModelAdmin):
	list_display = ('organism_name', 'common_name', 'organism_type', 'cellularity')
	list_filter = ['organism_type', 'cellularity']
	search_fields = ['organism_name', 'common_name', 'comments']
admin.site.register(Organism, Organism_Admin)


# Add the Tree table.
class Tree_Admin(admin.ModelAdmin):
	list_display = ('tree_id', 'name', 'reviewed', 'updated')
	list_filter = ['reviewed', 'updated']
	search_fields = ['tree_id', 'name', 'structure', 'comments']
admin.site.register(Tree, Tree_Admin)


# Add the File table.
class File_Admin(admin.ModelAdmin):
	list_display = ('id', 'object_id', 'path_to_file', 'date', 'comments')
	list_filter = ['date']
	search_fields = ['object_id', 'path_to_file', 'comments']
admin.site.register(File, File_Admin)

# Add the Genefamily table.
class Genefamily_Admin(admin.ModelAdmin):
	list_display = ('id','treefam_id','protein_type','gene_id','gene_name')
	list_filter = ['protein_type']
	search_fields = ['protein_type']
admin.site.register(Genefamily, Genefamily_Admin)


# Add the cancer_pathway table
class Cancer_pathway_Admin(admin.ModelAdmin):
	list_display = ('id','pathway_id','pathway_description','pathway_type','pathway_name','protein_id','protein_name','protein_type','substrate_id','substrate_name','substrate_type','pairs')
	list_filter = ['protein_type','substrate_type','pathway_id','pathway_type']
	search_fields = ['protein_type']
admin.site.register(Cancer_pathway, Cancer_pathway_Admin)

# Add the Reference table.
class Reference_Admin(admin.ModelAdmin):
	list_display = ('reference_id', 'title', 'authors', 'location', 'comments')
	search_fields = ['reference_id', 'title', 'authors', 'comments']
admin.site.register(Reference, Reference_Admin)


# Add the ObjectId_Reference table.
class ObjectId_Reference_Admin(admin.ModelAdmin):
	list_display = ('object_id', 'reference')
	search_fields = ('object_id', 'reference')
admin.site.register(ObjectId_Reference, ObjectId_Reference_Admin)


# Add the Source table.
class Source_Admin(admin.ModelAdmin):
	list_display = ('source_id', 'url', 'description')
	search_fields = ('source_id', 'url', 'description')
admin.site.register(Source, Source_Admin)


# Add the ID table.
class ID_Admin(admin.ModelAdmin):
	list_display = ('id', 'object_id', 'external_id', 'source', 'comments')
	search_fields = ['object_id', 'external_id', 'source', 'comments']
admin.site.register(ID, ID_Admin)


