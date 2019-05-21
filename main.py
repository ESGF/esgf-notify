
import logging
from logging.handlers import RotatingFileHandler

from notify.sub import Sub
from notify.query import Query

import json
import random
import time
def main():
    

    # Logging
    filename = 'noti.log'
    rotater = RotatingFileHandler(filename, maxBytes=pow(2, 20), backupCount=2)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)s %(levelname)s:%(message)s',
        handlers=[rotater]
    )
    nQs = 1
    variants = ['r1i1p1f1', 'r1i1p1f2', 'r3i1p1f1', 'r8i1p1f1']
    my_subs = [
        Sub(
            str(i), 
            {
                'project':['CMIP6', 'CORDEX'],
                'variant_label': random.sample(variants, k=random.randint(1, len(variants)-1))
            }
        )
        for i in range(nQs)
    ]
    indexNodes = [
        # 'esg-dn1.nsc.liu.se',
        # 'esg.pik-potsdam.de',
        # 'esgdata.gfdl.noaa.gov',
        # 'esgf-data.dkrz.de',
        # 'esgf-index1.ceda.ac.uk',
        # 'esgf-index3.ceda.ac.uk',
        # 'esgf-index4.ceda.ac.uk', 
        # 'esgf-node.ipsl.upmc.fr',
        'esgf-node.llnl.gov',
        # 'esgf.nccs.nasa.gov',
        # 'esgf.nci.org.au'
    ]
    for indexNode in indexNodes:
        start = time.time()
        my_query = Query(indexNode)
        for sub in my_subs:
            res = my_query.getMessages(sub)
            print(json.dumps(res, indent=2, sort_keys=True))
        dur = time.time() - start
        avg = dur/nQs
        print(indexNode, f'total: {dur}, avg: {avg}')
main()
