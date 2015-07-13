#!/usr/bin/env python
#
# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import time

import webapp2
from google.appengine.api import memcache


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
		
        self.response.write(funcioncita())
		


		#self.response.write(projectNumber)

def funcioncita():
	anda='cosa'

	return anda			
		
class FeedPage(webapp2.RequestHandler):
    def get(self):
        rss_feed_url = self.request.get("rssFeedURL")
        data = memcache.get(rss_feed_url)
        if data is None:
            current_time = time.asctime(time.gmtime(time.time()))
            result = 'Loaded into cache at ' + current_time
            memcache.add(rss_feed_url, result, 60)
        else:
            result = 'From Cache : ' + data
        self.response.write(result)

def buscar():

	projectNumber=443899523795;
	projectId="predictorcajas"
	sql = "SELECT hits.item.productSku FROM flatten((select hits.transaction.transactionId from [google.com:analytics-bigquery:LondonCycleHelmet.ga_sessions_20130910] where hits.item.productSku = 'HELM-LIGHT-3'), hits.transaction.transactionId ) as t1  left join each flatten([google.com:analytics-bigquery:LondonCycleHelmet.ga_sessions_20130910] ,hits.transaction.transactionId) as t2 on t1.hits.transaction.transactionId=t2.hits.transaction.transactionId where hits.item.productSku is not null and hits.item.productSku !='HELM-LIGHT-3' limit ";
	queryResults=[]
	queryRequest=[]
	body={ 
    "kind": "bigquery#queryRequest","defaultDataset": {"projectId": projectId, # [Optional] The ID of the project containing this dataset.
      "datasetId": projectId,}, "query": sql}
	 
	 #"timeoutMs": 42, # [Optional] How long to wait for the query to complete, in milliseconds, before the request times out and returns. Note that this is only a timeout for the request, not the query. If the query takes longer to run than the timeout value, the call returns without any results and with the 'jobComplete' flag set to false. You can call GetQueryResults() to wait for the query to complete and read the results. The default value is 10000 milliseconds (10 seconds).
	
	#body=json.dumps(body)
	'''	{"totalRows":"2",
		"kind":"bigquery#queryResponse",
		"schema":
			{"fields":
					[{"name":"hits_item_productSku","type":"STRING","mode":"NULLABLE"}]},
					"jobReference":{"jobId":"job__Q4b8HGdp229xfOtnoxjqkW-XXs","projectId":"prueba-977"},
					"cacheHit":True,
					"jobComplete":True,
					"rows":[{"f":[{"v":"HELM-FOLD-1"}]},
					{"f":[{"v":"VEST-YELLOW-5"}]}],
			"totalBytesProcessed":"0"}
	'''
		
	resultGran=query(projectId, body)
	while (resultGran[jobComplete]==False):
		resultGran=query(projectId, body)
	return resultGran[rows]
		
class Busqueda(webapp2.RequestHandler):	 

	def get(self):
		self.response.write(buscar())
		###AnADIDO
		'''
	
		'''
		
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/feed', FeedPage),
	('/query', Busqueda)
], debug=True)
