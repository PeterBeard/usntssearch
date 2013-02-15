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
import logging

from SearchModule import *

log = logging.getLogger(__name__)

# Search on NZBx.co
class aa_NZBx(SearchModule):
	# Set up class variables
	def __init__(self):
		super(aa_NZBx, self).__init__()
		self.name = 'nzbX.co'
		self.shortName = 'NZX'
		self.queryURL = 'https://nzbx.co/api/search'
		self.baseURL = 'https://nzbx.co'
		self.active = 1
		self.builtin = 1
		self.login = 0
		
	# Perform a search using the given query string
	def search(self, queryString, cfg):
		# Get JSON
		urlParams = dict(
			q=queryString
		)
		results = SearchResults()
		try:
			http_result = requests.get(url=self.queryURL, params=urlParams, verify=False, timeout=cfg['timeout'])
		except Exception as e:
			log.error('Failed to get response from server: ' + str(e))
			return results
		# Try to parse JSON
		try:
			data = http_result.json()
		except Exception as e:
			log.error('Unable to parse JSON: ' + str(e))
			return results
		# Put the data in a result object and append it to the result list
		for i in xrange(len(data)):
			if data[i]['name']:
				r = Result()
				r.title = data[i]['name']
				if 'fromname' in data[i]:
					r.poster = data[i]['fromname']
				r.size = data[i]['size']
				r.nzbURL = data[i]['nzb']
				r.group = data[i]['groupid']
				r.timestamp = int(data[i]['postdate'])
				r.provider = self.name
				r.providerURL = self.baseURL

			results.append(r)
		return results
