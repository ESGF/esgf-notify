from pub_client import publisherClient

import list2json, sys

hostname = "pcmdi8vm.llnl.gov"
cert_fn = "cert.pem"
increment_in = False

ARGS = 1

def main(args):

	if len(args) < (ARGS + 1):
		print("Missing required arguments")
		exit(0)


	pubcount = int(args[1])
#	hostname = args[1]
#	cert_fn = args[3]

	d = list2json.list_to_json(list2json.get_rand_lines(sys.stdin, pubcount), hostname, increment=increment_in)

	pubCli = publisherClient(cert_fn, hostname)

	for rec in d:

		new_xml = list2json.gen_xml(rec)
		upd_xml = list2json.gen_hide_xml(rec['prev_id'])

		pubCli.update(upd_xml)
		pubCli.publish(new_xml)

if __name__ == '__main__':
	main(sys.argv)
