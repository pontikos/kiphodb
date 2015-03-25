import sys
import os
def PATH(*args):
	return os.sep.join([str(x) for x in args])
if __name__ == 'netpath.netpath':
        ABSPATH = os.path.abspath('netpath')
elif __name__ == 'pathway.netpath.netpath':
        ABSPATH = os.path.abspath(PATH('pathway','netpath'))
else:
        ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
# Add to the sys path the path to the dbproject
sys.path.append(PATH(ABSPATH, ".."))
sys.path.append(PATH(ABSPATH, "..", ".."))
#Need to add this for models objects to work
sys.path.append(PATH(ABSPATH, "..", "..", ".."))

# Import all necessary modules.
from uniprotxml import *
from xml.dom.minidom import parseString
import re


#First create a new entry in the source table.
source = Source()
source.source_id = 'NetPath'
source.url = 'http://www.netpath.org/'
source.description = "'NetPath' is a curated resource of signal transduction pathways in humans. It is a collaboration between the PandeyLab at Johns Hopkins University and the Institute of Bioinformatics. At this time, 10 immune and 10 cancer signaling pathways are available."
source.save()


#def saveprotein(gene_name, prot_type, subs):
#	try:
#		protein_uniprot = UniprotEntry(gene=gene_name, organism='Human [9606]',)
#	except Exception, e:
#		print e
#		return None
#	protein_uniprot.save(substrate=subs, protein_type=prot_type, source=source, comment=protein_uniprot.comment('function'))
#	print "saved", protein_uniprot.accession()
#	return protein_uniprot.accession()    

