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

try:
	from BeautifulSoup import BeautifulSoup, Tag
	bs_version = 3
except Exception:
	from bs4 import BeautifulSoup, Tag # BeautifulSoup 4
	bs_version = 4

log = logging.getLogger(__name__)

# Search on Womble's NZB Index
class Womble(SearchModule):
	# Set up class variables
	def __init__(self):
		super(Womble, self).__init__()
		self.name = 'Womble\'s NZB Index'
		self.shortName = 'WOM'
		self.queryURL = 'http://newshost.co.za/'
		self.baseURL = 'http://newshost.co.za'
		self.builtin = 1
		self.active = 1
	# Perform a search using the given query string
	def search(self, queryString, cfg):
		# Get HTML
		urlParams = dict(
			s=queryString,
		)
		results = SearchResults()
		
		try:
			http_result = requests.get(url=self.queryURL, params=urlParams, verify=False, timeout=cfg['timeout'])
		except Exception as e:
			log.error('Failed to get response from server: ' + str(e))
			return results
		# Parse the HTML with BS
		data = http_result.text
		
		soup = BeautifulSoup(data)
		if bs_version == 4:
			rows = soup.find_all('tr')
		else:
			rows = soup.findAll('tr')
		
		for row in rows:
			if bs_version == 4:
				cells = row.find_all('td')
			else:
				cells = row.findAll('td')
			if len(cells) == 6:
				if cells[3].a:
					# Timestamp is formatted m/d/Y g:i:s pp
					utimestamp = unicode(cells[0].string)
					tend = utimestamp.find('/')
					
					month = int(utimestamp[0:tend])
					tstart = tend+1
					tend = utimestamp.find('/',tstart)
					day = int(utimestamp[tstart:tend])
					tstart = tend+1
					tend = utimestamp.find(' ',tstart)
					year = int(utimestamp[tstart:tend])
					
					tstart = tend+1
					tend = utimestamp.find(':',tstart)
					hour = int(utimestamp[tstart:tend])
					tstart = tend+1
					tend = utimestamp.find(':',tstart)
					minute = int(utimestamp[tstart:tend])
					tstart = tend+1
					tend = utimestamp.find(' ',tstart)
					second = int(utimestamp[tstart:tend])
					
					timestruct = (year, month, day, hour, minute, second, 0, 0, 0)
					
					timestamp = time.mktime(timestruct)
					
					ufilesize = unicode(cells[1].string).replace(',','')
					scale_factor = 1000
					if ufilesize.find('MB') > -1:
						scale_factor = 10**6
					elif ufilesize.find('GB') > -1:
						scale_factor = 10**9
					elif ufilesize.find('TB') > -1:
						scale_factor = 10**12
					
					ufilesize = ufilesize[0:ufilesize.find('&')]
					
					filesize = int(float(ufilesize) * scale_factor)
					poster = ''
					url = unicode(cells[3].a['href'])
					# Search term is highlighted with a <span>. Remove this.
					title = ''
					for part in cells[5].contents:
						if isinstance(part, Tag):
							title = title + unicode(part.string)
						else:
							title = title + unicode(part)
					r = Result()
					r.title = title
					r.poster = poster
					r.size = filesize
					r.nzbURL = self.baseURL + '/' + url
					r.timestamp = timestamp
					r.provider = self.name
					r.providerURL = self.baseURL
					
					results.append(r)
		
		return results