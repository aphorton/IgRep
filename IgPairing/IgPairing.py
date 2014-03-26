#import pdb
import pandas as pd
import imgt
from imgt.loader import IMGT_Loader
#from imgt.nomenclature import igrep as cIgrep
#from imgt.nomenclature import imgt as cImgt

# directory containing IMGT results files.
imgt_filepath = u'F:\SkyDrive\QUICK\exampleIMGT'


# specify columns to import & define new names. Use language defined in imgt.nomenclature.
import_fields = {
	"1_Summary": {
		"Sequence ID": "seqID",
		"Functionality": "",
		"V-GENE and allele": "Vgene",
		"D-GENE and allele": "Dgene",
		"J-GENE and allele": "Jgene",
		"Sequence": ""
	},
	"3_Nt-sequences": {
		"Sequence ID": "seqID",
		"V-D-J-REGION": "VDJ_nt",
		"V-J-REGION": "VJ_nt",
		"JUNCTION": "Junct_nt"
	},
	"5_AA-sequences": {
		"Sequence ID": "seqID",
		"V-D-J-REGION": "VDJ_aa",
		"V-J-REGION": "VJ_aa",
		"JUNCTION": "Junct_aa"
	}
}

#cIgrep = imgt.nomenclature.igrep_namedtup
#cImgt =  imgt.nomenclature.imgt_namedtup
#dIgrep = imgt.nomenclature.igrep_dict
#dImgt =  imgt.nomenclature.imgt_dict
#f_common = lambda x: (dImgt(x),dIgrep(x))
#f_aa = lambda x: (dImgt(x),dIgrep('dIgrep(x))
#f_nt = lambda x: (dImgt(x),dIgrep(x))

#import_fields = {
#	'1_Summary': {
#		cImgt.seqID: const['seqID'],
#		'Sequence number': const['seqnum'],
#		'Functionality': '',
#		'V-GENE and allele': const['vgene'],
#		'D-GENE and allele': const['dgene'],
#		'J-GENE and allele': const['jgene'],
#		'Sequence': '',
#	},
#	'3_Nt-sequences': {
#		'Sequence ID': const['seqID'],
#		'V-D-J-REGION': nt_field(const['vdj']),
#		'V-J-REGION': nt_field(const['vj']),
#		'JUNCTION': nt_field(const['junct']),
#	},
#	'5_AA-sequences': {
#		'Sequence ID': const['seqID'],
#		'V-D-J-REGION': aa_field(const['vdj']),
#		'V-J-REGION': aa_field(const['vj']),
#		'JUNCTION': aa_field(const['junct']),
#	}
#}


# imgt loader class is instantiated with a dir path or list of IMGT file(s).
imgt_loader = IMGT_Loader(imgt_filepath)

df = imgt_loader.load_all(import_fields)
### tooling around
if df.index.name is not None:
	df.reset_index(inplace=True)
else:
	df.reset_index(inplace=True, drop=True) # needed for the string extract to work (bug)

re_expr = '(?P<Seq_ID>[^ _]+).(?P<Pair_Ind>[12])'
x = df['seqID'].str.extract(re_expr)
df['seqID'] = x['Seq_ID']

x['Pair_Ind'] = x['Pair_Ind'].astype(int) # convert pair to int.  This is probably unnecessary and potentially bad but may speed up the following indexing operations.
ind_R1 = x['Pair_Ind'] == 1
ind_R2 = x['Pair_Ind'] == 2

df_R1 = df[ind_R1]
df_R2 = df[ind_R2]

df_paired = df_R1.merge(df_R2, how='outer', on=['seqID'], suffixes=['_R1','_R2'])

df_matches = df_paired[(df_paired['num_R1']>0) & (df_paired['num_R2']>0)]


########### cruft below

#re_expr='[^:]*:[^:]*:[^:]*:(?P<Seq_ID>[^ _]+).(?P<Pair_Ind>[12])'

#print(x['Pair_Ind'].unique())

#filename = r'C:\SkyDrive\QUICK\exampleIMGT\1_Summary_397_IMGTheavys_ab_080812.txt'
#x = imgt.pd_load(filename, import_fields,
#imgt_loader.file_headers['1_Summary'])

#df = x.join(df)
#df.set_index(['Seq_ID','Pair_Ind'], inplace=True)
#df.sort(inplace=True)

#df[0:3]


#const = {'seqID': 'seqID',
#		 'seqNum':'seqNum',
#		 'vgene': 'Vgene',
#		 'dgene': 'Dgene',
#		 'jgene': 'Jgene',
#		 'junct': 'Junct',
#		 'vdj':   'VDJ',
#		 'vj':	  'VJ',
#		 'aa':    'aa',
#		 'nt':    'nt',
#		 }

#aa_field = lambda field: '{}_aa'.format(field)
#nt_field = lambda field: '{}_nt'.format(field)