#def savereaction(protein_uniprot,substrate_uniprot,reaction_type):
#	newReaction = Reaction()
#	newReaction.ki_pho_accession_number = Protein(protein_uniprot)
#	newReaction.substrate_accession_number = Protein(substrate_uniprot)
#	newReaction.reaction_type = reaction_type
#	newReaction.reaction_effect = 'A'
#	newReaction.reaction_evidence = 'R'
#	newReaction.reaction_score = '1'
#	newReaction.reaction_description = ''
#	newReaction.source = source
#	newReaction.save()
descriptions=[
"Integrins are cell surface heterodimeric protein complex consisting of one alpha and one beta chain. Integrins act as cell adhesion molecules as well as participate in cellular signaling. The ligands of the alpha6 beta4 integrin are heterotrimers belonging to the laminin family including Laminin A2, Laminin B1, Laminin C1, Laminin A3, Laminin B3, Laminin C2, Laminin A5, Laminin A1 and Laminin B2 among others. Upon activation, the receptor is phosphorylated and associates with adaptor molecules Shc and Grb2, which then activate the PI 3-kinase/Akt, MAPK/NFkB and SMAD signaling modules.",
"The androgen receptor is a member of the nuclear receptor family of ligand activated transcription factors. These receptors bind to steroid hormones, thyroid hormone, retinoids and vitamin D among others, dimerize and bind to DNA. Its ligands include testosterone, dehydroepiandrosterone and androstenedione. Stimulation of the receptor activates the SMAD signaling module",
"There are 4 Notch receptors in humans (Notch 1-4) that bind to a family of 5 ligands (Jagged 1 and 2 and Delta-like 1-3). The Notch receptors are expressed on the cell surface as heterodimeric proteins and their ligands are also membrane-bound. Signaling through the Notch receptors is triggered by ligand-binding that induces cleavage of the extracellular domain by an ADAM family metalloprotease followed by a cleavage within the transmembrane domain by gamma secretase complex. The second cleavage leads to translocation of the cytosolic domain of Notch receptors into the nucleus. Notch proteins are important in lineage specification and stem cell maintenance. Aberrant Notch signaling has been linked to a number of malignancies including leukemias, lymphomas and carcinomas of the breast, skin, lung, cervix and kidneys. ",
"The epidermal growth factor receptor (EGFR1) is a cell surface receptor that belongs to the EGFR/erbB family of receptor tyrosine kinases. Upon binding to its ligand Epidermal Growth Factor (EGF), this receptor can undergo homodimerization or heterodimerize with other members of the erbB family, ERBB2, ERBB3 or ERBB4, resulting in phosphorylation of the receptor subunits. In addition to EGF, the EGFR1 also binds to transforming growth factor alpha (TGF alpha), Amphiregulin, Betacellulin, Epiregulin and Heparin-binding EGF-like growth factor (HB-EGF). Ligand binding activates the Ras/Raf/MAPK signaling modules.",
"Inhibitor of DNA binding (ID) proteins are members of the helix-loop-helix (HLH) family of proteins which lack a DNA binding domain themselves but bind to other family members inhibiting their DNA binding capacity. This family of proteins is comprised of IDs 1, 2, 3 and 4. They can be stimulated by ligands such as the Vascular Endothelial Growth Factor (VEGF), TGF beta and the T cell receptor.",
"Kit is a receptor protein tyrosine kinase, which is a receptor for stem cell factor or kit ligand. Signaling through Kit is important for formation of red cells, lymphocytes, mast cells and platelets among others. Binding of Kit receptor to stem cell factor leads to an intracellular cascade of events that includes activation of PI 3-kinase, Src family kinases and PLC gamma. Activating mutations in the Kit receptor are associated with several human malignancies include leukemias, gastrointestinal stromal tumors and mastocytomas.",
"The TGF beta receptors TGFBR1 and TGFBR2 belong to a subfamily of membrane-bound serine/threonine kinases which are designated as Type I or II based on their structural and functional properties. The receptor is composed of pairs of type I or II arranged in a heterotetrameric complex. Its ligand, TGF beta, has 3 members - TGFB1, TGFB2 and TGFB3, which can homodimerize or heterodimerize before binding to the receptors. Ligand binding activates the MAPK/SMAD signaling modules.",
"Wnt family of proteins are a large family of cysteine-rich secreted glycoproteins that regulate cell-cell interactions. They bind to members of the Frizzled family of 7 transmembrane receptors. Binding of Wnt to its receptors leads to activation of at least 3 distinct pathways: i) the canonical beta catenin pathway, ii) the planar cell polarity pathway, and, iii) the calcium pathway. In the canonical beta catenin pathway, binding of Wnt to its receptors leads to stabilization of beta catenin in the cytosol followed by its translocation into the nucleus where it activates the transcription factor Tcf/Lef leading to upregulation of target genes. The non canonical planar cell polarity pathway involves activation of Dishevelled, small G proteins (Rho/Rac) and JNK. The non canonical calcium pathway involves activation of calcium sensitive kinases, PKC and CAMKII by Dishevelled. The Wnt signaling pathway is similar to the Hedgehog pathway in many respects. Abnormalities in the Wnt signaling pathway are associated with a large variety of human malignancies including tumors of breast, colon, pancreas, liver and bone.",
"The Tumor Necrosis Factor alpha is a proinflammatory cytokine belonging to the TNF superfamily. It signals through 2 separate receptors - TNFRSF1A and TNFRSF1B, both members of the TNF receptor superfamily. Activation by the homotrimeric ligand results in receptor trimerization. TNFRSF1A trimers result in the activation of NF-kB through MAPK and caspase pathways leading to apoptosis, whereas a heterocomplex of both TNFRSF1A and TNFRSF1B recruits proteins such as BIRC2 and BIRC3, which are apoptotic inhibitors. As both TNF alpha and IL-1 stimulate the MAPK signaling module and activate NFkB, they are synergistic and complement each other's activity.",
"The Hedgehog proteins are a family of secreted ligands that include sonic hedgehog, Indian hedgehog and desert hedgehog in humans. Binding of Hedgehog ligands to their receptors, Patched 1 and 2, prevents inhibition of a 7 transmembrane receptor called Smoothened. This leads to activation of GLI family of transcription factors (GLI1-3). Signaling through the Hedgehog pathway is essential for development of many tissues and organs. This pathway is highly conserved among metazoans. Aberrant activation of this pathway has been associated with a number of human malignancies including carcinoma of lung, esophagus, pancreas and prostate.",
"The T cell receptor complex includes the ligand binding TCR alpha and TCR beta chains, along with CD3 gamma, delta, epsilon and zeta subunits. This receptor complex is stimulated by antigen peptides presented by the Major Histocompatibility Complex proteins present on T cells and antigen presenting cells. Stimulation of the T cell receptor leads to the activation of NFkB and NFAT signaling modules which play a key role in T cell receptor signaling.",
"The B cell receptor includes membrane mu heavy chain molecules bound to a light chain and an Ig alpha (CD79A)/Ig beta (CD79B) heterodimer. Activation of the B cell receptor involves phosphorylation of the cytoplasmic immunoreceptor tyrosine-based activation motifs (ITAMs) present in Ig alpha and beta. This leads to activation of several non-receptor tyrosine kinases including those of the Src, Tec and Syk family of kinases. Downstream messengers include DAG, IP3, MAPK/ERK and JNK signaling modules.",
"The interleukin 1 family of cytokines includes interleukin-1 alpha (IL1A), beta (IL1B) and the IL-1 receptor antagonist (IL1RN). These bind to the IL-1 receptor (IL1R1) as well as its decoy receptor, IL1R2. Upon binding to the ligands, interleukin-1 alpha or beta, IL1R1 interacts with IL-1 receptor accessory protein (IL1RAP) to activate the MAPK/JNK signaling modules. The MAPK pathway leads to activation of NFkB complex. As both IL-1 and TNF alpha stimulate the MAPK signaling module and activate NFkB, they are synergistic and complement each other's activity.",
"Interleukin-2 belongs to a family of cytokines, which includes IL-4, IL-7, IL-9, IL-15 and IL-21. IL-2 signals through a receptor complex consisting of IL-2 specific IL-2 receptor alpha (CD25), IL-2 receptor beta (CD122) and a common gamma chain (gamma c), which is shared by all members of this family of cytokines. Binding of IL-2 activates the Ras/MAPK, JAK/Stat and PI 3-kinase/Akt signaling modules.",
"Interleukin-3 belongs to a family of cytokines, which includes IL-5 and GM-CSF. It signals through a receptor complex comprising of an IL-3 specific IL-3 receptor alpha subunit (IL3RA) and a common beta chain, which is shared between all members of this cytokine family. Binding of IL-3 to IL3RA recruits the beta chain to the complex, which activates the JAK/STAT, MAPK and PI 3-kinase signaling modules.",
"Interleukin-4 belongs to the IL-2 family of cytokines, which includes IL-2, IL-7, IL-9, IL-15 and IL-21. It signals through 2 different receptor complexes; Receptor complex 1 comprises of IL-4 receptor alpha (IL4RA) and the common gamma chain (gamma c), Receptor complex 2 comprises of IL4RA and IL-13 receptor alpha1. IL-4 stimulates the JAK/STAT and MAPK signaling modules.",
"Interleukin-5 belongs to the family of cytokines, which includes IL-3 and GM-CSF. It signals through a receptor complex comprising of an IL-5 receptor alpha subunit (IL5RA), and a common beta chain which is shared between all members of this cytokine family. Binding of IL-5 to IL5RA recruits the beta chain to the complex, this then activates the JAK/STAT and Raf/MAPK signaling modules.",
"Interleukin-6 belongs to a family of cytokines which includes IL-11, ciliary neurotrophic factor (CNTF), cardiotropin-1, cardiotrophin-like cytokine, leukemia inhibitory factor (LIF) and Oncostatin M. IL-6 signals through a ternary receptor complex consisting of IL-6 receptor alpha (IL6RA) and a homodimer of the signal transducing receptor gp130. IL-6 stimulates the association of IL6RA to gp130, which then activates the Jak/STAT, Ras/Raf/MAPK and PI 3-kinase signaling modules.",
"Interleukin-7 belongs to a family of cytokines, which includes IL-2, IL-4, IL-9, IL-15 and IL-21. It signals through a receptor complex consisting of IL-7 receptor alpha chain (IL7RA) and a common gamma chain (gamma c) that is shared between all members of this family. IL-7 mainly activates the JAK/STAT signaling module.",
"Interleukin-9 belongs to a family of cytokines, which includes IL-2, IL-4, IL-7, IL-15 and IL-21. It signals through a receptor complex consisting of an IL-9 receptor (IL9R) and a common gamma chain that is shared between all members of this family. IL-9 activates Jak/STAT and MAPK signaling modules."
]

