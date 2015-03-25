import sys

if len(sys.argv) < 2:
	print 'Expect at least one arg'


#populate protein tables
if 'protein' in sys.argv or 'phosphabase' in sys.argv:
	import phosphabase
	print 'Starting phosphabase'
	phosphabase.parse()
	print 'Finished phosphabase'

if 'protein' in sys.argv or 'kinbase' in sys.argv:
	import kinbase
	print 'Starting kinbase'
	kinbase.parse()
	print 'Finished kinbase'

if 'protein' in sys.argv or 'phosphopoint' in sys.argv:
	import phosphopoint
	print 'Starting phosphopoint'
	phosphopoint.parse()
	print 'Finished phosphopoint'

if 'protein' in sys.argv or 'phosida' in sys.argv:
	import phosida
	print 'Starting phosida'
	phosida.parse()
	print 'Finished phosida'

if 'protein' in sys.argv or 'phosphoELM' in sys.argv:
	import phosphoELM
	print 'Starting phosphoELM'
	phosphoELM.parse()
	print 'Finished phosphoELM'

if 'protein' in sys.argv or 'kinasecom' in sys.argv:
    import kinasecom
    print 'Starting kinasecom'
    kinasecom.parse()
    print 'Finished Parsing'

#Populate phosphorylation site table
if 'reaction' in sys.argv or 'dbPTM2' in sys.argv:
	from reaction import dbPTM2
	print 'Starting dbPTM2'
	dbPTM2.parse()
	print 'Finished dbPTM2'



#populate reaction table

if 'reaction' in sys.argv or 'reactome' in sys.argv:
	from reaction import reactome
	print 'Starting reaction.reactome'
	reactome.parse()
	print 'Finished reaction.reactome'
	
if 'reaction' in sys.argv or 'networKIN' in sys.argv:
	from reaction import networKIN
	print 'Starting networKIN'
	networKIN.parse()
	print 'Finished networKIN'

if 'pathway' in sys.argv or 'netpath' in sys.argv:
	from pathway import netpath
	print 'Starting pathway.netpath'
	netpath.parse()
	print 'Finished pathway.netpath'
	


#Unused has been moved to unused.
#why though?
#if 'reaction' in sys.argv or 'inact' in sys.argv:
#	from reaction import inact
#	print 'Starting reaction.inact'
#	inact.parse()
#	print 'Finished reaction.inact'


#populate pathway tables
if 'pathway' in sys.argv or 'kegg' in sys.argv:
	from pathway import kegg
	print 'Starting pathway.kegg'
	kegg.parse()
	print 'Finished pathway.kegg'

if 'pathway' in sys.argv or 'panther' in sys.argv:
	from pathway import panther
	print 'Starting pathway.panther'
	panther.parse()
	print 'Finished pathway.panther'

if 'pathway' in sys.argv or 'nci' in sys.argv:
	from pathway import nci_nature_pid
	print 'Starting pathway.nci_nature_pid'
	nci_nature_pid.parse()
	print 'Finished pathway.nci_nature_pid'

if 'pathway' in sys.argv or 'pathway.reactome' in sys.argv:
	from pathway import reactome
	print 'Starting pathway.reactome'
	reactome.parse()
	print 'Finished pathway.reactome'




