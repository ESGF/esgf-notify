

DRS = { 'CMIP6' : [ 'mip_era' , 'activity_drs','institution_id','source_id','experiment_id','member_id','table_id','variable_id','grid_label', 'version' ] }


from random import sample

def get_rand_lines(infile, count):

	return sample([line for line in infile], count)


def list_to_json(in_arr, node, **kwargs):

	increment = False
	if ('increment' in kwargs and kwargs['increment']):
		increment=True
	ret = []
	for line in in_arr:

		parts = line.split('.')

		key = parts[0]
		facets = DRS[key]
		d = {}
		for i, f in enumerate(facets):
			d[f] = parts[i]

		d['data_node'] = node
		d['index_node'] = node
		DRSlen = len(DRS[key])
		if increment:
			newvers = int(d['version'][1:]) + 1 
			d['version'] = newvers
			prev_id = '.'.join(parts[0:DRSlen])
			instance_id = '.'.join(parts[0:DRSlen - 1] + ['v' + str(newvers)])
			d['prev_id'] = prev_id
		else:
			instance_id = '.'.join(parts[0:DRSlen])
			d['version'] = d['version'][1:]
		d['instance_id'] = instance_id
		d['master_id'] = '.'.join(parts[0:DRSlen-1])
		d['id'] = instance_id + '|' + node
		d['title'] = instance_id
		d['replica'] = 'false'
		d['latest'] = 'true'
		d['type'] = 'Dataset'
		d['project'] = key + '-test'

		ret.append(d)

	return ret


def gen_xml(fn, d):
	f=open(fn,'w')
	f.write("<doc>\n")
	for key in d:
		f.write('  <field name="{}">{}</field>\n'.format(key, d[key]))
	f.write("</doc>\n")
	f.close()

def gen_hide_xml(id, *args):
        pp = ""
        if len(args) > 0:
                pp = args[0]

	f = open(pp + id + ".prev.xml", 'w')
	txt =  """<updates core="datasets" action="set">
	   <update>
	      <query>instance_id={}</query>
	      <field name="latest">
	         <value>false</value>
	      </field>
	   </update>
	</updates>
	\n""".format(id)
	f.write(txt)
	f.close()

import sys

d = list_to_json(get_rand_lines(sys.stdin, int(sys.argv[1])), 'esgf-test-data.llnl.gov', increment=True)

path_prefix = ""

if len(sys.argv) > 2:

	path_prefix = sys.argv[2]

for rec in d:
	gen_hide_xml(rec['prev_id'], path_prefix)
	gen_xml(path_prefix+rec['instance_id'] + '.xml', rec)


