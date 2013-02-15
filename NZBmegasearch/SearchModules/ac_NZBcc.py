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
from SearchModule import *

try:
	from BeautifulSoup import BeautifulSoup
except Exception:
	from bs4 import BeautifulSoup # BeautifulSoup 4

# Search on NZB.cc
class ac_NZBcc(SearchModule):
	# Set up class variables
	def __init__(self):
		super(ac_NZBcc, self).__init__()
		self.name = 'NZB.cc'
		self.shortName = 'NZB'
		self.queryURL = 'https://nzb.cc/q.php'
		self.baseURL = 'https://nzb.cc'
		self.nzbDownloadBaseURL = 'http://nzb.cc/nzb.php?c='
		self.active = 1
		self.builtin = 1
		self.login = 0
		
	# Perform a search using the given query string
	def search(self, queryString, cfg):
		# Get HTML
		urlParams = dict(
			q=queryString
		)
		results = SearchResults()
		
		try:
			http_result = requests.get(url=self.queryURL, params=urlParams, verify=False, timeout=cfg['timeout'])
		except Exception as e:
			print e
			return results
		data = http_result.text
		# Start parsing the text
		cstart = 0
		cend = len(data)
		cstart = data.find("[", cstart, cend)+1

		#~ parse all members and put in parsed data
		inc=1
		
		while True:
			cstart = data.find("[", cstart, cend)+1
			if cstart == 0:
				break
				
			s1 = data.find(',', cstart, cend)
			id_nzb = data[cstart:s1]
			
			s2a = data.find('"', s1+1, cend)+1
			s2b = data.find('"', s2a, cend)
			name = data[s2a:s2b]
			
			s3a = data.find('"', s2b+1, cend)+1
			s3b = data.find('"', s3a, cend)
			poster_name = data[s3a:s3b]

			s4a = data.find('"', s3b+1, cend)+1
			s4b = data.find('"', s4a, cend)
			filelist_preview = data[s4a:s4b]
			
			s5a = data.find('"', s4b+1, cend)+1
			s5b = data.find('"', s5a, cend)
			group = data[s5a:s5b]

			s6a = data.find(',', s5b+1, cend)+1
			s6b = data.find(',', s6a, cend)
			filesize = int(data[s6a:s6b]) * 1000000

			s7a = data.find('"', s6b+1, cend)+1
			s7b = data.find('"', s7a, cend)
			age = data[s7a:s7b]

			s8a = data.find('"', s7b+1, cend)+1
			s8b = data.find('"', s8a, cend)
			release_comments = data[s8a:s8b]

			#~ absolute day of posting
			intage = int(age[0:age.find(' ')])
			today = time.time()
			#dd = datetime.timedelta(days=intage)
			#earlier = today - dd
			posting_date_timestamp = today - intage*3600*24#time.mktime(earlier.timetuple())
			#~ print posting_date_timestamp 

			#~ convert for total nzb url
			#~ GET /nzb.php?c=54132542
			url = self.nzbDownloadBaseURL + id_nzb
			
			cstart = s8b+1

			# Clean up the name
			nstart = name.find('&quot;')+6
			name = name[nstart:name.find('&quot;',nstart)]
			name = name.replace('<b>','')
			name = name.replace('<\/b>','')
			# Create the result object
			r = Result()
			r.title = name
			r.poster = poster_name
			r.size = filesize
			r.nzbURL = url
			r.group = group
			r.timestamp = posting_date_timestamp
			r.provider = self.name
			r.providerURL = self.baseURL
			
			results.append(r)

		return results
