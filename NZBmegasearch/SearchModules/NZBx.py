# # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## #    
#~ This file is part of NZBmegasearch by pillone.
#~ 
#~ NZBmegasearch is free software: you can redistribute it and/or modify
#~ it under the terms of the GNU General Public License as published by
#~ the Free Software Foundation, either version 3 of the License, or
#~ (at your option) any later version.
#~ 
#~ NZBmegasearch is distributed in the hope that it will be useful,
#~ but WITHOUT ANY WARRANTY; without even the implied warranty of
#~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#~ GNU General Public License for more details.
#~ 
#~ You should have received a copy of the GNU General Public License
#~ along with NZBmegasearch.  If not, see <http://www.gnu.org/licenses/>.
# # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## #
import json

from SearchModule import *

# Search on NZBx.co
class NZBx(SearchModule):
	# Set up class variables
	def __init__(self):
		super(NZBx, self).__init__()
		self.name = 'nzbX.co'
		self.queryURL = 'https://nzbx.co/api/search'
		self.baseURL = 'https://nzbx.co'
	# Perform a search using the given query string
	def search(self, queryString):
		# Get JSON
		urlParams = dict(
			q=queryString
		)
		try:
			http_result = requests.get(url=self.queryURL, params=urlParams, verify=False)
		except Exception as e:
			print e
			return []
		
		data = http_result.json()
			
		results = SearchResults()
		for i in xrange(len(data)):
			if data[i]['name']:
				r = Result()
				r.title = data[i]['name']
				r.poster = data[i]['fromname']
				r.size = data[i]['size']
				r.nzbURL = data[i]['nzb']
				r.group = data[i]['groupid']
				r.timestamp = int(data[i]['postdate'])
				r.provider = self.name
				r.providerURL = self.baseURL

			results.append(r)
		return results