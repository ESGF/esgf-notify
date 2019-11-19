import list2json, sys, os, json, random
from time import time, sleep
from datetime import date, timedelta

from pub_client import publisherClient

if len(sys.argv) < 4:
    print("Usage: python pub-sim-2.py /path/to/datasets <count> <interval>")
    print("<count> = number of datasets to publish")
    print("<interval> = time between start of each publication task")
    exit(-1)

PUB_INTERVAL = float(sys.argv[3])
DEBUG = True
TOT_PERIODS = int(sys.argv[2])
hostname = "pcmdi8vm.llnl.gov"
cert_fn = "cert.pem"

rnd = random.random

pub_list = []
PERIOD = 4  # Count per period
BASE = 2 * PERIOD # number of new-only events to complete
DRS_LEN = 10
quick_retract = -1

def retract_id(instance_id, hostname):

    return "{}|{}".format(instance_id, hostname)

def main():

    # dset_list = []
    # for line in open(sys.argv[1]):
    #     dset_list.append(line.rstrip()) 


    dsetjson = list2json.list_to_json(open(sys.argv[1]), hostname, increment=False)

    DCOUNT = len(dsetjson)

    dsarr = list(range(DCOUNT))
    p_count = 0

    for i in range(DCOUNT):

        x = int(rnd()* DCOUNT )
        tmp = dsarr[i]
        dsarr[i] = dsarr[x]
        dsarr[x] = tmp

    pubCli = publisherClient(cert_fn, hostname)
    print("running main")

    for i, idx in enumerate(dsarr): 

        if i == TOT_PERIODS:
            break

        starttime = time()

        if i < BASE:
            dset = dsetjson[idx]
            dsetid = dset["instance_id"]
            new_xml = list2json.gen_xml(dset)
            pubCli.publish(new_xml)
            print(starttime, i, dsetid, "D-New-Dataset")
            pub_list.append([dsetid, "PUB"])

        else:
            if i % PERIOD <  (PERIOD -2):

                dset = dsetjson[idx]
                dsetid = dset["instance_id"]
                new_xml = list2json.gen_xml(dset)
                pubCli.publish(new_xml)
                print(starttime, i, dsetid, "D-New-Dataset")
                pub_list.append([dsetid, "PUB"])
          


            elif i % PERIOD == (PERIOD - 2):
                # new version should be from old datasets - try this - could be retracted

                listlenbase = (len(pub_list) - 2)

                dset_rec = None
                choice = -1
                # additional case update a retracted version
                # quick new version

                while True:

                    if p_count == (TOT_PERIODS - 2):

                        if DEBUG:
                            print(starttime, "find quick new version")
                        choice = ((TOT_PERIODS - 3) * PERIOD)
                        if DEBUG:
                            print("cat one", choice, len(pub_list)) 
                            print(pub_list[choice])
                    elif p_count == (TOT_PERIODS - 3):
                        if DEBUG:
                            print("find previous retraction")
                        choice =quick_retract
                        if DEBUG:
                            print(starttime,"cat two", choice, len(pub_list)) 
                            print(pub_list[choice])
                        dset_rec = pub_list[choice]
                        break
                    else:
                        choice = int(rnd() * listlenbase)
                        dset_rec = pub_list[choice]
                        if dset_rec[1] == "PUB":
                            break


    #           print "len:", listlenbase, "choice", choice

    

                print(starttime,i, choice, dset_rec, "E-New-version")
                dset = dset_rec[0]
                updated_dset_json = list2json.list_to_json([dset], hostname, increment=True)
                rec = updated_dset_json[0]
                new_ver=rec["instance_id"]
                new_xml = list2json.gen_xml(rec)
                upd_xml = list2json.gen_hide_xml(rec['prev_id'])
                pubCli.update(upd_xml)
                pubCli.publish(new_xml)

                
                pub_list[choice] = [new_ver, "PUB" ] 

            else:
                assert(i % PERIOD == PERIOD -1)


                if p_count == (TOT_PERIODS - 1):
                    # quick retraction
                    choice = ((TOT_PERIODS - 2) * PERIOD)
                    if DEBUG:
                        print(starttime, choice, len(pub_list), "C-Quick-Retraction")
                    ret_str = "C-Quick-Retraction"
                else:
                    choice = int(rnd() * (len(pub_list) -PERIOD))
                    ret_str = "A-New-Retraction"
                    quick_retract= choice
                    if DEBUG:
                        print(starttime, choice, len(pub_list), ret_str)
                dset_rec = pub_list[choice]
                
                dset = dset_rec[0]
                pubCli.retract(retract_id(dset, hostname))
                pub_list[choice] = [dset, "RETR"]

        endtime = time()
        eltime = endtime - starttime
        sleep (PUB_INTERVAL - eltime )


if __name__ == '__main__':
    main()

