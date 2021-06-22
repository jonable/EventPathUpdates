
import subprocess
import os
import xml.etree.ElementTree as ET


def query(query, utility_path=None):
	"""
	Pipes a query in to the queryeventpath program
	"""
	# will need to config this

	if not utility_path:
		raise Exception('DBISAM UTILITY not configured')

	process_path = utility_path
	try:
		proc = subprocess.Popen([
			process_path,
			query
		], stdout=subprocess.PIPE)
	except Exception, e:
		raise e
	
	xml = proc.communicate()[0]
	
	# print os.path.join(os.path.expanduser('~'), 'Desktop','output.xml')	
	# open(os.path.join(os.path.abspath('./dbisam/data'),'output.xml'), 'w+').write(xml)

	rows_as_dict = list(parse_xml(xml))	
	return rows_as_dict

def parse_xml(xml):
	""" Parse returned xml from queryeventpath """
	# queryeventpath xml does not add nodes who's value are empty
	# having all the requested columns seems valuable
	# dictified fills in empty columns
	try:	
		root = ET.fromstring(xml)
	except Exception, e:		
		raise Exception('%s \n %s' % (e, xml))

	headers = list(i.getchildren() for i in root[0])[0]
	attrnames = list(x.get('attrname') for x in headers)

	rows = list(i.getchildren() for i in root[1])
	# return list({i.tag: i.text for i in row} for row in rows)	
	
	# dictified = []
	for row in rows:
		nodedict = dict((x, None) for x in attrnames)
		for node in row:
			nodedict[node.tag] = node.text
		yield nodedict		
		# dictified.append(nodedict)
	# return dictified

def is_config(path=None):
	return os.path.exist(path)