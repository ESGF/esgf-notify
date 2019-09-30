from pub_client import publisherClient

import list2json, sys

hostname = "pcmdi8vm.llnl.gov"
cert_fn = "cert.pem"
increment_in = False
retract = True

ARGS = 1

def main(args):

    if len(args) < (ARGS + 1):
        print("Missing required arguments")
        exit(0)


    pubcount = int(args[1])
    #	hostname = args[1]
    #	cert_fn = args[3]

    pubCli = publisherClient(cert_fn, hostname)

    if retract:

        for dset in list2json.get_rand_lines(sys.stdin, pubcount):
            print('\"{}\"'.format(dset.strip()))
            dset_id = "{}|{}".format(dset.strip(), hostname)
            pubCli.retract(dset_id)
    else:
        d = list2json.list_to_json(list2json.get_rand_lines(sys.stdin, pubcount), hostname, increment=increment_in)


        for rec in d:

            new_xml = list2json.gen_xml(rec)
            if increment_in:
                upd_xml = list2json.gen_hide_xml(rec['prev_id'])
                pubCli.update(upd_xml)
            pubCli.publish(new_xml)

if __name__ == '__main__':
    main(sys.argv)
