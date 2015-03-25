from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib import databrowse
from KiPhoDB.models import *
databrowse.site.register(Protein)
databrowse.site.register(GOTerm)
databrowse.site.register(Organism)
databrowse.site.register(Domain)
databrowse.site.register(Reaction)
databrowse.site.register(PhosphorylationSite)
databrowse.site.register(Pathway)
databrowse.site.register(Tree)
databrowse.site.register(File)
databrowse.site.register(Reference)



urlpatterns = patterns('',
     #DataBrowse.
     (r'^databrowse/(.*)', databrowse.site.root),

     #Administration Site.
     (r'^admin/(.*)', admin.site.root),

     #Static files. 
     #(r'^(?P<path>.*html)$', 'django.views.static.serve', {'document_root': './web_site/'}),
     (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './web_site/images'}),
     (r'^stylesheets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './web_site/stylesheets'}),
     (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './web_site/js'}),
     (r'^PhyloWidget/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './web_site/PhyloWidget'}),
     (r'^database/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './web_site/database'}),
    
     #Index, about, news, search, contact, comments.
     (r'^$', 'dbproject.KiPhoDB.views.index'),
     (r'^about.html','dbproject.KiPhoDB.views.about'),
     (r'^news.html','dbproject.KiPhoDB.views.news'),
     (r'^search.html','dbproject.KiPhoDB.views.search'),
     (r'^contact.html','dbproject.KiPhoDB.views.contact'),
     (r'^comments',include('django.contrib.comments.urls')),
     (r'^comment.html','dbproject.KiPhoDB.views.comment'),
     (r'^genefamily.html','dbproject.KiPhoDB.views.genefamily'),

     #Pages to view single elements.
     (r'^protein$', 'dbproject.KiPhoDB.views.protein'),
     (r'^domain$','dbproject.KiPhoDB.views.domain'),
     (r'^go_term$','dbproject.KiPhoDB.views.go_term'),
     (r'^phosphorylation_site$','dbproject.KiPhoDB.views.phosphorylation_site'),
     (r'^organism$','dbproject.KiPhoDB.views.organism'),
     (r'^reference$','dbproject.KiPhoDB.views.reference'),
     (r'^reaction$','dbproject.KiPhoDB.views.reaction'),

     (r'^pathway$','dbproject.KiPhoDB.views.pathway'),
     (r'^kinfamily$','dbproject.KiPhoDB.views.kinfamily'),
     (r'^phosfamily$','dbproject.KiPhoDB.views.phosfamily'),

     (r'^canpathwaypage$','dbproject.KiPhoDB.views.canpathwaypage'),
     (r'^impathwaypage$','dbproject.KiPhoDB.views.impathwaypage'),

     (r'^cpathway1$','dbproject.KiPhoDB.views.pathway1'),
     (r'^cpathway2$','dbproject.KiPhoDB.views.pathway2'),
     (r'^cpathway3$','dbproject.KiPhoDB.views.pathway3'),
     (r'^cpathway4$','dbproject.KiPhoDB.views.pathway4'),
     (r'^cpathway5$','dbproject.KiPhoDB.views.pathway5'),
     (r'^cpathway6$','dbproject.KiPhoDB.views.pathway6'),
     (r'^cpathway7$','dbproject.KiPhoDB.views.pathway7'),
     (r'^cpathway8$','dbproject.KiPhoDB.views.pathway8'),
     (r'^cpathway9$','dbproject.KiPhoDB.views.pathway9'),
     (r'^cpathway10$','dbproject.KiPhoDB.views.pathway10'),
     (r'^ipathway11$','dbproject.KiPhoDB.views.pathway11'),
     (r'^ipathway12$','dbproject.KiPhoDB.views.pathway12'),
     (r'^ipathway13$','dbproject.KiPhoDB.views.pathway13'),
     (r'^ipathway14$','dbproject.KiPhoDB.views.pathway14'),
     (r'^ipathway15$','dbproject.KiPhoDB.views.pathway15'),
     (r'^ipathway16$','dbproject.KiPhoDB.views.pathway16'),
     (r'^ipathway17$','dbproject.KiPhoDB.views.pathway17'),
     (r'^ipathway18$','dbproject.KiPhoDB.views.pathway18'),
     (r'^ipathway19$','dbproject.KiPhoDB.views.pathway19'),
     (r'^ipathway20$','dbproject.KiPhoDB.views.pathway20'),


     (r'^suggest$','dbproject.KiPhoDB.views.suggest'),
     (r'^suggest_reaction_protein$','dbproject.KiPhoDB.views.suggest_reaction_protein'),

     (r'^results$','dbproject.KiPhoDB.views.results'),

     #Pages to view query results.
     (r'^results.html','dbproject.KiPhoDB.views.results'),
     (r'^pairs.html','dbproject.KiPhoDB.views.reactions'),
     (r'^sqlresults.html','dbproject.KiPhoDB.views.sqlresults'),
     (r'^tree/(?P<treeID>.*)$','dbproject.KiPhoDB.views.tree'),
     (r'^generateTree.html','dbproject.KiPhoDB.views.generateTree'),
     (r'^advancedsearch.html','dbproject.KiPhoDB.views.advancedSearch'),
     (r'^kinfamily$','dbproject.KiPhoDB.views.kinfamily'),


	 #test
	 (r'^test2$', 'dbproject.KiPhoDB.views.test'),
	 (r'^ajax_test$', 'dbproject.KiPhoDB.views.ajax_test')

)
