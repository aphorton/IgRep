#import pdb
import pandas as pd
import imgt
from imgt.loader import IMGT_Loader
#from imgt.nomenclature import igrep as cIgrep
#from imgt.nomenclature import imgt as cImgt

# User-defined directory containing IMGT results files.
#	An included sample set is located in './igTools/data/sample IMGT files'. Make sure it's unzipped.
imgt_filepath = imgt.rsrc('sample IMGT files').path # this is the path to the IMGT files.


# specify columns to import & define new names. Use language defined in imgt.nomenclature.
#	Include a column across all IMGT files that uniquely identifies a sequence. We use 'Sequence ID'.
# @TODO enforce consistency in field naming.
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


# imgt loader class is instantiated with a dir path or list of IMGT file(s).
imgt_loader = IMGT_Loader(imgt_filepath)

df = imgt_loader.load_all(import_fields)
### tooling around
if df.index.name is not None:
	df.reset_index(inplace=True)
else:
	df.reset_index(inplace=True, drop=True) # needed for the string extract to work (bug)

# split original 'Sequence ID' at the underscore. First part is new 'Seq_ID'. Extract 'Pair_Ind' from remainder & toss rest.
#	ex. 'M00619:14:000000000-A0WLN:1:1109:19446:25158_1:N:0' -->
#		'M00619:14:000000000-A0WLN:1:1109:19446:25158', 1
re_expr = '(?P<{field_seqID}>[^ _]+).(?P<{field_pairInd}>[12])'.format(
				field_seqID = 'Seq_ID',   field_pairInd = 'Pair_Ind')
x = df['seqID'].str.extract(re_expr)
df['seqID'] = x['Seq_ID']

x['Pair_Ind'] = x['Pair_Ind'].astype(int) # convert pair to int.  This is probably unnecessary and potentially bad but may speed up the following indexing operations.
ind_R1 = x['Pair_Ind'] == 1
ind_R2 = x['Pair_Ind'] == 2

df_R1 = df[ind_R1]
df_R2 = df[ind_R2]

df_paired = df_R1.merge(df_R2, how='outer', on=['seqID'], suffixes=['_R1','_R2'])



########### cruft below

#df_matches = df_paired[(df_paired.Vgene_R1.isnull() | df_paired.Vgene_R2.isnull())]

#re_expr='[^:]*:[^:]*:[^:]*:(?P<Seq_ID>[^ _]+).(?P<Pair_Ind>[12])'

#print(x['Pair_Ind'].unique())

#filename = r'C:\SkyDrive\QUICK\exampleIMGT\1_Summary_397_IMGTheavys_ab_080812.txt'
#x = imgt.pd_load(filename, import_fields,
#imgt_loader.file_headers['1_Summary'])

#df = x.join(df)
#df.set_index(['Seq_ID','Pair_Ind'], inplace=True)
#df.sort(inplace=True)

#df[0:3]
