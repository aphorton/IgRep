
import os
from cStringIO import StringIO
import pandas as pd

imgt_filetypes = ['1_Summary', '2_IMGT-gapped-nt-sequences', '3_Nt-sequences', '4_IMGT-gapped-AA-sequences', '5_AA-sequences', '6_Junction', '7_V-REGION-mutation-and-AA-change-table', '8_V-REGION-nt-mutation-statistics', '9_V-REGION-AA-change-statistics', '10_V-REGION-mutation-hotspots', '11_Parameters']

class imgt_loader(object):
	
	def __init__(self, dirname=None, filenames=None):
		self.filesIn = self._filesIn_(dirname,filenames)
		self.file_headers = self.get_header_cols(self.filesIn)

	def _filesIn_(self, dirname, filenames):
		if isinstance(dirname,basestring):
			filesIn = get_filenames(dirname)
		elif filenames is not None:
			if isinstance(filenames, basestring):
				filesIn = [filenames]
			elif all([isinstance(fn,basestring) for fn in filenames]):
				filesIn = list(filenames)
		else:
			return None
		return filesIn

	def get_header_cols(self, files_dict):
		if not isinstance(files_dict,dict):
			return None
		header_cols = {}
		for ft in sorted(files_dict.keys()):
			##### TODO check if all files of a type have same # columns
			header_gen = (get_header(fn) for fn in files_dict[ft])
			header_cols[ft] = None
			while not(header_cols[ft]):
				header_cols[ft] = header_gen.next()
			for h in header_gen:
				if h is not None:
					assert h == header_cols[ft]
		return header_cols

	def load_all(self, import_fields, merge_on='Sequence ID', safe_mode=True, **pd_params):
		
		df = pd.DataFrame()
		for prefix in sorted(import_fields.keys()):
			if not(import_fields[prefix]):
				continue
			filesLoad = self.filesIn.get(prefix)
			
			t_df = []
			for f in filesLoad:
				colsIn = self.file_headers.get(prefix)

				t_df.append(pd_load(f,
							import_fields=import_fields,
							col_names_in=colsIn,
							safe_mode=safe_mode,
							**pd_params))
			if df.empty:
				df = pd.concat(t_df)
				suff_left = ''.join(prefix.partition('_')[1:])
				t = import_fields[prefix][merge_on]
				left_on = (t if t else merge_on)
			else:
				suff_right = ''.join(prefix.partition('_')[1:])
				t = import_fields[prefix][merge_on]
				right_on = (t if t else merge_on)
				df = df.merge(pd.concat(t_df),
							  left_on = left_on,
							  right_on = right_on,
							  how = 'outer',
							  suffixes = (suff_left,suff_right))
				suff_left = suff_right
				left_on = right_on
		return df
pass

def pd_load(fileIn, import_fields=None, col_names_in=None, safe_mode=True, **pd_params):
	"""
	col_names_in: column names, ignored if file has header. ~~~ Fix this? ~~~
	"""
	cols = return_cols(import_fields, fileIn)
	if cols['use'] is None:
		return

	pd_load = pd.read_csv

	# get file header names, checking if first first field == 'Sequence number'
	header_names = get_header(fileIn,
							  checkfun = lambda x: x[0] == ('Sequence number'))
	
	if (header_names is None) and safe_mode: # then the file might be malformed
		"""Read file into buffer, prepending a valid header line.
		Pandas has trouble with IMGT files, specifically when 'usecols' is set &
		first row has fewer fields than the max."""
		header_line = '\t'.join(col_names_in)
		with open(fileIn) as fidIn:
			s = StringIO()
			s.write(header_line)
			s.write('\n')
			s.write(fidIn.read())
			s.seek(0)
		load_this = s
		header_row = 0 # header_row is input arg to pandas.read* specifying header row number
		names = None
	else:
		load_this = fileIn
		if header_names is not None:
			header_row = 0 # header_row is input arg to pandas.read* specifying header row number
			names = None
		else:
			header_row = None
			names = col_names_in  # could be a problem if dimension mismatch
	
	#pd_params.update({
	#		'header' : header_row,
	#		'names' : names,
	#		'sep' : '\t',
	#		'usecols' :cols['use'],
	#		'low_memory' :False
	#		})
	df = pd_load(load_this,
				  header = header_row,
				  names = names,
				  sep = '\t',
				  usecols=cols['use'],
				  low_memory=False,
				  **pd_params)
	if cols['rename'] is not None and len(cols['rename']) > 0:
		df.rename(columns = cols['rename'],
				  inplace = True)
	return df

