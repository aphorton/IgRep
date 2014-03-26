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


