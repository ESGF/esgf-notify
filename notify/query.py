from datetime import datetime, timedelta
import logging

import requests

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
        dateFormat = "%Y-%m-%dT%H:%M:%SZ"
        now = datetime.utcnow()
        self.stop = now.strftime(dateFormat)
        self.start = (now - timedelta(days=interval)).strftime(dateFormat)
        self.defaultParams = {
            'wt': 'json',
            'shards': shards,
        }

    def getMessages(self, sub):

        # Build query for each subscriber
        # This is putting it into Solr's query format
        qualifiers = [
            "%s:(%s)" % (field, " OR ".join(sub.fields[field]))
            for field in sub.fields
        ]
        query = ' AND '.join(qualifiers)

        # Get all the counts
        all_counts = self._counts(query)
        # Get counts of removed datasets
        removed_counts = self._counts(query, removed=True)
        results = {
            'all': all_counts,
            'removed': removed_counts,
            'new': all_counts - removed_counts
        }
        self.log.debug("Results: %s", str(results))
        return results

    def _counts(self, query, removed=False):
        fq = 'type:Dataset AND replica:False AND _timestamp:[%s TO %s]' % (self.start, self.stop)
        # Simply add the redacted qualifier to see removals
        if removed:
            fq += ' AND latest:false'
        params = {
            'q': '*:*',
            'facet': 'true',
            'facet.query': query,
            'fq': fq,
#            'rows': 0,
        }
        res = self._query(params)
        # None indicates error
        if res is None:
            return None

        results = res['facet_counts']['facet_queries']
        query_used = res['responseHeader']['params']['facet.query']
        self.log.debug('Raw Results: %s', str(res))
        try:
            return results[query_used]
        except KeyError:
            self.log.debug('HERE')
            return 0

    def _query(self, params):

        # Combine parameters
        params = {**self.defaultParams, **params}
        self.log.debug(str(params))
        # Make request/query
        try:
            r = requests.get(self.solrPath, params=params)
            r.raise_for_status()
        except requests.exceptions.RequestException as err:
            self.log.error(str(err))
            return None
        return r.json()
    
    
    
