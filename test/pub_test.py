from pub_client import publisherClient

import list2json, sys

ARGS = 3

def main(args):

	if len(args) < (ARGS + 1):
		print("Missing required arguments")
		exit(0)


	pubcount = int(args[2])
	hostname = args[1]
	cert_fn = args[3]

	d = list2json.list_to_json(list2json.get_rand_lines(sys.stdin, pubcount), hostname, increment=True)

	pubCli = publisherClient(cert_fn, hostname)

	for rec in d:

		new_xml = list2json.gen_xml(rec)
		upd_xml = list2json.gen_hide_xml(rec['prev_id'])


if __name__ == '__main__':
	main(sys.argv)