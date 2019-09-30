import logging
from logging.handlers import RotatingFileHandler

from notify.sub import Sub
from notify.query import Query

from db.query_engine import QueryEngine

import json
import random
import time, sys

from tracking import ResultTracker
from esgf_feedback.send_job import process_users

HOSTNAME='pcmdi8vm.llnl.gov'
#QPERIOD='5DAYS'
QPERIOD='20HOURS'
LATEST=False
DEBUG=True
MAIL=False


def main(indexNode):

    with open('/esg/config/.esg_pg_pass') as f:
        dbpass = f.read().rstrip()

    # Logging
    filename = 'noti.log'
    rotater = RotatingFileHandler(filename, maxBytes=pow(2, 20), backupCount=2)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)s %(levelname)s:%(message)s',
        handlers=[rotater]
    )


    tracker = ResultTracker()

    qe = QueryEngine('postgresql://dbsuper:{}@localhost/esgcet'.format(dbpass))
  
    my_subs = [
        Sub(
            i, x[1], x[0]
        )
        for i,x in enumerate(qe.get_rows())
    ]
    start = time.time()

    my_query = Query(indexNode, interval=QPERIOD)

    tmp_res = []
    for sub in my_subs:

        res = my_query.getMessages(sub, latest=LATEST)

        if len(res) > 0:

            # In the latest case we are just looking for all datasets matching criteria
            if LATEST:
                tmp_res.append(["{}.v{}".format(x["master_id"],x["version"]) for x in res])
            else:  # we are tracking results
                tracker.track_results(sub.email, res)

    
    if LATEST and len(tmp_res) > 0:
        combo_res = [x for y in tmp_res for x in y]
        print("\n".join(combo_res))
        print('')
    else:
        combo_res =tracker.combine_user_res()
        if DEBUG:
            outstr = str(combo_res).replace('},', '},\n')
            print(outstr)
        if MAIL:
            process_users(combo_res)

# DEBUG        print (json.dumps(res, indent=2, sort_keys=True))

    dur = time.time() - start
    avg = dur/len(my_subs)
    print (indexNode, 'total: {}, avg: {}'.format(dur,avg))


#if (len(sys.argv) < 2):
#    print ("missing required indexNode arguement")

#main(sys.argv[1])
main(HOSTNAME)
