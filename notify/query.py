from datetime import datetime, timedelta
import logging

import requests
from operator import add
from functools import reduce

#QPERIOD='24HOURS'
QPERIOD='7DAYS'

class Query(object):

    def __init__(self, indexNode, interval=7):
        self.log = logging.getLogger(__name__)
        self.esgSearchPath = 'https://%s/esg-search/search' % indexNode
        self.solrPath = 'https://%s/solr/datasets/select' % indexNode

        # Determine what shards are a part of the index node
        esgSearchParams = {
            'limit': 0,
            'format': 'application/solr+json'
        }
        r = requests.get(self.esgSearchPath, params=esgSearchParams)
        res = r.json()
        shards = res['responseHeader']['params']['shards']

        # Setup default parameters
#        dateFormat = "%Y-%m-%dT%H:%M:%SZ"
#        now = datetime.utcnow()
#        self.start =  'NOW-24HOURS' #now.strftime(dateFormat)
        self.start =  'NOW-{}'.format(QPERIOD) #now.strftime(dateFormat)
        self.stop = 'NOW' #(now - timedelta(days=interval)).strftime(dateFormat)

        self.defaultParams = '&wt=json&shards=%s' % shards
        

    def getMessages(self, sub):

        # Build query for each subscriber
        # This is putting it into Solr's query format
        qualifiers = [
            "&fq=%s:(%s)" % (field, ' OR '.join(sub.fields[field]))
            for field in sub.fields
        ]
        query = ''.join(qualifiers)

        # Get all the counts
#        removed_counts = self._counts(query, removed=True)
        all_docs = self._docs(query)
        # Get counts of removed datasets

        return all_docs

    def _docs(self, query, removed=False):
        fq = '&fq=type:Dataset&fq=replica:False&fq=_timestamp:[%s TO %s]' % (self.start, self.stop)
        # Simply add the redacted qualifier to see removals
        if removed:
            fq += '&fq=latest:False'

        ret_fields = ['master_id', 'version', 'latest', 'retracted']

        fl = '&'.join([ "fl=%s" % x for x in  ret_fields])

        params = 'q=*:*&rows=10000&'+ fl + fq + query
#            'rows': 0,
        
        res = self._query(params)
        # None indicates error
        if res is None:
            return None


        self.log.debug('Raw Results: %s', str(res))
        try:
            return res['response']['docs']
        except KeyError:
            self.log.debug('HERE')
            return 0

    def _query(self, params):

        # Combine parameters
 #       params = {**self.defaultParams, **params}
        self.log.debug(str(params))
        # Make request/query
        try:
            r = requests.get(self.solrPath + '?' + params + self.defaultParams)
            r.raise_for_status()
        except requests.exceptions.RequestException as err:
            self.log.error(str(err))
            return None
        return r.json()
    
    
    
