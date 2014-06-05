# define keywords and nomenclatures for consistent naming of IMGT-related variables

#		?? Should this be in dict or class form ??

from collections import namedtuple

def dict_to_namedtuple(dictIn):
	return namedtuple('NamedTuple',dictIn.keys())(**dictIn)

igrep_dict = {
		'seqID': 'seqID',
		'seqNum':'seqNum',
		'vgene': 'Vgene',
		'dgene': 'Dgene',
		'jgene': 'Jgene',
		'junct': 'Junct',
		'vdj':   'VDJ',
		'vj':    'VJ',
		'aa':    'aa',
		'nt':    'nt',
		'aa_field': lambda field: '{}_aa'.format(field),
		'nt_field': lambda field: '{}_nt'.format(field),
		}

igrep_namedtup = dict_to_namedtuple(igrep_dict)

imgt_dict = {
		'seqNum':'Sequence number',
		'seqID': 'Sequence ID',
		'functional': 'Functional',
		'vgene': 'V-GENE and allele',
		'dgene': 'D-GENE and allele',
		'jgene': 'J-GENE and allele',
		'junct': 'JUNCTION',
		'vdj':   'V-D-J-REGION',
		'vj':    'V-J-REGION',
		#'aa_field' : lambda field: 'AA {}'.format(field),
		#'nt_field' : lambda field: 'NT {}'.format(field),
		}

imgt_namedtup = dict_to_namedtuple(imgt_dict)



#igrep_vars = collections.OrderedDict((
#		( 'seqID',    'seqID'),
#		( 'seqNum',   'seqNum'),
#		( 'vgene',    'Vgene'),
#		( 'dgene',    'Dgene'),
#		( 'jgene',    'Jgene'),
#		( 'junct',    'Junct'),
#		( 'vdj',      'VDJ'),
#		( 'vj',       'VJ'),
#		( 'aa',       'aa'),
#		( 'nt',       'nt'),
#		( 'aa_field', lambda field: '{}_aa'.format(field)),
#		( 'nt_field', lambda field: '{}_nt'.format(field))
#	))


#class IgRep(object):
#	varnames = {
#		'seqID': 'seqID',
#		'seqNum':'seqNum',
#		'vgene': 'Vgene',
#		'dgene': 'Dgene',
#		'jgene': 'Jgene',
#		'junct': 'Junct',
#		'vdj':   'VDJ',
#		'vj':    'VJ',
#		'aa':    'aa',
#		'nt':    'nt',
#		}

#	varsObj = namedtuple(varnames)
#	aa_field = lambda field: '{}_aa'.format(field)
#	nt_field = lambda field: '{}_nt'.format(field)

#class IGMT(object):
#	"""IMGT naming conventions"""
#	pass



""" ~~~~~~~~~~~~~~~~~~~~~~~~~~
	This was in IgPairing.py, commented out. I've forgotten exactly what I had in mind -- it was 
	some way to enforce name consistency.
	~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
########################################################################################
#converters : dict. optional
#Dict of functions for converting values in certain columns. Keys can either be integers or column labels
########################################################################################

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

#cIgrep = imgt.nomenclature.igrep_namedtup
#cImgt =  imgt.nomenclature.imgt_namedtup
#dIgrep = imgt.nomenclature.igrep_dict
#dImgt =  imgt.nomenclature.imgt_dict
#f_common = lambda x: (dImgt(x),dIgrep(x))
#f_aa = lambda x: (dImgt(x),dIgrep(x))
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