def get_filenames(dirname, imgt_filetypes=None):
	"""Returns imgt filetype-specific filenames.
	The commented out stuff reorganizes this data -- could be useful later.
	Vars in 'imgt_filetypes' must be either
	  - integers corresponding to the IMGT files
	  - strings of the imgt file prefixes [must start with numbers. :( Hardcoded.]"""
	if imgt_filetypes is None:
		imgt_filetypes = ['1_Summary', '2_IMGT-gapped-nt-sequences', '3_Nt-sequences', '4_IMGT-gapped-AA-sequences', '5_AA-sequences', '6_Junction', '7_V-REGION-mutation-and-AA-change-table', '8_V-REGION-nt-mutation-statistics', '9_V-REGION-AA-change-statistics', '10_V-REGION-mutation-hotspots', '11_Parameters']
	elif all([isinstance(s,int) for s in imgt_filetypes]):
		t = ['', '1_Summary', '2_IMGT-gapped-nt-sequences', '3_Nt-sequences', '4_IMGT-gapped-AA-sequences', '5_AA-sequences', '6_Junction', '7_V-REGION-mutation-and-AA-change-table', '8_V-REGION-nt-mutation-statistics', '9_V-REGION-AA-change-statistics', '10_V-REGION-mutation-hotspots', '11_Parameters']
		imgt_filetypes = [t[i] for i in imgt_filetypes]
	files = sorted(os.walk(dirname).next()[2])
	fn_imgt = {} # maps imgt file types or numbers to files in path
	#fn_proj = {} # maps sequence set base names to imgt files
	for s in imgt_filetypes:
		i = int(s.partition('_')[0])
		for file in files:
			if file.startswith(s):
				file_fullpath = os.path.join(dirname,file)
				#fn_suffix = os.path.splitext(file)[0].partition(s + '_')[2]
				#fn_proj.setdefault(fn_suffix,{}).update({i:file_fullpath,
				#s:file_fullpath})
				fn_imgt.setdefault(s,[]).append(file_fullpath)
				#fn_imgt.setdefault(i,[]).append(file_fullpath)
				#fn_imgt.setdefault('all',[]).append(file_fullpath)
	#x = os.path.commonprefix(q)
	#maxind = max([x.rfind(c) for c in list('_ -')])
	#if maxind > 1:
	#	common_name = x[:maxind]
	#	fn_proj[common_name]={}
	#	for f in q:
	#		sub_name = f[maxind:].strip('_ -')
	#		fn_proj[common_name][sub_name] = fn_proj[f]
	#pprint(fn_proj)
	#pprint(fn_imgt)
	return fn_imgt

def get_header(filename, delim='\t', checkfun=lambda x: x[0] == ('Sequence number')):
	"""Get first line of file, split by delimiter.
	Also, verifies first line is header, given funct handle 'checkfun'.
	  If does not pass check, returns None."""
	with open(filename) as fid:
		fields = fid.readline().rstrip('\r\n').split(delim)
	if checkfun is not None:
		try:
			assert(checkfun(fields))
		except:
			fields = None
	return fields

def return_cols(import_fields, filename):
	"""Defines pandas options 'usecols' and 'rename'.
	returns dict:
	{ use : columns (names or indices) to import,
	  rename : { old_col_name: new_col_name }
	}
	import_fields can be:
	  1. dict { IMGT_filetype: cols (dict or list) }
	  2. dict { cols: rename vals }
	  3. list/tuple/set of cols
	  4. None - returns all columns
	'cols' can be names or indices
	"""
	if import_fields is None:
		return {'use': None, 'rename': None}

	if isinstance(import_fields,dict):
		fbasename = os.path.basename(filename)

		ftype = [ft for ft in imgt_filetypes if fbasename.startswith(ft)][0] # return the IMGT file type of the current file

		if not(ftype): raise Exception, "can't identify IMGT file type of input file"

		if not(import_fields.has_key(ftype)):
			return None

		fields = import_fields[ftype]
	else:
		fields = import_fields

	if isinstance(fields,dict):
		rename = {k:v for k,v in fields.iteritems() if v}
		usecols = fields.keys()
	else:
		usecols = list(fields)
		rename = {}
	return { 'use': usecols, 'rename': rename }

