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
import logging

from SearchModule import *

log = logging.getLogger(__name__)

# Search on NZBx.co
class ae_FTDworld(SearchModule):
	# Set up class variables
	def __init__(self):
		super(ae_FTDworld, self).__init__()
		self.name = 'FTDworld.net'
		self.shortName = 'FTD'
		self.queryURL = 'http://ftdworld.net/api/index.php'
		self.baseURL = 'http://ftdworld.net'
		self.nzbDownloadBaseURL = 'http://ftdworld.net/spotinfo.php?id='
		#~ self.nzbDownloadBaseURL = 'http://ftdworld.net/cgi-bin/nzbdown.pl?fileID='
		self.active = 1
		self.builtin = 1
		self.login = 0
		self.cookie=0
		
	def dologin(self, cfg):			
		loginurl='http://ftdworld.net/api/login.php'
		urlParams = dict(
			userlogin=cfg['login'],
			passlogin=cfg['pwd']
		)
		try:
			http_result = requests.post(loginurl, data=urlParams)
			data = http_result.json()
			
			self.cookie = {'name' : 'FTDWSESSID',
					'val' : http_result.cookies['FTDWSESSID']}
			log.info('Cookie value: ' + self.cookie)
			return data['goodToGo']
		except Exception as e:
			log.info('Unable to login to server: ' + str(e))
			return False
		
	# Perform a search using the given query string
	def search(self, queryString, cfg):
		#~ rt = self.dologin(cfg)
		
		# Get JSON
		urlParams = dict(
			customQuery='usr',
			ctitle=queryString
		)
		
		results = SearchResults()
		
		try:
			http_result = requests.get(url=self.queryURL, params=urlParams, verify=False, timeout=cfg['timeout'])
		except Exception as e:
			log.error('Failed to get response from server: ' + str(e))
			return results
		
		dataglob = http_result.json()
		if 'data' in dataglob:
			data = dataglob['data'];
					
			for i in xrange(len(data)):
				r = Result()
				r.title = data[i]['Title']
				r.size = int(data[i]['Size'])*1000000
				r.nzbURL = self.nzbDownloadBaseURL + data[i]['id']
				r.timestamp = int(data[i]['Created'])
				r.provider = self.name
				r.providerURL = self.baseURL
				
				results.append(r)
		else:
			log.error('Failed to parse JSON returned by server.')
		return results
