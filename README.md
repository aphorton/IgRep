IgRep
=====

so far, just for Ig pairing and data management


Modules
=======

imgt
----

**imgt.IMGT_Loader()** -
Import IMGT results file(s) into a pandas dataframe.

```python
from .loader import	imgt_loader
# directory containing IMGT results files.
imgt_filepath = './imgt_results/exp1'
# specify columns to import & define new names (if desired)
import_fields = {
	"1_Summary": {
		"Sequence ID":  "seqID", 
		"Sequence":     ""
	},
	"3_Nt-sequences": {
		"Sequence ID":  "seqID",
		"V-D-J-REGION": "nt_VDJ",
		"V-J-REGION":   "nt_VJ",
		"JUNCTION":     "nt_Junct"
	},
	"5_AA-sequences": {
		"Sequence ID":  "seqID",
		"V-D-J-REGION": "aa_VDJ",
		"V-J-REGION":   "aa_VJ"
	}
}
# imgt loader class is instantiated with a dir path or list of IMGT file(s).
imgt_loader = IMGT_Loader(imgt_filepath)
imgt_dataframe = imgt_loader.load_all(import_fields, nrows=5)
```



To import a set of file(s), create an IMGT_Loader() object passing either:  
1. directory containing IGMT files  
2. list of file(s)  

All files to import must follow IMGT naming convention for csv output:  
- '1_Summary_*.txt'  
- '2_IMGT-gapped-nt-sequences_*.txt'  
- '3_Nt-sequences_*.txt'  
- '4_IMGT-gapped-AA-sequences_*.txt'  
- '5_AA-sequences_*.txt'  
- '6_Junction_*.txt'  
- '7_V-REGION-mutation-and-AA-change-table_*.txt'  
- '8_V-REGION-nt-mutation-statistics_*.txt'  
- '9_V-REGION-AA-change-statistics_*.txt'  
- '10_V-REGION-mutation-hotspots_*.txt'  
- '11_Parameters_*.txt'  

Methods for user to define alternate file prefixes may be considered.


######IMGT_Loader.load_all(import_fields=None, merge_on='Sequence ID', safe_mode=True, **pd_params):

`import_fields` if *None* or not given, all columns are loaded.

`merge_on` column to combine imported data with. Usually *Sequenc ID*. The can be the name before or after renaming the columns, though the pre-rename value takes precedence in case of conflict.

`**pd_params` collects arguments that may be passed to *pandas.read_csv*, though *header*, *names*, *usecols*, *low_memory*, and *sep* are reserved.

- - - -