p_names=[
"Alpha6 Beta4 Integrin","AR","Notch","EGFR1","ID","Kit","TGF beta receptor","Wnt","TNF alpha,TNF kB","Hedgehog","T cell receptor","B cell Receptor","IL1","IL2","IL3","IL4","IL5","IL6","IL7","IL9"]
def parse():
	#open the owl files
	for x in xrange(1, 21):
		try:
			print x
			xml_string = file(PATH(ABSPATH, "NetPath_%d.owl" % x), 'r').read()
			dom = parseString(xml_string)
		except Exception,e:
			print e
			exit()

		comment_phosphorylation=[]
		comment_dephosphorylation=[]

		kinases=[]
		kin_substrate=[]

		phos_substrate=[]
		phosphatases=[]
	 
		for name in dom.getElementsByTagName("NAME"):
			#If you find phosphorylation then store the kinase and the substrate
			if not name.firstChild:
				continue;
			if not name.firstChild.data:
				continue;
			data = name.firstChild.data
			if re.search('\ADp-', data):
				data = data.split('-')  
				if re.search('_',data[1]):
					data_phos=data[1].split('_')
					phosphatases.append(data_phos[0])
					phos_substrate.append(data[2])
					continue
				phos_substrate.append(data[2])
				phosphatases.append(data[1])

				newCancerpathway=Cancer_pathway()
				newCancerpathway.pathway_id=x
				newCancerpathway.pathway_name=p_names[x-1]
				newCancerpathway.pathway_description=descriptions[x-1]
				newCancerpathway.protein_id=data[1]
				newCancerpathway.protein_name=''
				newCancerpathway.protein_type='P'
				newCancerpathway.substrate_id=data[2]
				newCancerpathway.substrate_name=''
				newCancerpathway.substrate_type='Ps'
				newCancerpathway.pairs='%s-%s (Phosphatase-Substrate)' % (data[1],data[2])
				if x<11:
					newCancerpathway.pathway_type='1'
				else:
					newCancerpathway.pathway_type='2'
				newCancerpathway.save()

			elif re.search('\AP-', data):
				data = data.split('-')  
				kin_substrate.append(data[2])
				kinases.append(data[1])
				newCancerpathway=Cancer_pathway()
				newCancerpathway.pathway_id=x
				newCancerpathway.pathway_name=p_names[x-1]
				newCancerpathway.pathway_description=descriptions[x-1]
				newCancerpathway.protein_id=data[1]
				newCancerpathway.protein_name=''
				newCancerpathway.protein_type='K'
				newCancerpathway.substrate_id=data[2]
				newCancerpathway.substrate_name=''
				newCancerpathway.substrate_type='Ks'
				newCancerpathway.pairs='%s-%s (Kinase-Substrate)' % (data[1],data[2])
				newCancerpathway.pathway_type='1'
				if x<11:
					newCancerpathway.pathway_type='1'
				else:
					newCancerpathway.pathway_type='2'
				newCancerpathway.save()

		#print kinases
		#print kin_substrate
		#print phosphatases
		#print phos_substrate

		for kin in xrange(0,len(kin_substrate)):
			for phos in xrange(0,len(phos_substrate)):
				if kin==phos:
					newCancerpathway=Cancer_pathway()
					newCancerpathway.pathway_id=x
					newCancerpathway.pathway_name=p_names[x-1]
					newCancerpathway.pathway_description=descriptions[x-1]
					newCancerpathway.protein_id='%s,%s' % (kinases[kin],phosphatases[phos])
					newCancerpathway.protein_name=''
					newCancerpathway.protein_type='O'
					newCancerpathway.substrate_id=phos_substrate[phos]
					newCancerpathway.substrate_name=''
					newCancerpathway.substrate_type='Cs'
					newCancerpathway.pairs='%s-%s-%s (Kinase-Substrate-phosphatase)' % (kinases[kin],phos_substrate[phos],phosphatases[phos])
					if x<11:
						newCancerpathway.pathway_type='1'
					else:
						newCancerpathway.pathway_type='2'
					newCancerpathway.save()				

#	print kinases

#	print kin_substrate
#		for y in xrange(len(phosphatases)):
#			phos_acc = saveprotein(phosphatases[y],'P',False)
#			phos_subs_acc = saveprotein(phos_substrate[y],'O',True)
#			if not phos_acc or not phos_subs_acc:
#				continue
#			savereaction(phos_acc,phos_subs_acc,'D')

#		for y in xrange(len(kinases)):
#			kin_acc = saveprotein(kinases[y],'K',False)
#			kin_subs_acc = saveprotein(kin_substrate[y],'O',True)
#			if not kin_acc or not kin_subs_acc:
#				continue
#			savereaction(kin_acc,kin_subs_acc,'P')


if __name__ == '__main__':
	parse()























