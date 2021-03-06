import os
from .loader import	pd_load, IMGT_Loader
import nomenclature

#__all__ = ['imgt','load']
#import load

# put this in a general tools module and STRUCTURE IT BETTER
class rsrc(object):
	"""Use for accessing imgt resource files."""
	def __init__(self,subdirs=None):
		self.path = self.pkg_path('data',subdirs)
		self.files = self.dir_files()
	
	#def add_resource()...
	
	def pkg_path(self,resourceDir=None,subdirs=None):
		pn_base = os.path.abspath(os.path.join(os.path.dirname(__file__),resourceDir))
		if subdirs:
			return os.path.join(pn_base,subdirs)
		else:
			return pn_base

	def dir_files(self):
		"""Get files within top level of given directory.
		Return dict with keys:
			'_all_' : all files
			'<ext1>': files with <ext1>
			'<ext2>': files with <ext2>
		etc. """
		try:
			files = os.walk(self.path).next()[2]
		except:
			raise Exception("{} is not accessible".format(self.path))
		
		contents = {'_all_' : files}
		[contents[ext[1:]].append(base + ext) if contents.has_key(ext[1:]) 
				else contents.update({ext[1:]:[base + ext]})
			for base,ext in [os.path.splitext(f) for f in files]]

		return contents


